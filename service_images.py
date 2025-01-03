from cornsnake import util_print
import openai

import service_api_key
import config

openai.api_key = service_api_key.get_openai_key()

def generate_images(word, image_count):
    prompt = f"""
        Generate an image that is a typical representation of: <<{word}>>.
        The image must be as realistic as possible, and for a general audience.

        IMPORTANT: do NOT place any text or words in the image.
    """
    openai.api_type = "openai"

    if config.OPENAI_IMAGE_MODEL == "dall-e-3":
        util_print.print_warning("This model only supports generating 1 image at a time")
        image_count = 1

    response = openai.images.generate(
        prompt=prompt,
        n=image_count,
        model=config.OPENAI_IMAGE_MODEL,
        size=config.IMAGE_SIZE,
        quality="standard"
    )

    responses = response.data
    image_urls = []
    for r in responses:
        image_urls.append(r.url)
    return image_urls
