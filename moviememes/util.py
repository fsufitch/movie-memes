import os
from datetime import datetime


class Timer:
    def __init__(self):
        self.start = datetime.utcnow()

    def reset(self):
        self.start = datetime.utcnow()

    def get_seconds(self):
        return (datetime.utcnow() - self.start).total_seconds()

class SnapshotPaths:
    def __init__(self, original_db_url: str):
        self.db_url = original_db_url

    def get(self, movie_id: str, filename: str):
        if '://' in self.db_url:
            parent = self.db_url.rsplit('/', 1)[0]
            return '/'.join([parent, movie_id, filename])
        parent = os.path.dirname(self.db_url)
        return os.path.join(parent, movie_id, filename)
        