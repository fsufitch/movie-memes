from sqlalchemy.sql.expression import true
from urllib.parse import parse_qs

from moviememes.aws_lambda.types import (ActionHandlerReturn,
                                         AWSAPIGatewayEvent, AWSLambdaContext)
from moviememes.db import Snapshot


def search_handler(event: AWSAPIGatewayEvent, context: AWSLambdaContext) -> ActionHandlerReturn:  # pylint: disable=unused-argument
    snapshot_paths = event['snapshot_paths']
    dbsession = event['dbsession']

    params = parse_qs(event['rawQueryString'].lstrip('?'))
    search_query = (params.get('q') or [''])[0].strip()

    if not search_query or len(search_query) < 3:
        return 400, {'error': 'required param, specified once, of length at least 3: q'}

    movie_ids = params.get('movie', [])[:10]

    movie_condition = Snapshot.movie_id.in_(movie_ids) if movie_ids else true()

    results = dbsession.query(Snapshot).filter(
        movie_condition &
        Snapshot.subtitle.ilike(f'%{search_query}%')
    ).all()

    response = [{
        "id": snapshot.id,
        "movie_id": snapshot.movie_id,
        "start": snapshot.start_seconds,
        "end": snapshot.end_seconds,
        "subtitle": snapshot.subtitle,
        'snapshot_plain': snapshot.screenshot_plain,
        'snapshot_subtitled': snapshot.screenshot_subtitle,
        'clip_subtitled': snapshot.clip_subtitle,
        'urls': {
            'snapshot_plain': snapshot_paths.get(snapshot.movie_id, snapshot.screenshot_plain),
            'snapshot_subtitled': snapshot_paths.get(snapshot.movie_id, snapshot.screenshot_subtitle),
            'clip_subtitled': snapshot_paths.get(snapshot.movie_id, snapshot.clip_subtitle),
        },
    } for snapshot in results]

    return 200, response
