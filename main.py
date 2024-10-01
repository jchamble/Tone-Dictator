import json
import re
import math
import numpy as np 
from collections import defaultdict

word_pattern = re.compile(r'\b\w+\b')

emotion_list = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 
            'negative', 'positive', 'sadness', 'surprise', 'trust']
tone_list = ['joking', 'sarcasm', 'serious', 'light_hearted', 
             'genuine', 'negative', 'positive']

def load_json_data(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

def generate_tone_vectors(tone_data):
    """Converts tone json data to a usable dictionary of numpy arrays"""
    tone_vectors = {}
    for tone in tone_list:
        emo_vals = []
        for emotion in emotion_list:
            emo_vals.append(tone_data[tone][emotion])
        tone_vectors[tone] = np.array(emo_vals)
    return tone_vectors

def get_emotion_vector(text, emo_lex):
    """Calculates the emotion vector for the given text"""
    input_words = word_pattern.findall(text.lower())
    total_matched_words = 0
    emotion_dict = defaultdict(float)
    # Tracks emotion frequency in a dictionary
    for word in input_words:
        if word in emo_lex:
            total_matched_words += 1
            for emotion in emotion_list:
                emotion_dict[emotion] += emo_lex[word][emotion]
    # Division by 0 edge case
    if(total_matched_words == 0):
        return np.zeros(len(emotion_list))
    # Converts dictionary to a numpy vector
    emotion_vector = [emotion_dict[emotion] / total_matched_words for emotion in emotion_list]
    return np.array(emotion_vector)

def find_closest_match(emo_vec, tone_vecs):
    lowest_mag = math.inf
    best_tone = ''
    for tone in tone_list:
        curr_vec = tone_vecs[tone]
        vec_diff = np.subtract(curr_vec, emo_vec)
        vec_mag = np.linalg.norm(vec_diff)
        if vec_mag < lowest_mag:
            lowest_mag = vec_mag
            best_tone = tone
    return best_tone
    
emo_lex = load_json_data('emo_lex.json')
tone_data = load_json_data('tone_indicators.json')
text = input("Enter text: ")
emo_vec = get_emotion_vector(text, emo_lex)
tone_vecs = generate_tone_vectors(tone_data)
print(find_closest_match(emo_vec, tone_vecs))