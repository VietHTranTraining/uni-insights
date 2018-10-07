import document_utils
import twitter_utils
import ibm_utils 
import watson_developer_cloud
from review_analysis import normalize_data
import os

TEST_DATA = './traindata'
TWITTER_USERNAMES_FILE = './traindata/twitter.json'
SAVE_FILE_NAME = 'trained_memory.json'
SAVE_DIRECTORY_FILE_NAME = 'id_name.json'

# Get trainable data
universities = document_utils.get_all_dirs(TEST_DATA)

id_name = {}
trained_data, trained_data_tw = {}, {}
print 'Analyzing essays...'
for university in universities:
    university_name = university.split('/')[-1]
    print university_name
    essays = document_utils.get_all_files(university)
    aggr_data = {
        'needs': {},        
        'consumption_preferences': {},        
        'values': {},        
        'personality': {},        
    }
    for essay in essays:
        essay_ext = essay.split('.')[-1]
        if essay_ext != 'txt':
            os.remove(essay)
            continue
        essay_data = '.' + ''.join(essay.split('.')[:-1]) + '.json'
        essay_data_normalized = '.' + ''.join(essay.split('.')[:-1]) + '_normalized.json'
        print essay
        personality_data = ibm_utils.anaylyze_user(essay) 
        personality_data_normalized = normalize_data(personality_data) 
        document_utils.write_json(personality_data, essay_data)
        document_utils.write_json(personality_data_normalized, essay_data_normalized)
        for key in personality_data_normalized:
            facets = personality_data_normalized[key]
            for facet in facets:
                if facet not in aggr_data[key]:
                    aggr_data[key][facet] = {
                        'name': facets[facet]['name']
                    }
                    id_name[facet] = facets[facet]['name']
                    if 'raw_score' in facets[facet]:
                        aggr_data[key][facet] = {
                            'raw_score': [],
                            'percentile': []
                        }
                    else:
                        aggr_data[key][facet] = {
                            'score': [],
                        }
                if 'raw_score' in facets[facet]:
                    aggr_data[key][facet]['raw_score'].append(facets[facet]['raw_score'])
                    aggr_data[key][facet]['percentile'].append(facets[facet]['percentile'])
                else:
                    aggr_data[key][facet]['score'].append(facets[facet]['score'])
    new_aggr_data = dict(aggr_data)
    for key in aggr_data:
        new_aggr_data[key] = dict(aggr_data[key])
        for facet in aggr_data[key]:
            new_aggr_data[key][facet] = dict(aggr_data[key][facet])
            facet_data = aggr_data[key][facet]
            if 'raw_score' in facet_data:
                mean = sum(facet_data['percentile'])/len(facet_data['percentile'])
                is_correlated = True
                for p in facet_data['percentile']:
                    if abs(mean - p) > 0.30:
                        print 'Not correlated: ' + facet
                        new_aggr_data[key].pop(facet, None)
                        is_correlated = False
                        break
                if not is_correlated:
                    continue
                new_aggr_data[key][facet]['percentile'] = mean
                mean = sum(facet_data['raw_score'])/len(facet_data['raw_score'])
                for rs in facet_data['raw_score']:
                    if abs(mean - rs) > 0.30:
                        print 'Not correlated: ' + facet
                        new_aggr_data[key].pop(facet, None)
                        is_correlated = False
                        break
                if not is_correlated:
                    continue
                new_aggr_data[key][facet]['raw_score'] = mean
            else:
                std_score = facet_data['score'][0]
                for score in facet_data['score']:
                    if score != std_score:
                        print 'Not correlated: ' + facet
                        new_aggr_data[key].pop(facet, None)
                        break
                if facet in new_aggr_data[key]:
                    new_aggr_data[key][facet] = std_score
    if not new_aggr_data[key]:
        new_aggr_data.pop(key, None)
    trained_data[university_name] = new_aggr_data
print 'Analyzing essays complete!'
print 'Analyzing users\' tweets...'
TWITTER_USERNAMES = document_utils.read_json(TWITTER_USERNAMES_FILE)
for university in TWITTER_USERNAMES:
    print university
    aggr_data = {
        'needs': {},        
        'consumption_preferences': {},        
        'values': {},        
        'personality': {},
    }
    for username in TWITTER_USERNAMES[university]:
        print username
        try:
            tweets = twitter_utils.get_user_tweets(username)
        except Exception:
            continue
        tweet_tmp_file = './user_tweets.tmp'
        document_utils.write_json(tweets, tweet_tmp_file)
        try:
            personality_data = ibm_utils.anaylyze_user_json(tweet_tmp_file) 
        except watson_developer_cloud.watson_service.WatsonApiException:
            continue
        personality_data_normalized = normalize_data(personality_data) 
        os.remove(tweet_tmp_file)
        for key in personality_data_normalized:
            facets = personality_data_normalized[key]
            for facet in facets:
                if facet not in aggr_data[key]:
                    aggr_data[key][facet] = {
                        'name': facets[facet]['name']
                    }
                    if 'raw_score' in facets[facet]:
                        aggr_data[key][facet] = {
                            'raw_score': [],
                            'percentile': []
                        }
                    else:
                        aggr_data[key][facet] = {
                            'score': [],
                        }
                if 'raw_score' in facets[facet]:
                    aggr_data[key][facet]['raw_score'].append(facets[facet]['raw_score'])
                    aggr_data[key][facet]['percentile'].append(facets[facet]['percentile'])
                else:
                    aggr_data[key][facet]['score'].append(facets[facet]['score'])
    new_aggr_data = dict(aggr_data)
    for key in aggr_data:
        new_aggr_data[key] = dict(aggr_data[key])
        for facet in aggr_data[key]:
            new_aggr_data[key][facet] = dict(aggr_data[key][facet])
            facet_data = aggr_data[key][facet]
            if 'raw_score' in facet_data:
                mean = sum(facet_data['percentile'])/len(facet_data['percentile'])
                is_correlated = True
                for p in facet_data['percentile']:
                    if abs(mean - p) > 0.40:
                        print 'Not correlated: ' + facet
                        new_aggr_data[key].pop(facet, None)
                        is_correlated = False
                        break
                if not is_correlated:
                    continue
                new_aggr_data[key][facet]['percentile'] = mean
                mean = sum(facet_data['raw_score'])/len(facet_data['raw_score'])
                for rs in facet_data['raw_score']:
                    if abs(mean - rs) > 0.40:
                        print 'Not correlated: ' + facet
                        new_aggr_data[key].pop(facet, None)
                        is_correlated = False
                        break
                if not is_correlated:
                    continue
                new_aggr_data[key][facet]['raw_score'] = mean
            else:
                std_score = facet_data['score'][0]
                for score in facet_data['score']:
                    if score != std_score:
                        print 'Not correlated: ' + facet
                        new_aggr_data[key].pop(facet, None)
                        break
                if facet in new_aggr_data[key]:
                    new_aggr_data[key][facet] = std_score
    if not new_aggr_data[key]:
        new_aggr_data.pop(key, None)
    trained_data_tw[university] = new_aggr_data

print 'Analyzing users\' tweets complete!'
print 'Saving training data...'
document_utils.write_json({'essay': trained_data, 'twitter': trained_data_tw}, SAVE_FILE_NAME)
document_utils.write_json(id_name, SAVE_DIRECTORY_FILE_NAME)
print 'Training data is successfully saved at ' + SAVE_FILE_NAME
