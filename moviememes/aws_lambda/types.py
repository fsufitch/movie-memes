from typing import Any, Callable, Mapping, Tuple, TypedDict

from sqlalchemy.orm.session import Session

from moviememes.util import SnapshotPaths, Timer

class InputEvent(TypedDict):
    action: str
    hot_timer: Timer
    dbsession: Session
    snapshot_paths: SnapshotPaths


# See: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
AWSLambdaContext = Any

ActionHandlerReturn = Tuple[int, dict]
ActionHandler = Callable[[InputEvent, dict], ActionHandlerReturn]

ActionRoutes = Mapping[str, Callable[[InputEvent, dict], Tuple[int, dict]]]
