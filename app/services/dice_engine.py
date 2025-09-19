from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiceEngine:
    seed: int

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def roll(self) -> tuple[int, datetime]:
        value = self._rng.randint(1, 6)
        ts = datetime.utcnow()
        return value, ts

    def reseed(self, seed: int) -> None:
        self.seed = seed
        self._rng.seed(seed)

