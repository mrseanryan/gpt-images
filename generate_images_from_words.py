from sys import argv

import util_json

# args
if (len(argv) != 3):
    print(
        f"USAGE: {argv[0]} <path to JSON file with words that need an image> <path to the images output directory>")
    exit(1)

path_to_json_words = argv[1]
output_path_images_dir = argv[2]

words = util_json.read_words_from_json_file(path_to_json_words)
print(f"Generating images for {len(words)} words ...")
