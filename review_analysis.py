import document_utils
import ibm_utils
import twitter_utils
import json
import os

TRAINED_MEMORY_FILE = './trained_memory.json'
TRAINED_DATA = None

def normalize_data(data):
    normalize_data = {
        'needs': {},        
        'consumption_preferences': {},        
        'values': {},        
        'personality': {},        
    }
    if 'needs' in data:
        needs = data['needs']
        for need in needs:
            normalize_data['needs'][need['trait_id']] = {
                'name': need['name'],
                'percentile': need['percentile'],
                'raw_score': need['raw_score'],
            }
    if 'consumption_preferences' in data:
        consumption_preferences = data['consumption_preferences']
        for consumption_preference in consumption_preferences:
            preferences = consumption_preference['consumption_preferences']
            for preference in preferences:
                normalize_data['consumption_preferences'][preference['consumption_preference_id']] = {
                    'name': preference['name'],       
                    'score': preference['score'],       
                }
    if 'values' in data:
        values = data['values']
        for value in values:
            normalize_data['values'][value['trait_id']] = {
                'name': value['name'],
                'percentile': value['percentile'],
                'raw_score': value['raw_score'],
            }
    if 'personality' in data:
        personalities = data['personality']
        for personality in personalities:
            normalize_data['personality'][personality['trait_id']] = {
                'name': personality['name'],       
                'percentile': personality['percentile'],       
                'raw_score': personality['raw_score'],       
            }
            if 'children' in personality:
                children = personality['children']
                for child in children:
                    normalize_data['personality'][child['trait_id']] = {
                        'name': child['name'],       
                        'percentile': child['percentile'],       
                        'raw_score': child['raw_score'],       
                    }
    return normalize_data

def categorize_score(score):
    if score <= 0.25:
        return 'Low'
    elif score <= 0.5:
        return 'Medium Low'
    elif score <= 0.75:
        return 'Medium High'
    else:
        return 'High'

def analyze_essay(essay, university):
    global TRAINED_DATA
    if TRAINED_DATA is None:
        TRAINED_DATA = document_utils.read_json(TRAINED_MEMORY_FILE)
    essay_analysis = normalize_data(ibm_utils.anaylyze_user_text(essay))
    university_data = TRAINED_DATA['essay'][university]
    counter, match_counter, message = 0, 0, {}
    for key in university_data:
        if key not in message:
            message[key] = {}
        for facet in university_data[key]:
            if facet not in message[key]:
                message[key][facet] = {}
            counter += 1
            if isinstance(university_data[key][facet],float):
                message[key][facet] = {}
                if essay_analysis[key][facet]['score'] != university_data[key][facet]:
                    message[key][facet] = 'No'
                else:
                    message[key][facet] = 'Yes'
                    match_counter += 1
            elif 'raw_score' in university_data[key][facet]:
                university_score = university_data[key][facet]['raw_score']
                essay_score = essay_analysis[key][facet]['raw_score']
                message[key][facet][university] = categorize_score(university_score)
                message[key][facet]['user'] = categorize_score(essay_score)
                if message[key][facet][university] == message[key][facet]['user']:
                    match_counter += 1

    match_score = (match_counter * 1.0) / counter
    return match_score, message

def analyze_twitter(username, university):
    global TRAINED_DATA
    if TRAINED_DATA is None:
        TRAINED_DATA = document_utils.read_json(TRAINED_MEMORY_FILE)
    try:
        tweets = twitter_utils.get_user_tweets(username)
    except Exception as ex:
        return -1, {'error': str(ex)}
    tweet_tmp_file = './user_tweets.tmp'
    document_utils.write_json(tweets, tweet_tmp_file)
    try:
        twitter_analysis = normalize_data(ibm_utils.anaylyze_user_json(tweet_tmp_file))
    except Exception as ex:
        return -1, {'error': str(ex)}
    #os.remove(tweet_tmp_file)
    university_data = TRAINED_DATA['twitter'][university]
    counter, match_counter, message = 0, 0, {}
    for key in university_data:
        if key not in message:
            message[key] = {}
        for facet in university_data[key]:
            if facet not in message[key]:
                message[key][facet] = {}
            counter += 1
            if isinstance(university_data[key][facet],float):
                message[key][facet] = {}
                if twitter_analysis[key][facet]['score'] != university_data[key][facet]:
                    message[key][facet] = 'No'
                else:
                    message[key][facet] = 'Yes'
                    match_counter += 1
            elif 'raw_score' in university_data[key][facet]:
                university_score = university_data[key][facet]['raw_score']
                essay_score = twitter_analysis[key][facet]['raw_score']
                message[key][facet][university] = categorize_score(university_score)
                message[key][facet]['user'] = categorize_score(essay_score)
                if message[key][facet][university] == message[key][facet]['user']:
                    match_counter += 1

    match_score = (match_counter * 1.0) / counter
    return match_score, message
