import base64
from cornsnake import util_print
from openai import OpenAI
from openai.types import Image
import os
import requests

import service_api_key
import config
from prompts import build_prompt

client = OpenAI(api_key=service_api_key.get_openai_key())


def _download_to(url, file_path):
    print(f"  downloading image from {url} ...")
    r = requests.get(url, allow_redirects=True)
    print(f"  saving image at {file_path}")
    open(file_path, 'wb').write(r.content)

def calculate_word_out_path(word, output_dir, index):
    word = word.replace(' ', '-')
    return os.path.join(output_dir, f"{word}_{index}.jpg")

def generate_images_and_save(word, description, image_count, output_dir) -> None:
    prompt = build_prompt(word, description)

    request_kwargs = {
        'prompt': prompt,
        'n': image_count,
        'model': config.OPENAI_IMAGE_MODEL,
        'size': config.IMAGE_SIZE,
        'quality': config.ACTIVE_QUALITY,
    }

    reference_image_path = config.REFERENCE_IMAGE_PATH
    if reference_image_path:
        if os.path.isfile(reference_image_path):
            print(f"  using reference image: {reference_image_path}")
            with open(reference_image_path, 'rb') as reference_image:
                try:
                    response = client.images.edit(
                        **request_kwargs,
                        image=reference_image,
                    )
                except Exception as e:
                    util_print.print_error(
                        f"  [error] - failed to apply reference image via images.edit: {e}. Continuing without reference image."
                    )
                    response = client.images.generate(**request_kwargs)
        else:
            util_print.print_error(
                f"  [error] - REFERENCE_IMAGE_PATH not found: {reference_image_path}. Continuing without reference image."
            )
            response = client.images.generate(**request_kwargs)
    else:
        response = client.images.generate(**request_kwargs)

    responses = response.data
    if not responses or len(responses) == 0:
        util_print.print_error(f"  [error] - no images returned from AI for word: {word}")
        return

    for i, r in enumerate(responses):
        # dall-e responsds with URLs to download - but GPT-image-1 returns image already in its response (b64_json).
        if isinstance(r, str):
            _download_to(r, calculate_word_out_path(word, output_dir, i))
        elif isinstance(r, Image):
            if r.url:
                _download_to(r.url, calculate_word_out_path(word, output_dir, i))
            elif r.b64_json:
                file_path = calculate_word_out_path(word, output_dir, i)
                print(f"  saving image at {file_path}")
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(r.b64_json))
            else:
                util_print.print_error(f"  [error] - Image object has no url or b64_json")
        else:
            util_print.print_error(f"  [error] - unexpected response type: {type(r)}")
