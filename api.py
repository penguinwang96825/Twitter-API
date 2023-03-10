import os
import logging
import typing as tp
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(os.environ["PATH"])
app = FastAPI()


class TweetItem(BaseModel):

    username: tp.Union[str, None]
    search: tp.Union[str, None]
    since: str = "2022-08-25"
    until: str = "2022-09-14"
    minlikes: int = 0
    minretweets: int = 0
    minreplies: int = 0


@app.get("/")
def root():
    return {
        "info": {
            "title": "TwitterAPI", 
            "version": "2022.12.29"
        }
    }


@app.post("/twitter-api/v1/tweets/")
async def get_tweets(item: TweetItem):
    os.system("echo $PATH")
    return get_tweets_(
        username=item.username, 
        search=item.search, 
        since=item.since, 
        until=item.until, 
        minlikes=item.minlikes, 
        minretweets=item.minretweets, 
        minreplies=item.minreplies
    )


def get_tweets_(
    username='', 
    search='', 
    since='2022-08-25', 
    until='2022-09-14', 
    minlikes=0, 
    minretweets=0, 
    minreplies=0
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
    elif (len(search) != 0) & (search is not None):
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
        'id', 'conversation_id', 'date', 'time', 'timezone', 
        'tweet', 'replies_count', 'retweets_count', 'likes_count', 'link'
    ]]

    # Convert to JSON format
    data = defaultdict(list)
    data['length'] = len(df)
    for idx, row in df.iterrows():
        data['data'].append(dict(row))

    return data

