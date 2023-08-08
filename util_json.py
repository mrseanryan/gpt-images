import json

def read_from_json_file(path_to_json):
    f = open(path_to_json)
    data = json.load(f)
    f.close()
    return data

def read_words_from_json_file(path_to_json):
    json = read_from_json_file(path_to_json)
    simple_words = json['words_no_image']
    words_to_description = dict()
    for word in simple_words:
        words_to_description[word] = word
    if 'complex_words' in json:
        complex_words = json['complex_words']
    for word_and_description in complex_words:
        words_to_description[word_and_description['word']] = word_and_description['description']

    return words_to_description
