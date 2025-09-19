from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TreatmentArm(str, Enum):
    t25 = "T25"
    t50 = "T50"
    t75 = "T75"


class ReferenceSize(int, Enum):
    n10 = 10
    n100 = 100


class Treatment(BaseModel):
    arm: TreatmentArm
    reference_size: ReferenceSize


class Series(BaseModel):
    id: str
    index: int = Field(..., ge=0)
    started_at: datetime
    rolls_in_series: int = 0
    active: bool = True


class Participant(BaseModel):
    session_id: str
    bracelet_id_hash: Optional[str] = None
    consent_version: str
    consent_accepted_at: datetime
    treatment: Treatment


class RollEvent(BaseModel):
    series_id: str
    session_id: str
    rolled_value: int = Field(..., ge=1, le=6)
    served_at: datetime
    interaction_hash: str


class ReportEvent(BaseModel):
    series_id: str
    session_id: str
    reported_value: int = Field(..., ge=1, le=6)
    received_at: datetime
    accepted: bool
    reason: Optional[str] = None
    tickets_awarded: int = 0


class Ticket(BaseModel):
    session_id: str
    series_id: str
    amount: int = Field(..., ge=0)
    created_at: datetime


class Raffle(BaseModel):
    raffle_id: str
    created_at: datetime
    total_tickets: int
    winner_session_id: Optional[str] = None
    winner_drawn_at: Optional[datetime] = None

