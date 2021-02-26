from datetime import datetime


class Timer:
    def __init__(self):
        self.start = datetime.utcnow()

    def reset(self):
        self.start = datetime.utcnow()

    def get_seconds(self):
        return (datetime.utcnow() - self.start).total_seconds()
