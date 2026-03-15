import config

def build_prompt(word: str, description: str) -> str:
    prompt = f"""
        Generate an image that is a typical representation of: <<{description}>>.
        The image must be as realistic as possible, and for a general audience.

        IMPORTANT: do NOT place any text or words in the image.
    """

    CANVAS_SIZE = "1536x1024"

    if config.IMAGE_SIZE is not CANVAS_SIZE:
        raise ValueError(f"[xxxGAME_SPRITE_MODE_TOP_DOWN = True] Unsupported IMAGE_SIZE: {config.IMAGE_SIZE}. Please use {CANVAS_SIZE}.")

    if config.GAME_SPRITE_MODE_TOP_DOWN:
        prompt = f"""
    Game development sprite atlas.
    Canvas size {CANVAS_SIZE} pixels.
    SpriteGrid layout: 6 columns × 2 rows.
    Cell size: 256x256 pixels.
    Each cell contains the same character at the same scale.
    Safe drawing area 200x200 pixels centered inside each cell with empty padding so the character never touches cell borders.
    Character: {description}.
    Camera: strict top-down orthographic view (bird's-eye view).
    Animation layout: Row 1 shows the {word} alien walking DOWN toward the bottom of the screen with its head pointing downward, 6 sequential frames forming a walk cycle from left to right.
    Row 2 shows the {word} alien walking RIGHT toward the right side of the screen with its head pointing right, 6 sequential frames forming a walk cycle from left to right.
    Style: detailed 2D game sprite with strong outlines, stylized painted shading, {config.GAME_TEXTURE_STYLE}, readable top-down silhouette, consistent lighting and proportions across frames.
    Background: plain white sprite sheet background with clear spacing between cells. rows must show clearly different orientations of the character.
    """

    return prompt
