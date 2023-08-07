# gpt-images

Simple Python client to generate images from a word-list via Open AI (DAL-E)

## Dependencies

- Open-AI API key
- Python 3

## Usage

1. Set up (see the Setup section)
2. Edit the list of words at [./data/words_no_image.json](./data/words_no_image.json)
3. Run ./go.sh

OR:

```
python ./generate_images_from_words.py <path to JSON file> <path to output directory>
```

4. Check the images at the output directory. By default this is [./output](./output).
