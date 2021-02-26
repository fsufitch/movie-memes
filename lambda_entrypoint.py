# Need this file because Lambda does not like executing an app/function file nested in a module dir
from moviememes.aws_lambda.app import main_handler #pylint: disable=unused-import
