import json

def read_from_json_file(path_to_json):
    f = open(path_to_json)
    data = json.load(f)
    f.close()
    return data

def read_words_from_json_file(path_to_json):
    return read_from_json_file(path_to_json)['words_no_image']
