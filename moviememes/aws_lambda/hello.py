import os

from moviememes.db import Snapshot
from moviememes.aws_lambda.types import ActionHandlerReturn, InputEvent, AWSLambdaContext


def hello_handler(event: InputEvent, context: AWSLambdaContext) -> ActionHandlerReturn:
    session = event['dbsession']
    snapshot_count = session.query(Snapshot).count()

    return 200, {
        'ok': True,
        'snapshot_count': snapshot_count,
        'function_name': context.function_name,
        'function_version': context.function_version,
        'hot_time': event['hot_timer'].get_seconds(),
        'env': { k:v for k,v in os.environ.items() }
    }
