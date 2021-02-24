""" Compatibility with, and abstraction from subtitle files """
import datetime
from typing import List

import chardet
from pysubparser import parser as subparser

from moviememes.preprocessor.structs import Subtitle


def parse_subtitles(subtitle_file: str) -> List[Subtitle]:
    """ Return a list of Subtitle objects derived from the given file """
    with open(subtitle_file, 'rb') as f:
        chardet_result = chardet.detect(f.read())

    return [
        Subtitle(s.index, s.text, _to_sec(s.start), _to_sec(s.end))
        for s in subparser.parse(subtitle_file, encoding=chardet_result['encoding'])
    ]


def _to_sec(time: datetime.time) -> float:
    """ Convert a datetime.time into a second delta from 00:00:00 """
    return time.second + 60 * (time.minute + 60 * time.hour) + time.microsecond / 1000000
