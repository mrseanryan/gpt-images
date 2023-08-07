# gpt-images

Simple Python client to generate images from a word-list via Open AI (DAL-E)

## Dependencies

- Open-AI API key (for DAL-E)
- Python 3
- Unix or Mac OS (Windows may need some adaptation)

## Usage

1. Set up (see the Setup section)
2. Edit the list of words at [./data/words_no_image.json](./data/words_no_image.json)
3. Run ./go.sh

OR:

```
python ./generate_images_from_words.py <path to JSON file> <path to output directory>
```

4. Check the images at the output directory. By default this is [./output](./output).

## Set up

1. Install openai Python client.

```
pip install openai
```

2. Get an Open AI key

3. Set environment variable with your OpenAI key:

```
export OPENAI_API_KEY="xxx"
```

Add that to your shell initializing script (`~/.zprofile` or similar)

Load in current terminal:

```
source ~/.zprofile
