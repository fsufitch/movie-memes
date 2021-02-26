from datetime import time
from moviememes.db import Snapshot
from moviememes.aws_lambda.types import AWSLambdaContext, ActionHandlerReturn, InputEvent


class GetSnapshotEvent(InputEvent):
    movie_id: str
    timestamp: float


def get_snapshot_handler(event: GetSnapshotEvent, context: AWSLambdaContext) -> ActionHandlerReturn:  # pylint: disable=unused-argument
    movie_id = event['movie_id']
    timestamp = event['timestamp']
    snapshot_paths = event['snapshot_paths']
    db = event['dbsession']

    query = db.query(Snapshot).filter(
        (Snapshot.movie_id == movie_id)
        & (Snapshot.start_seconds <= timestamp)
        & (Snapshot.end_seconds > timestamp))
    query_count = query.count()

    for row in query.all():
        print(row.movie_id, row.start_seconds, row.end_seconds, row.subtitle)

    if not query_count:
        return 404, {}
    if query_count > 1:
        return 500, {'error': f'DB contains multiple snapshots ({query_count}) for this timestamp, WTF?'}

    snapshot = query.one()
    return 200, {
        'start': snapshot.start_seconds,
        'end': snapshot.end_seconds,
        'text': snapshot.subtitle,

        'snapshot_plain': snapshot.screenshot_plain,
        'snapshot_subtitled': snapshot.screenshot_subtitle,
        'clip_subtitled': snapshot.clip_subtitle,
        'urls': {
            'snapshot_plain': snapshot_paths.get(movie_id, snapshot.screenshot_plain),
            'snapshot_subtitled': snapshot_paths.get(movie_id, snapshot.screenshot_subtitle),
            'clip_subtitled': snapshot_paths.get(movie_id, snapshot.clip_subtitle),
        },
    }
