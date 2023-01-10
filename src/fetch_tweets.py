import os
import logging
import pandas as pd
from collections import defaultdict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_tweets_by_username(
    username='', since='1995-10-16', until='1996-08-25', minlikes=0, minretweets=0, minreplies=0
):
    # Search the tweets via twint CLI
    if (len(username) != 0) & (username is not None):
        logger.info(f'Search with {username}')
        os.system(
            f'twint -u {username} '
            f'--min-likes {minlikes} '
            f'--min-retweets {minretweets} '
            f'--min-replies {minreplies} '
            f'--since {since} '
            f'--until {until} '
            f'-o tweets.csv --csv'
        )
    else:
        raise ValueError("Username or search shouldn't be empty!")

    if not os.path.exists('tweets.csv'):
        return {
            'length': 0, 
            'data': []
        }

    # Load from csv file and pre-process
    df = pd.read_csv('tweets.csv', sep='\t')
    os.system('rm -rf tweets.csv')
    df = df[[
        'id', 'conversation_id', 'date', 'time', 'timezone', 'username', 
        'tweet', 'replies_count', 'retweets_count', 'likes_count', 'link'
    ]]

    return df


def get_tweets_by_keyword(
    search='', since='1995-10-16', until='1996-08-25', minlikes=0, minretweets=0, minreplies=0
):
    # Search the tweets via twint CLI
    if (len(search) != 0) & (search is not None):
        logger.info(f'Search with {search}')
        os.system(
            f'twint -s {search} '
            f'--min-likes {minlikes} '
            f'--min-retweets {minretweets} '
            f'--min-replies {minreplies} '
            f'--since {since} '
            f'--until {until} '
            f'-o tweets.csv --csv'
        )
    else:
        raise ValueError("Username or search shouldn't be empty!")

    if not os.path.exists('tweets.csv'):
        return {
            'length': 0, 
            'data': []
        }

    # Load from csv file and pre-process
    df = pd.read_csv('tweets.csv', sep='\t')
    os.system('rm -rf tweets.csv')
    df = df[[
        'id', 'conversation_id', 'date', 'time', 'timezone', 'username', 
        'tweet', 'replies_count', 'retweets_count', 'likes_count', 'link'
    ]]

    return df