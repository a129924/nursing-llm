from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RawMessageDictSchema:
    role: str
    content: str
