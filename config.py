IMAGES_PER_WORD = 3

IS_DEBUG = False

# Wait to avoid hitting limits:
WAIT_BETWEEN_IMAGES_IN_SECONDS = 15 # rate limit is 5/1min

OPENAI_IMAGE_MODEL = 'dall-e-2' # dall-e-2 or dall-e-3. dall-e-3 is better, but costs more and only 1 image at a time. suggest: try dall-e-2 first.

IMAGE_SIZE="1024x1024" # dall-e-2: up to 1024x1024. dall-e-3: can be one of: 1024x1024, 1792x1024, 1024x1792.
