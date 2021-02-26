from typing import List, Tuple

def parse_path(path) -> Tuple[str, List[str]]:
    parts = path.lstrip('/').split('/')

    return parts[0], parts[1:]