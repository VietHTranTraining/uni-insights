import document_utils

TWITTER_FILE = './traindata/twitter.txt'
SAVE_FILE = './traindata/twitter.json'

usernames, current_university = {}, 'psu'
with open(TWITTER_FILE) as f:
    for line in f:
        if line == '\n' or line == '':
            continue
        content = line[:-1]
        if content[0] != '@':
            usernames[content] = []
            current_university = content
        else:
            usernames[current_university].append(content[1:])
document_utils.write_json(usernames, SAVE_FILE)
