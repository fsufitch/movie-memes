""" This is the main "brains" of the program """

from typing import List

from moviememes.preprocessor.structs import MovieInput, SubtitleWorkItem
from moviememes.preprocessor.subtitle_compat import parse_subtitles


def create_work_items(movie_input: MovieInput, image_suffix: str, video_suffix: str) -> List[SubtitleWorkItem]:
    """ Create the concrete work items related to the given movie input """
    subs = parse_subtitles(movie_input.sub_file)

    return [
        SubtitleWorkItem(movie_input, sub,
                 f'screenshot_plain_{sub.start}-{sub.end}{image_suffix}',
                 f'screenshot_subtitle_{sub.start}-{sub.end}{image_suffix}',
                 f'clip_subtitle_{sub.start}-{sub.end}{video_suffix}',
                 ) for sub in subs
    ]
