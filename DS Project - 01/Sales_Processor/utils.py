import re
from typing import Iterable


def to_snake_case(s: str) -> str:

    s = s.strip()
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def normalize_columns(cols: Iterable[str]):
    return [to_snake_case(c) for c in cols]
