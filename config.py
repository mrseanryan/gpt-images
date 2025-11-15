from enum import Enum, StrEnum, auto
from typing_extensions import Literal

from openai import NotGiven

IMAGES_PER_WORD = 1

IS_DEBUG = False

# Wait to avoid hitting limits:
WAIT_BETWEEN_IMAGES_IN_SECONDS = 15 # rate limit is 5/1min

OPENAI_IMAGE_MODEL = 'gpt-image-1' # gpt-image-1 [2025-11] - older: dall-e-2 or dall-e-3. dall-e-3 is better, but costs more and only 1 image at a time.

IMAGE_SIZE="1024x1024" # dall-e-2: up to 1024x1024. dall-e-3: can be one of: 1024x1024, 1792x1024, 1024x1792.

QUALITY_FOR_MODEL_GPT_1: NotGiven | Literal['standard', 'hd', 'low', 'medium', 'high', 'auto'] = 'high'
QUALITY_FOR_MODEL_DAL_E: Literal['standard', 'hd'] = 'standard'

ACTIVE_QUALITY = QUALITY_FOR_MODEL_GPT_1
