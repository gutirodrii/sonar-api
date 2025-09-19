from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    Participant,
    ReportEvent,
    RollEvent,
    Series,
    Treatment,
)
from app.deps.container import CONTAINER
from app.services.treatment_assigner import compute_normative_message
from app.security.audit import audit_event


public_router = APIRouter()

STORE = CONTAINER.store
DICE = CONTAINER.dice
ASSIGNER = CONTAINER.assigner
TICKETS = CONTAINER.tickets
SERIES = CONTAINER.series

# bootstrap a default series
DEFAULT_SERIES_ID = "series-1"
if not STORE.get_series(DEFAULT_SERIES_ID):
    STORE.reset_series(
        Series(id=DEFAULT_SERIES_ID, index=1, started_at=datetime.utcnow(), rolls_in_series=0)
    )


@public_router.get("/status")
async def status() -> dict:
    s = STORE.get_series(DEFAULT_SERIES_ID)
    return {"ok": True, "series_id": s.id if s else None, "rolls": s.rolls_in_series if s else 0}


@public_router.post("/start_session")
async def start_session(bracelet_id_hash: str | None = None) -> dict:
    session_id = str(uuid4())
    treatment: Treatment = ASSIGNER.assign()
    participant = Participant(
        session_id=session_id,
        bracelet_id_hash=bracelet_id_hash,
        consent_version="v1",
        consent_accepted_at=datetime.utcnow(),
        treatment=treatment,
    )
    STORE.upsert_participant(participant)
    audit_event("start_session", session_id=session_id, treatment=treatment.model_dump())
    return {"session_id": session_id, "treatment": treatment.model_dump()}


@public_router.post("/roll_die")
async def roll_die(session_id: str) -> dict:
    participant = STORE.get_participant(session_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    value, served_at = DICE.roll()
    s = STORE.get_series(DEFAULT_SERIES_ID)
    if not s or not s.active:
        raise HTTPException(status_code=400, detail="Serie no activa")
    s = SERIES.record_roll(s.id, value)

    event = RollEvent(
        series_id=s.id,
        session_id=session_id,
        rolled_value=value,
        served_at=served_at,
        interaction_hash=str(uuid4()),
    )
    STORE.set_last_roll(event)
    audit_event("roll_die", session_id=session_id, value=value, served_at=served_at.isoformat())
    return {"real": value, "served_at": served_at.isoformat(), "ih": event.interaction_hash}


@public_router.post("/report")
async def report(session_id: str, reported_value: int) -> dict:
    participant = STORE.get_participant(session_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    last = STORE.get_last_roll(session_id)
    if not last:
        raise HTTPException(status_code=400, detail="No hay lanzamiento previo")

    # single valid report rule and time window (e.g., 60s)
    if STORE.get_report(session_id):
        raise HTTPException(status_code=400, detail="Reporte ya registrado")

    if datetime.utcnow() - last.served_at > timedelta(seconds=60):
        accepted = False
        reason = "Fuera de ventana"
        tickets = 0
    else:
        accepted = True
        reason = None
        tickets = TICKETS.tickets_for_report(int(reported_value))

    r = ReportEvent(
        series_id=last.series_id,
        session_id=session_id,
        reported_value=int(reported_value),
        received_at=datetime.utcnow(),
        accepted=accepted,
        reason=reason,
        tickets_awarded=tickets,
    )
    STORE.set_report(r)
    audit_event(
        "report",
        session_id=session_id,
        reported_value=int(reported_value),
        accepted=accepted,
        tickets=tickets,
        reason=reason,
    )
    return {"accepted": accepted, "tickets": tickets, "reason": reason}


@public_router.get("/norm")
async def get_norm(session_id: str) -> dict:
    participant = STORE.get_participant(session_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    recent_fives_percentage = SERIES.recent_percentage_of_value(DEFAULT_SERIES_ID, 5)
    msg = compute_normative_message(
        participant.treatment.arm, participant.treatment.reference_size, recent_fives_percentage
    )
    return {"message": msg, "spoiler": False}

