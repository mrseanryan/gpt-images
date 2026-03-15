from enum import Enum, StrEnum, auto
from typing_extensions import Literal

from openai import NotGiven

IMAGES_PER_WORD = 2

IS_DEBUG = False

# Wait to avoid hitting limits:
WAIT_BETWEEN_IMAGES_IN_SECONDS = 15 # rate limit is 5/1min

# ref pricing = https://developers.openai.com/api/docs/pricing/
OPENAI_IMAGE_MODEL = 'gpt-image-1-mini' # gpt-image-1-mini [2026-03] gpt-image-1 [2025-11] - older: dall-e-2 or dall-e-3. dall-e-3 is better, but costs more and only 1 image at a time.

# dall-e-2: up to 1024x1024. dall-e-3: can be one of: 1024x1024, 1792x1024, 1024x1792.
# gpt-image-1-mini: 1024x1024 usually good. up to 1536x1024. gpt-image-1: up to 2048x2048.
IMAGE_SIZE="1024x1024"

QUALITY_FOR_MODEL_GPT_1: NotGiven | Literal['standard', 'hd', 'low', 'medium', 'high', 'auto'] = 'high'
QUALITY_FOR_MODEL_DAL_E: Literal['standard', 'hd'] = 'standard'

ACTIVE_QUALITY = QUALITY_FOR_MODEL_GPT_1

# Game sprite specific config:
GAME_SPRITE_MODE_TOP_DOWN = False  # Adjusts prompt for 2D game, top-down view.
REFERENCE_IMAGE_PATH = "output/alien-sprite-sheet--4e2_0--ok.jpg"  # Optional reference image for style guidance. Set to None if not used.
GAME_TEXTURE_STYLE = "dark green biomechanical exoskeleton texture"  # Texture style for game sprites. Adjust as needed.
