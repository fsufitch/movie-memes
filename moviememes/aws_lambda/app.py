import json
import logging
import os
import tempfile
import traceback

import requests
from moviememes.aws_lambda.hello import hello_handler
from moviememes.aws_lambda.snapshots import get_snapshot_handler
from moviememes.aws_lambda.types import ActionHandlerReturn, ActionRoutes
from moviememes.db import get_sessionmaker
from moviememes.util import SnapshotPaths, Timer

ACTIONS: ActionRoutes = {
    'hello': hello_handler,
    'get_snapshot': get_snapshot_handler,
}


def not_found_handler(event, context) -> ActionHandlerReturn:  # pylint: disable=unused-argument
    return 404, {}


def init_function():
    hot_timer = Timer()
    db_sessionmaker = bootstrap_db(os.environ.get('MOVIE_DB_URL'))
    snapshot_paths = SnapshotPaths(os.environ.get('MOVIE_DB_URL'))

    def inner(event, context):
        event['hot_timer'] = hot_timer
        event['dbsession'] = db_sessionmaker()
        event['snapshot_paths'] = snapshot_paths

        action_handler = ACTIONS.get(
            event.get('action', None), not_found_handler)

        try:
            code, body_data = action_handler(event, context)
        except Exception as exc:  # pylint: disable=broad-except
            code = 500
            body_data = {'error': repr(exc), 'traceback': traceback.format_exc()}

        return {
            'statusCode': code,
            'body': json.dumps(body_data)
        }
    return inner


def bootstrap_db(url: str):
    logging.info('Initializing DB from URL: %s', url)
    if not url:
        logging.warning('No URL to bootstrap DB from; using empty DB')
        return get_sessionmaker(None)

    response = requests.get(url, stream=True)

    if response.status_code != requests.codes['ok']:
        raise ValueError(
            f'Non-OK status code trying to look up DB: {response.status_code}')

    _, dbpath = tempfile.mkstemp('_moviedb.sqlite3')
    with open(dbpath, 'wb') as dbfile:
        for byts in response.iter_content(None):
            byts: bytes
            dbfile.write(byts)

    return get_sessionmaker(dbpath)


main_handler = init_function()
