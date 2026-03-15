import base64
from pathlib import Path
from PIL import Image
from openai import OpenAI
from cornsnake import util_input, util_print

# TODO make this generic
# TODO read from config

client = OpenAI()

OUTPUT_DIR = Path("output/sprites")
OUTPUT_DIR.mkdir(exist_ok=True)


MODEL = "gpt-image-1-mini" # gpt-image-1 is probably better but more expensive.

DESCRIPTION = "scary green alien creature inspired by classic sci-fi xenomorph with elongated head, claws and tail"
TEXTURE = "dark green biomechanical exoskeleton texture"
CREATURE_TYPE = "alien"

CANVAS_SIZE = "1536x1024"

OUTPUT_FILENAME_PREFIX = "alien_top_down"

def build_image_path(filename: str):
    return OUTPUT_DIR / filename.replace(" ", "_")

def save_image(b64_data: str, filename: str):
    path = build_image_path(filename)

    print(f"Saving image to {path}")


    with open(path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return path

def generate_image(prompt: str, size: str, reference_image: Path | None = None):
    if reference_image:
        print("Generating image with reference...")
        with open(reference_image, "rb") as img:
            result = client.images.edit(
                model=MODEL,
                size=size,
                prompt=prompt,
                image=img,
            )
    else:
        print("Generating image...")
        result = client.images.generate(
            model=MODEL,
            size=size,
            prompt=prompt,
        )

    result = result.data[0].b64_json
    print("[done]")
    return result

def should_recreate(image_path: Path, description: str) -> bool:
    if image_path.exists():
        print(f"{description.capitalize()} already exists [{image_path}].")
        should_recreate = util_input.input_with_format_y_or_n(
            "Do you want to re-create it? (y/n)",
            default=False,
        )
        if not should_recreate:
            print(f"Skipping generation for existing {description}.")
            return False
    return True

# -------------------------------------------------
# STEP 1 — Generate direction reference sprites
# -------------------------------------------------

def generate_direction_reference(direction: str):

    prompt = f"""
Game character reference sprite.
Canvas {CANVAS_SIZE}.

Character centered in frame.

Character:
{DESCRIPTION}.

View:
strict orthographic top-down game camera.
Visible from above: top of head, back and shoulders.
Face mostly hidden.

Orientation:
alien facing {direction}.

Style:
detailed 2D game sprite with strong outlines,
painted shading,
{TEXTURE}.

Background:
plain white.
"""

    image_filename = f"alien_reference_{direction}.png"
    image_path  = build_image_path(image_filename)
    if not should_recreate(image_path, "reference image"):
        return image_path

    img_b64 = generate_image(prompt, CANVAS_SIZE)
    return save_image(img_b64, image_filename)


# -------------------------------------------------
# STEP 2 — Generate animation sheets
# -------------------------------------------------

def generate_animation(direction: str, reference_path: Path):

    image_filename = f"{OUTPUT_FILENAME_PREFIX}_walk_{direction}.png"
    image_path = build_image_path(image_filename)

    if not should_recreate(image_path, "animation sheet"):
        return image_path

    prompt = f"""
Game engine sprite atlas using the provided character reference.

Canvas {CANVAS_SIZE} pixels.
Grid layout: 6 columns × 4 rows.
Cell size: 256x256.

The character must match the reference {CREATURE_TYPE} exactly in design, scale and orientation.

Animation:
{CREATURE_TYPE} walking {direction}.
6 sequential frames forming a smooth walk cycle.
Pose changes gradually between frames.

Character position and scale remain identical across frames.

Camera:
strict orthographic top-down game camera.

Style:
detailed 2D game sprite with strong outlines,
painted shading,
{TEXTURE}.

Background:
plain white sprite sheet background.
"""

    img_b64 = generate_image(prompt, CANVAS_SIZE, reference_path)
    return save_image(img_b64, image_filename)


# -------------------------------------------------
# STEP 3 — Combine sheets into final atlas
# -------------------------------------------------

def combine_sheets(down_sheet: Path, right_sheet: Path):
    output = OUTPUT_DIR / (OUTPUT_FILENAME_PREFIX + "_final_atlas.png")
    if output.exists():
        should_recreate = util_input.input_with_format_y_or_n(
            f"Final atlas already exists [{output}]. Do you want to re-create it? (y/n)",
            default=False,
        )
        if not should_recreate:
            print("Skipping atlas assembly.")
            return output

    print("Assembling atlas...")

    down = Image.open(down_sheet)
    right = Image.open(right_sheet)

    width = down.width
    height = down.height + right.height

    atlas = Image.new("RGBA", (width, height))

    atlas.paste(down, (0, 0))
    atlas.paste(right, (0, down.height))

    atlas.save(output)

    return output

def slice_sprite_atlas(atlas_path, animation_name: str, rows, cols, top_margin=0, left_margin=0, row_height=None):
    atlas = Image.open(atlas_path)

    output_dir = OUTPUT_DIR / "frames"
    if output_dir.exists():
        for file in output_dir.glob(f"{animation_name}_*.png"):
            file.unlink()
    else:
        output_dir.mkdir(exist_ok=True)

    frame_index = 0

    usable_width = atlas.width - left_margin
    usable_height = atlas.height - top_margin

    frame_width = usable_width // cols
    frame_height = row_height if row_height is not None else usable_height // rows

    for row in range(rows):
        for col in range(cols):

            x = left_margin + (col * frame_width)
            y = top_margin + (row * frame_height)

            frame = atlas.crop((x, y, x + frame_width, y + frame_height))
            frame = frame.resize((256,256), Image.NEAREST)
            filename = f"{animation_name}_{frame_index}.png"
            frame.save(output_dir / filename)
            frame_index += 1

    print(f"Frames for {animation_name} saved to {output_dir}")
    return output_dir


def prompt_and_slice_sheet(sheet_path: Path, animation_name: str, label: str):
    columns = int(util_input.input_custom(
        f"View the {label} sheet {sheet_path} - tell me the ACTUAL number of columns in the sprite sheet (default 6): ",
        default="6",
    ))
    rows = int(util_input.input_custom(
        " - and the ACTUAL number of rows in the sprite sheet (default 2): ",
        default="2",
    ))

    util_print.print_important("tip: view the image in MS Paint or similar, to check the top/left margins and the actual row height.")
    while True:
        left_margin = int(util_input.input_custom("Left margin in pixels (default 0): ", default="0"))
        top_margin = int(util_input.input_custom("Top margin in pixels (default 0): ", default="0"))
        with Image.open(sheet_path) as atlas:
            computed_row_height = max(1, (atlas.height - top_margin) // rows)
        row_height = int(util_input.input_custom(
            f"Row height in pixels (default {computed_row_height}): ",
            default=str(computed_row_height),
        ))

        output_dir = slice_sprite_atlas(
            sheet_path,
            animation_name,
            cols=columns,
            rows=rows,
            top_margin=top_margin,
            left_margin=left_margin,
            row_height=row_height,
        )

        frame_count = columns * rows
        util_print.print_result(f"{frame_count} frames saved to: {output_dir}")

        try_new_margin = util_input.input_with_format_y_or_n(
            f"Do you want to create the frames again (re-slice) [{sheet_path}] with different margins? (y/n)",
            default=False,
        )
        if not try_new_margin:
            break

# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------

def main():
    util_print.print_section("Game Sprite Generation Pipeline")
    util_print.print_important(f"Using model: {MODEL}")
    util_print.print_section("Step 1: generating direction references")

    ref_down = generate_direction_reference("DOWN toward the bottom of the screen")
    ref_right = generate_direction_reference("RIGHT toward the right side of the screen")

    util_print.print_important("tip: to retry, you can delete the images you don't like, and run again (we skip existing reference images)")
    if not util_input.input_with_format_y_or_n("Please check the reference images. Continue to animation generation? (y/n)", default=True):
        print("Aborting.")
        return

    util_print.print_section("Step 2: generating animations")
    walk_down = generate_animation("DOWN toward the bottom of the screen", ref_down)
    walk_right = generate_animation("RIGHT toward the right side of the screen", ref_right)

    util_print.print_section("Step 3: assembling atlas")

    atlas = combine_sheets(walk_down, walk_right)
    util_print.print_custom(f"Full atlas: {atlas} (warning: right and down might NOT be aligned)")
    util_print.print_result(f"walk_down sheet: {walk_down}")
    util_print.print_result(f"walk_right sheet: {walk_right}")
    util_print.print_important("tip: check the sheets in an editor with a overlay guides such as Affinity Photo (View | Guides). Crop each file so that each sprite fits within the grid.")
    if not util_input.input_with_format_y_or_n("Please check the atlas image. Continue to slicing into frames? (y/n)", default=True):
        print("Skipping the sheet slicing step.")
    else:
        util_print.print_section("Step 4: slicing Step 2 sheets into sprite frames")

        prompt_and_slice_sheet(walk_down, "walk_down", "DOWN")
        prompt_and_slice_sheet(walk_right, "walk_right", "RIGHT")

    util_print.print_result("Done.")


if __name__ == "__main__":
    main()
