import re


def preprocess(tweet):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    emoticon_list = [
        ':\)', ':\)\)', ':o', '=D', ':P', 'xD', '\^\^', ':\(', 
        ':\(\(', 'T\.T', ':<', '>\.<', ':D', '\;\)', '\(:', '\):'
    ]
    contraction_patterns = [
        (r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'[Ii]\'m', 'I am'), (r'ain\'t', 'is not'), 
        (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'), (r'(\w+)\'ve', '\g<1> have'), 
        (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), 
        (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not')
    ]

    tweet = re.sub('\‘', '\'', tweet)
    tweet = re.sub('\’', '\'', tweet)
    tweet = re.sub('\“', '\"', tweet)
    tweet = re.sub('\”', '\"', tweet)
    tweet = re.sub('&lt;', '<', tweet)
    tweet = re.sub('&gt;', '>', tweet)
    tweet = re.sub('&nbsp;', '', tweet)
    tweet = re.sub('&amp;', r'&', tweet)
    tweet = re.sub('&quot;', '\"', tweet)
    for pattern, repl in [(re.compile(regex), repl) for (regex, repl) in contraction_patterns]:
        tweet, _ = re.subn(pattern, repl, tweet)
    tweet = re.sub('@[^\s]+', ' [USER] ', tweet)
    tweet = re.sub(emoji_pattern, ' [EMOJI] ', tweet)
    tweet = re.sub(r'#([^\s]+)', ' [HASHTAG] ', tweet)
    tweet = re.sub(r'(\d+(\.\d+)?%)', ' [PERCENTAGE] ', tweet)
    tweet = re.sub(r'[\$\£\€\¥\₩\฿\₣]+?(\d+([,\.\d]+)?)([BKMTZbkmtz])?', ' [MONEY] ', tweet)
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' [URL] ', tweet)
    tweet = re.sub(r'|'.join(emoticon_list), ' [EMOTICON] ', tweet)
    tweet = re.sub(' +', ' ', tweet)
    tweet = tweet.strip()

    return tweet