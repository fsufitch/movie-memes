import logging
from typing import Callable

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

_Base = declarative_base()


class Movie(_Base):
    __tablename__ = 'movies'
    id = Column(String, primary_key=True)
    title = Column(String)

    snapshots = relationship('Snapshot', order_by='Snapshot.start_seconds', back_populates='movie')
    attributions = relationship('Attribution', back_populates='movie', cascade='all, delete, delete-orphan')


class Attribution(_Base):
    __tablename__ = 'attributions'
    id = Column(Integer, primary_key=True)
    movie_id = Column(String, ForeignKey('movies.id'))
    text = Column(String)
    url = Column(String)

    movie = relationship('Movie', back_populates='attributions')


class Snapshot(_Base):
    __tablename__ = 'snapshots'

    id = Column(Integer, primary_key=True)
    movie_id = Column(String, ForeignKey('movies.id'))
    start_seconds = Column(Integer, nullable=False)
    end_seconds = Column(Integer)

    subtitle = Column(String, nullable=False)

    screenshot_plain = Column(String)
    screenshot_subtitle = Column(String)
    clip_subtitle = Column(String)

    movie = relationship('Movie', back_populates='snapshots')


def get_sessionmaker(path: str, echo: bool=False, initdb=True) -> Callable[[], Session]:
    print(path, echo, initdb)
    if path:
        engine = create_engine(f'sqlite:///{path}', echo=echo)
    else:
        logging.warn('no engine path specified, using in-memory SQLite engine and forcing echo on')
        engine = create_engine('sqlite:///:memory:', echo=True)

    if initdb:
        logging.info('ensuring database is initialized')
        _Base.metadata.create_all(engine)

    sm = sessionmaker(bind=engine)
    return sm

