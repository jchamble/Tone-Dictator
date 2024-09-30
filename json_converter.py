import json

# Not used, left for documentaton purposes
def convert_to_json(file_path, json_file_path):
    """Converts the original NRC data to a more usable json format"""
    word_emotion_dict = {}

    # Converts the text file to a dictionary
    with open(file_path, 'r') as file:
        for line in file:
            word, emotion, value = line.strip().split('\t')
            value = int(value)
            if word not in word_emotion_dict:
                word_emotion_dict[word] = {}
            word_emotion_dict[word][emotion] = value

    # Creates and writes the json data to given empty file
    json_word_data = json.dumps(word_emotion_dict)
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_word_data)