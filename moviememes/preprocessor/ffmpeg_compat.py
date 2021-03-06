""" ffmpeg compatibility layer """

import logging
import subprocess
import shlex
import os
import tempfile


def extract_all(input_file: str, subtitle_file: str, start_time: float, end_time: float,
                screenshot_plain_output: str, screenshot_subtitled_output: str, clip_subtitled_output: str):
    _ensure_parent_dir(screenshot_plain_output)
    _ensure_parent_dir(screenshot_subtitled_output)
    _ensure_parent_dir(clip_subtitled_output)

    duration = end_time - start_time

    with tempfile.TemporaryDirectory() as tmpdir:
        cropped_subtitle_file = os.path.join(
            tmpdir, os.path.split(subtitle_file)[1])

        cmd1 = [
            'ffmpeg', '-y',
            '-hide_banner', '-loglevel', 'error',
            '-ss', str(start_time), '-t', str(duration), '-i', str(subtitle_file),
            cropped_subtitle_file,
        ]

        logging.debug(shlex.join(cmd1))
        subprocess.check_call(cmd1)

        cmd2 = [
            'ffmpeg', '-y',
            '-hide_banner', '-loglevel', 'error',
            '-an', '-ss', str(start_time), '-t', str(duration),
            '-i', str(input_file),
            '-filter_complex', f'[0:v]split=2[plain1][plain2];'
                               f'[plain2]subtitles={cropped_subtitle_file}'
                               f'[sub1];[sub1]split=2[sub2][sub3]',
            '-map', '[plain1]', '-ss', str(duration / 2), '-frames:v', '1', '-q:v', '2', screenshot_plain_output,
            '-map', '[sub2]', '-ss', str(duration / 2), '-frames:v', '1', '-q:v', '2', screenshot_subtitled_output,
            '-map', '[sub3]', clip_subtitled_output,
        ]

        logging.debug(shlex.join(cmd2))
        subprocess.check_call(cmd2)


def _ensure_parent_dir(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
