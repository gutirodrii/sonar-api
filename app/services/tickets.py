from __future__ import annotations

from dataclasses import dataclass


TICKET_TABLE = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 0}


@dataclass
class TicketCalculator:
    def tickets_for_report(self, reported_value: int) -> int:
        return int(TICKET_TABLE.get(reported_value, 0))

