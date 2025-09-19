from __future__ import annotations

import structlog


logger = structlog.get_logger()


def audit_event(event: str, **kwargs) -> None:
    logger.info(event, **kwargs)

