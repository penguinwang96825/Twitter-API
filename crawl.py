import os
import logging
import datetime
import typing as tp
import pandas as pd
from collections import defaultdict
from peewee import (
    SqliteDatabase, Model, CharField, ForeignKeyField, 
    IntegerField, TextField, DateField, TimeField, BooleanField
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(os.environ["PATH"])
db = SqliteDatabase('twitter.db')


class DatabaseBaseModel(Model):

    class Meta:

        database = db


class User(DatabaseBaseModel):

    username = CharField(unique=True)


class Tweet(DatabaseBaseModel):

    id = IntegerField(unique=True)
    conversation_id = IntegerField()
    date = DateField()
    time = TimeField()
    timezone = TextField()
    username = ForeignKeyField(User, backref='tweets')
    tweet = TextField()
    replies_count = IntegerField()
    retweets_count = IntegerField()
    likes_count = IntegerField()
    link = TextField()


def get_tweets(
    username: tp.Union[str, None], 
    search: tp.Union[str, None], 
    since: str = '2022-08-25', 
    until: str = '2022-09-14', 
    minlikes: int = 0, 
    minretweets: int = 0, 
    minreplies: int = 0
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
        'id', 'conversation_id', 'date', 'time', 'timezone', 'username', 
        'tweet', 'replies_count', 'retweets_count', 'likes_count', 'link'
    ]]

    # Convert to JSON format
    data = defaultdict(list)
    data['length'] = len(df)
    for idx, row in df.iterrows():
        data['data'].append(dict(row))

    return data


def main():
    db.connect()
    db.create_tables([User, Tweet])

    response = get_tweets(
        username='Bitcoin', 
        search=None, 
        since='2022-08-25', 
        until='2022-09-14', 
        minlikes=100, 
        minretweets=0, 
        minreplies=0
    )
    df = pd.DataFrame(response['data'])
    print(df)

    user = User.get_or_create(username='Bitcoin')
    for idx, row in df.iterrows():
        Tweet.get_or_create(
            id=row['id'], 
            conversation_id=row['conversation_id'], 
            date=row['date'], 
            time=row['time'], 
            timezone=row['timezone'], 
            username=row['username'], 
            tweet=row['tweet'], 
            replies_count=row['replies_count'], 
            retweets_count=row['retweets_count'], 
            likes_count=row['likes_count'], 
            link=row['link']
        )

    # print(User.get(User.username == 'Bitcoin'))
    for row in Tweet.select().dicts():
        print(row)


if __name__ == '__main__':
    main()