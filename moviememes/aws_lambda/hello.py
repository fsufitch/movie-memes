from moviememes.aws_lambda.types import ActionHandlerReturn, InputEvent, AWSLambdaContext


def hello_handler(event: InputEvent, context: AWSLambdaContext) -> ActionHandlerReturn:  # pylint: disable=unused-argument
    return 200, {
        'ok': True,
        'context': {
            'function_name': context.function_name,
            'function_version': context.function_version,
            'hot_time': event['hot_timer'].get_seconds(),
        },
    }
