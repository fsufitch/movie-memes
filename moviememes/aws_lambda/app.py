import json
from moviememes.aws_lambda.util import Timer
import traceback

from moviememes.aws_lambda.hello import hello_handler
from moviememes.aws_lambda.types import ActionRoutes, ActionHandlerReturn


ACTIONS: ActionRoutes = {
    'hello': hello_handler,
}

def not_found_handler(event, context) -> ActionHandlerReturn: #pylint: disable=unused-argument
    return 404, {}

def create_main_handler():
    hot_timer = Timer()

    def inner(event, context):
        event['hot_timer'] = hot_timer

        action_handler = ACTIONS.get(event.get('action', None), not_found_handler)

        try:
            code, body_data = action_handler(event, context)
        except Exception as exc: # pylint: disable=broad-except
            code = 500
            body_data = {'error': str(exc), 'traceback': traceback.format_exc()}

        return {
            'statusCode': code,
            'body': json.dumps(body_data)
        }
    return inner

main_handler = create_main_handler()
