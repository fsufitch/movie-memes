from typing import Any, Callable, Mapping, Tuple, TypedDict

from moviememes.aws_lambda.util import Timer

class InputEvent(TypedDict):
    action: str
    hot_timer: Timer


# See: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
AWSLambdaContext = Any

ActionHandlerReturn = Tuple[int, dict]
ActionHandler = Callable[[InputEvent, dict], ActionHandlerReturn]

ActionRoutes = Mapping[str, Callable[[InputEvent, dict], Tuple[int, dict]]]
