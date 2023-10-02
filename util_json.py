import json

def read_from_json_file(path_to_json):
    with open(path_to_json) as f:
        data = json.load(f)
        return data

def write_to_json_file(file_dict, path_to_json):
    with open(path_to_json, 'w') as f:
        json_str = json.dumps(file_dict, indent=2)
        f.write(json_str)

def read_words_from_json_file(path_to_json):
    json = read_from_json_file(path_to_json)
    simple_words = json['words_no_image']
    words_to_description = dict()
    for word in simple_words:
        words_to_description[word] = word
    if 'complex_words' in json:
        complex_words = json['complex_words']
        for word in complex_words.keys():
            words_to_description[word] = complex_words[word]

    return words_to_description

def write_words_to_json_file(words_to_description, path_to_json):
    file_dict = dict()
    file_dict['words_no_image'] = []
    file_dict['complex_words'] = words_to_description
    write_to_json_file(file_dict, path_to_json)
