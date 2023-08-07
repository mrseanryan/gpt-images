import os
import requests
from sys import argv

import config
import service_images
import util_json
import util_wait

# args
if (len(argv) != 3):
    print(
        f"USAGE: {argv[0]} <path to JSON file with words that need an image> <path to the images output directory>")
    exit(1)

path_to_json_words = argv[1]
output_path_images_dir = argv[2]

words = util_json.read_words_from_json_file(path_to_json_words)
print(f"Generating images for {len(words)} words ...")

def download_to(url, file_path):
    r = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(r.content)

def calculate_word_out_path(word, output_dir, index):
    word = word.replace(' ', '-')
    return os.path.join(output_dir, f"{word}_{index}.jpg")

def generate_images_for_word(word, output_dir):
    urls = service_images.generate_images(word, config.IMAGES_PER_WORD)
    index = 1
    for url in urls:
        download_to(url, calculate_word_out_path(word, output_dir, index))
        index += 1

def are_images_already_generated(word, output_path_images_dir):
    out_file_path = calculate_word_out_path(word, output_path_images_dir, 1)
    return os.path.exists(out_file_path)

if config.IS_DEBUG:
    words = [words[0]]

for word in words:
    word = word.strip()
    print(f"{word}...")
    if are_images_already_generated(word, output_path_images_dir):
        print(f"    [skipping] - already have images")
    else:
        print(f" ... generating ...")
        generate_images_for_word(word, output_path_images_dir)
        print("    [generated]")
        util_wait.wait_seconds(config.WAIT_BETWEEN_IMAGES_IN_SECONDS)

print(f"[done] - see {output_path_images_dir}")
