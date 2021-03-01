from typing import Any, Callable, Mapping, Tuple, TypedDict

from sqlalchemy.orm.session import Session

from moviememes.util import SnapshotPaths

class _AWSAPIGatewayEvent_RequestContext_HTTP(TypedDict): #pylint: disable=invalid-name
    """ https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html """
    method: str
    path: str
    protocol: str
    sourceIp: str
    userAgent: str

class _AWSAPIGatewayEvent_RequestContext(TypedDict): #pylint: disable=invalid-name
    """ https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html """
    rawPath: str
    time: str
    timeEpoch: float
    http: _AWSAPIGatewayEvent_RequestContext_HTTP

class AWSAPIGatewayEvent(TypedDict):
    """ https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html """
    rawPath: str
    rawQueryString: str
    headers: Mapping[str, str]
    queryStringParameters: Mapping[str, str]
    requestContext: _AWSAPIGatewayEvent_RequestContext
    body: str
    pathParameters: Mapping[str, str]
    isBase64Encoded: bool
    stageVariables: Mapping[str, str]

    # initialized dynamically
    action: str
    path_extra: str
    dbsession: Session
    snapshot_paths: SnapshotPaths


# See: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
AWSLambdaContext = Any

ActionHandlerReturn = Tuple[int, dict]
ActionHandler = Callable[[AWSAPIGatewayEvent, dict], ActionHandlerReturn]

ActionRoutes = Mapping[str, ActionHandler]
