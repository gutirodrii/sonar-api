from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from app.models.schemas import Participant, ReportEvent, RollEvent, Series, Ticket


@dataclass
class InMemoryStore:
    series: Dict[str, Series] = field(default_factory=dict)
    participants: Dict[str, Participant] = field(default_factory=dict)
    last_roll: Dict[str, RollEvent] = field(default_factory=dict)  # session_id -> roll
    reports: Dict[str, ReportEvent] = field(default_factory=dict)  # session_id -> report
    tickets: Dict[str, Ticket] = field(default_factory=dict)  # session_id -> ticket summary latest

    def reset_series(self, series: Series) -> None:
        self.series[series.id] = series

    def get_series(self, series_id: str) -> Optional[Series]:
        return self.series.get(series_id)

    def upsert_participant(self, participant: Participant) -> None:
        self.participants[participant.session_id] = participant

    def get_participant(self, session_id: str) -> Optional[Participant]:
        return self.participants.get(session_id)

    def set_last_roll(self, event: RollEvent) -> None:
        self.last_roll[event.session_id] = event

    def get_last_roll(self, session_id: str) -> Optional[RollEvent]:
        return self.last_roll.get(session_id)

    def set_report(self, event: ReportEvent) -> None:
        self.reports[event.session_id] = event

    def get_report(self, session_id: str) -> Optional[ReportEvent]:
        return self.reports.get(session_id)

    def set_ticket(self, ticket: Ticket) -> None:
        self.tickets[ticket.session_id] = ticket

    def get_ticket(self, session_id: str) -> Optional[Ticket]:
        return self.tickets.get(session_id)

