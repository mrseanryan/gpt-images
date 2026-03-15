import config
import textwrap

# TODO remove the game stuff from this file + config. BUT keep the reference image feature.

def build_prompt(word: str, description: str) -> str:
    prompt = f"""
        Generate an image that is a typical representation of: <<{description}>>.
        The image must be as realistic as possible, and for a general audience.

        IMPORTANT: do NOT place any text or words in the image.
    """

    CANVAS_SIZE = "1536x1024"

    if config.IMAGE_SIZE is not CANVAS_SIZE:
        raise ValueError(f"[GAME_SPRITE_MODE_TOP_DOWN = True] Unsupported IMAGE_SIZE: {config.IMAGE_SIZE}. Please use {CANVAS_SIZE}.")

    # TODO make this generic
    if config.GAME_MODE_ENABLED:
        print(f"  [game mode enabled] - adjusting prompt for game sprite generation with texture: {config.GAME_TEXTURE_STYLE}")
        prompt_walk_down = f"""
Game engine sprite atlas.
Canvas size {CANVAS_SIZE}.
Grid layout: 6 columns × 1 row.
Cell size: 256x256 pixels.

Each cell contains the same character at identical scale and position.
Safe drawing area: 200x200 centered inside each cell with empty padding.

Character:
{description}.

View:
strict orthographic top-down game camera.
Visible from above: top of the head, back, shoulders and upper limbs.
Front face and chest mostly hidden.

Animation:
alien walking DOWN toward the bottom of the screen.
6 sequential frames forming a smooth walk cycle.
Pose changes gradually between frames.

Style:
detailed 2D game sprite with strong outlines,
painted shading and subtle highlights,
{config.GAME_TEXTURE_STYLE},
clear readable silhouette from above.

Background:
plain white sprite sheet background.
Clear spacing between cells.
"""

        prompt_walk_right = f"""
Game engine sprite atlas.
Canvas size {CANVAS_SIZE}.
Grid layout: 6 columns × 2 rows.
Cell size: 256x256 pixels.

Each cell contains the same character at identical scale and alignment.
Safe drawing area: 200x200 centered inside each cell.

Character:
{description}.

View:
strict orthographic top-down game camera.

Animation layout:
Row 1: alien walking DOWN toward the bottom of the screen, head pointing downward, 6 frames.
Row 2: alien walking RIGHT toward the right side of the screen, head pointing right, 6 frames.

Frames progress from left to right forming smooth walk cycles.
Pose changes gradually between frames.

Style:
detailed 2D game sprite with strong outlines,
painted shading and subtle highlights,
{config.GAME_TEXTURE_STYLE},
clear readable silhouette from above.

Background:
plain white sprite sheet background with spacing between cells.
"""
        
        prompt_walk_right_with_reference_image = f"""
Game engine sprite atlas using the provided sprite sheet as the reference.

Canvas size {CANVAS_SIZE}.
Grid layout: 6 columns × 1 row.
Cell size: 256x256 pixels.

The character must match the reference alien exactly in design, scale, pose alignment and style.
Safe drawing area: 200x200 centered inside each cell.

Animation:
alien walking RIGHT toward the right side of the screen.
6 sequential frames forming a smooth walk cycle.

View:
strict orthographic top-down game camera.

Style:
detailed 2D game sprite with strong outlines,
painted shading,
{config.GAME_TEXTURE_STYLE}.

Background:
plain white sprite sheet background.
"""

        if config.GAME_SPRITE_MODE_TOP_DOWN__WALKING_DOWN:
            prompt = prompt_walk_down
            if config.REFERENCE_IMAGE_PATH:
                raise ValueError("Reference images are not supported for the 'walking down' sprite mode (only for 'walking right'). Please set REFERENCE_IMAGE_PATH to None in config.py if using GAME_SPRITE_MODE_TOP_DOWN__WALKING_DOWN.")
            print("  [game sprite mode] - using top-down walking down prompt")
        else:
            prompt = prompt_walk_right
            if config.REFERENCE_IMAGE_PATH:
                print("  [game sprite mode] - using top-down walking right prompt with reference image")
                prompt = prompt_walk_right_with_reference_image
                # right neeeds a reference image (the 'walking down' version) to work well, so make sure to set REFERENCE_IMAGE_PATH in config.py
            else:
                print("  [game sprite mode] - using top-down walking right prompt (WARNING: no reference image)")

        prompt += "\nTrue top-down view showing the top of the head, back and shoulders, limbs extending outward from the body."    
        prompt += "\nCharacter position and scale must remain identical across all frames."

    prompt = textwrap.dedent(prompt).strip()
    print(f"  [final prompt]: {prompt}")

    return prompt
