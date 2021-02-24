""" ffmpeg compatibility layer """

import subprocess
import os


def extract_screenshot_plain(input_file: str, timestamp: float, output_file: str):
    """ Extract a plain screenshot from the video file """
    _ensure_parent_dir(output_file)
    subprocess.check_call([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', input_file,
        '-vframes', '1', '-q:v', '2',  # JPEG tweaking?
        '-ss', str(timestamp),
        output_file
    ])


def extract_screenshot_subtitled(input_file: str, timestamp: float, output_file: str, subtitle_file: str):
    """ Extract a screenshot with the subtitle at that time """
    _ensure_parent_dir(output_file)
    subprocess.check_call([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', input_file,
        '-vf', f'subtitles={subtitle_file}',
        '-vframes', '1', '-q:v', '2',  # JPEG tweaking?
        '-ss', str(timestamp),
        output_file
    ])


def extract_clip_subtitled(input_file: str, timestamp: float, duration: int, output_file: str, subtitle_file: str):
    """ Extract and encode a video clip of the given subtitle """
    _ensure_parent_dir(output_file)
    subprocess.check_call([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', input_file,
        '-vf', f'subtitles={subtitle_file}',
        '-ss', str(timestamp), '-t', str(duration),
        output_file
    ])


def _ensure_parent_dir(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
