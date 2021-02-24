""" This file contains "container" dataclasses used for organizing the program's data """
from typing import List
from dataclasses import dataclass

@dataclass
class MovieInput:
    """ MovieInput is one of the movie specs given by the CLI user """
    movie_id: str
    movie_title: str
    video_file: str
    sub_file: str
    sub_attribution_text: str
    sub_attribution_url: str

@dataclass
class Subtitle:
    """ The bare metadata about a subtitle"""
    index: int
    text: str
    start: float
    end: float


@dataclass
class SubtitleWorkItem:
    """ WorkItem represents a chunk of work that needs to be done for a movie+subtitle pair """
    movie_input: MovieInput
    subtitle: Subtitle
    screenshot_plain: str
    screenshot_subtitle: str
    clip_subtitle: str

    @property
    def middle_timestamp(self):
        """ return the middle of the timestamp for a (hopefully) good screenshot """
        return (self.subtitle.start + self.subtitle.end) / 2

    @property
    def duration(self):
        """ return how long this subtitle clip lasts """
        return self.subtitle.end - self.subtitle.start

@dataclass
class ProcessConfiguration:
    """ Stores the configured runtime variables for this process """
    movie_inputs: List[MovieInput]
    output_dir: str
    clear: bool
    sqlite_filename: str
