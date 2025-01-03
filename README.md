# gpt-images

Simple Python client to generate images from a word-list via Open AI (DAL-E)

## Dependencies

- Open-AI API key (for DAL-E)
- Python 3
- Unix or Mac OS (Windows may need some adaptation)

## Usage

1. Set up (see the Setup section)
2. Edit the list of words at [./data/words_no_image.json](./data/words_no_image.json).
3. For **more abstract or complex words, the AI will need your help** to generate better images.

The **LLM's that generate the images have a limited vocabulary**, so words such as
'zabuton' or 'wadi' are not (currently) correctly recognised. Also some words are so abstract, even for a human it is difficult to depict as an image (consider 'depression' or 'friendship' or 'shibboleth').
Also, some words can trigger the safety features of the LLM, for example 'trauma' or 'gruesome'.
For such words, you can add a description to describe the image you would like to see, that represents the word, in the 'complex_words' section of the JSON file.

To set up the JSON structure, you can run `./add_complex_word_templates.sh`.

See the example at [./data/example.words_no_image.json](./data/example.words_no_image.json).

4. Run ./go.sh

OR:

```
python ./generate_images_from_words.py <path to JSON file> <path to output directory>
```

4. Check the images at the output directory. By default this is [./output](./output).

## Set up

0. Install Python and poetry

- Python 3.11
- [Poetry](https://python-poetry.org/docs/)

1. Install openai Python client.

```
poetry install
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
```

Setup is done.
