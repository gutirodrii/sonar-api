from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.deps.container import CONTAINER


admin_router = APIRouter()

STORE = CONTAINER.store
SERIES = CONTAINER.series


@admin_router.post("/series/rotate")
async def rotate_series() -> dict:
    new_s = SERIES.rotate_series()
    return {"series_id": new_s.id, "index": new_s.index}


@admin_router.get("/series/status")
async def series_status() -> dict:
    # naive: return the last active series known
    # In memory version keeps one by default in public bootstrap
    # We'll expose minimal info
    active = None
    for s in STORE.series.values():
        if s.active:
            active = s
    if not active:
        raise HTTPException(status_code=404, detail="No hay serie activa")
    return {"id": active.id, "index": active.index, "rolls": active.rolls_in_series}

