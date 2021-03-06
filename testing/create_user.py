import click
import pymongo
import hashlib
import datetime

"""
Would be great if somebody could tell me whether using the requests library to create the user followed by using
pymongo to change the story_id and score would be better than validating input again here.
"""


URI = 'mongodb+srv://admin:pussydestroyer69@cluster0-mver3.mongodb.net/techflix?retryWrites=true&w=majority'
db = pymongo.MongoClient(URI)['techflix']


@click.command()
@click.argument('username')
@click.option('--password', default=None, help='Password, same as username if not mentioned')
@click.option('--s_id', prompt='Story id', help='Story id of the node you want to be at.')
@click.option('--score', default=13, help='Initial score')
def create_user(username, password, s_id, score):
    """CLI tool to create a user at any story_id, with any number of points"""
    if password is None:
        password = username

    # # Why not do it before password = username ? Well, that would cause confusion on the user's end as the
    # # password they entered when registering won't be accepted at login as passwords do not have a case restriction.
    username = username.lower()

    if not (username and password):
        raise click.BadParameter("Invalid username or password")

    if db.users.find_one({'username': username}):
        raise click.BadParameter("Username already exists")

    db.users.insert_one({
        'email': 'testing@thapar.edu',
        'username': username,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'score': score,
        'time': datetime.datetime.utcnow(),
        'story_id': s_id,
        'answered': False,
        'end': False,
    })


if __name__ == '__main__':
    create_user()
