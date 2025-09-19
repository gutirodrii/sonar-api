from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Dict, Optional

from app.models.schemas import Series
from app.storage.memory import InMemoryStore


@dataclass
class SeriesManager:
    store: InMemoryStore
    max_rolls_per_series: int = 500
    norm_window_size: int = 100

    # per-series cache of last values to compute simple norms (e.g., % of 5s)
    last_values: Dict[str, Deque[int]] = None

    def __post_init__(self) -> None:
        if self.last_values is None:
            self.last_values = {}

    def get_active_series(self, series_id: str) -> Series:
        series = self.store.get_series(series_id)
        if not series or not series.active:
            raise ValueError("Serie no activa")
        return series

    def record_roll(self, series_id: str, value: int) -> Series:
        series = self.get_active_series(series_id)
        series.rolls_in_series += 1
        lv = self.last_values.setdefault(series_id, deque(maxlen=self.norm_window_size))
        lv.append(value)
        # rotate automatically when threshold reached
        if series.rolls_in_series >= self.max_rolls_per_series:
            self.rotate_series(series_id)
        return series

    def recent_percentage_of_value(self, series_id: str, value: int) -> float:
        lv = self.last_values.get(series_id)
        if not lv:
            return 0.0
        count = sum(1 for v in lv if v == value)
        return (count / len(lv)) * 100.0

    def rotate_series(self, series_id: Optional[str] = None) -> Series:
        # deactivate old and create new series with incremented index
        old = self.store.get_series(series_id) if series_id else None
        index = (old.index + 1) if old else 1
        new_id = f"series-{index}"
        new_series = Series(id=new_id, index=index, started_at=datetime.utcnow(), rolls_in_series=0, active=True)
        if old:
            old.active = False
        self.store.reset_series(new_series)
        # reset window for new series
        self.last_values[new_id] = deque(maxlen=self.norm_window_size)
        return new_series

