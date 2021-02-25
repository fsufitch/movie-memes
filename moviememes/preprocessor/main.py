""" Main runnable file for running the movie memes preprocessor """
import argparse
import logging
import os
import sys

import tqdm
import yaml

from moviememes.db import get_sessionmaker, Movie, Attribution, Snapshot
from moviememes.preprocessor.processing import create_work_items
from moviememes.preprocessor.structs import MovieInput, ProcessConfiguration
from moviememes.preprocessor.ffmpeg_compat import extract_all

IMAGE_SUFFIX = '.jpg'
VIDEO_SUFFIX = '.mp4'


def main():
    """ Main """
    logging.basicConfig()
    config = configure()

    session = get_sessionmaker(
        os.path.join(config.output_dir, config.sqlite_filename),
        echo=True,
    )()

    for movie_input in config.movie_inputs:
        query = session.query(Movie).filter(Movie.id==movie_input.movie_id)
        if query.count():
            if not config.clear:
                continue
            session.delete(query.one())

        work_items = create_work_items(movie_input, IMAGE_SUFFIX, VIDEO_SUFFIX)

        movie = Movie(id=movie_input.movie_id, title=movie_input.movie_title)
        if movie_input.sub_attribution_text or movie_input.sub_attribution_url:
            movie.attributions.append(Attribution(
                text=movie_input.sub_attribution_text, 
                url=movie_input.sub_attribution_url,
            ))
        
        for item in tqdm.tqdm(work_items, desc=movie_input.movie_id):
            extract_all(
                movie_input.video_file,
                movie_input.sub_file,
                item.subtitle.start,
                item.subtitle.end,
                os.path.join(config.output_dir, movie_input.movie_id, item.screenshot_plain),
                os.path.join(config.output_dir, movie_input.movie_id, item.screenshot_subtitle),
                os.path.join(config.output_dir, movie_input.movie_id, item.clip_subtitle),             
            )

            movie.snapshots.append(Snapshot(
                start_seconds=item.subtitle.start,
                end_seconds=item.subtitle.end,
                subtitle=item.subtitle.text,
                screenshot_plain=item.screenshot_plain,
                screenshot_subtitle=item.screenshot_subtitle,
                clip_subtitle=item.clip_subtitle,
            ))

    session.add(movie)
    session.commit()
    session.close()


def configure() -> ProcessConfiguration:
    """ Parse and make sense of the process's configuration """
    parser = argparse.ArgumentParser(
        description='Process movies and subtitles into scene captures; '
                    'create a scenes.sqlite3 indexing the files/lines')
    parser.add_argument('config_yaml', type=str, 
        help='a YAML file including configuration of the process; see samples/config.yaml')
    args = parser.parse_args()

    with open(args.config_yaml) as f:
        config_data = yaml.load(f, Loader=yaml.SafeLoader)
    config_yaml_dir = os.path.dirname(args.config_yaml)

    return ProcessConfiguration(
        output_dir=_resolve_relative_path(
            config_yaml_dir, config_data['output_dir']),
        clear=config_data['clear_output'],
        sqlite_filename=config_data['sqlite_filename'],
        movie_inputs=[
            MovieInput(
                movie_id=movie_id,
                movie_title=data['title'],
                video_file=_resolve_relative_path(
                    config_yaml_dir, data['video']),
                sub_file=_resolve_relative_path(
                    config_yaml_dir, data['subtitles']),
                sub_attribution_text=data.get('subtitle_attribution_text', ''),
                sub_attribution_url=data.get('subtitle_attribution_url', ''),
            )
            for (movie_id, data) in config_data['movies'].items()]
    )


def _resolve_relative_path(from_path: str, to_path: str) -> str:
    if os.path.isabs(to_path):
        return to_path

    return os.path.realpath(
        os.path.join(from_path, to_path),
    )


def movie_input_parser(movie_thruple: str) -> MovieInput:
    """ Validate and parse a movie input thruple from the CLI """
    parts = movie_thruple.split(':')
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            f'invalid movie thruple does not have 3 parts: {movie_thruple}')
    movie, video_file, sub_file = parts
    if not movie:
        raise argparse.ArgumentTypeError(
            f'no movie ID found: {movie_thruple}')
    if not video_file:
        raise argparse.ArgumentTypeError(
            f'no video file path found: {movie_thruple}')
    if not sub_file:
        raise argparse.ArgumentTypeError(
            f'no subtitle file path found: {movie_thruple}')
    return MovieInput(movie, video_file, sub_file)


if __name__ == '__main__':
    main()
