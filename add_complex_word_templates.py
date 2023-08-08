import os
import requests
from sys import argv

import config
import service_images
import util_json
import util_wait

# args
if (len(argv) != 2):
    print(
        f"USAGE: {argv[0]} <path to JSON file with words that need an image>")
    exit(1)

path_to_json_words = argv[1]
words_to_description = util_json.read_words_from_json_file(path_to_json_words)

print(f"Making all words have a 'complex' entry. You will need to edit the descriptions.")
util_json.write_words_to_json_file(words_to_description, path_to_json_words)
print(f"[done] - {path_to_json_words}")
