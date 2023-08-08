import openai

import service_api_key

openai.api_key = service_api_key.get_openai_key()

def generate_images(word, image_count):
    prompt = f"""
        Generate an image that is a typical representation of: <<{word}>>.
        The image must be as realistic as possible, and for a general audience.

        IMPORTANT: do NOT place any text or words in the image.
    """

    response = openai.Image.create(
        prompt=prompt,
        n=image_count,
        #size="512x512"
        size="1024x1024",
    )

    responses = response["data"]
    image_urls = []
    for r in responses:
        image_urls.append(r['url'])
    return image_urls
