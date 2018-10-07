import twitter
import json

CONSUMER_KEY = 'SrkVbOWYzdNPDrbYG2ePjnxeE'
CONSUMER_SECRET = 'Jtubgd25vH40sddqxh2ri1uiYHU8nt2FJUEPFhjbuRIr2EiH47'
ACCESS_TOKEN = '895119289358962689-J9KrJjSLQJQpOB1QVnHb8RY8ZO0EuO2'
ACCESS_TOKEN_SECRET = '6IDk7Cz8Tvbzpd2pHdveJgsVZjGxIn5lfNJXPGAiYR87G'

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

def get_user_tweets(username):
    results = api.GetUserTimeline(screen_name=username, count=1000)
    extract_data = {'contentItems': []}
    for r in results:
        result = json.loads(str(r))
        data = {
            'content': result['text'].encode('ascii', 'ignore'),
            'contenttype': 'text/plain',
        }
        #    'language': result['lang'],
        extract_data['contentItems'].append(data)
    return extract_data

