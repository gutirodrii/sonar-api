from __future__ import annotations

from dataclasses import dataclass

from app.services.dice_engine import DiceEngine
from app.services.series_manager import SeriesManager
from app.services.tickets import TicketCalculator
from app.services.treatment_assigner import StratifiedRandomAssigner
from app.storage.memory import InMemoryStore


@dataclass
class Container:
    store: InMemoryStore
    dice: DiceEngine
    assigner: StratifiedRandomAssigner
    tickets: TicketCalculator
    series: SeriesManager


def build_container(seed: int = 42) -> Container:
    store = InMemoryStore()
    dice = DiceEngine(seed=seed)
    assigner = StratifiedRandomAssigner(seed=seed)
    tickets = TicketCalculator()
    series = SeriesManager(store=store)
    return Container(store=store, dice=dice, assigner=assigner, tickets=tickets, series=series)


CONTAINER = build_container()

