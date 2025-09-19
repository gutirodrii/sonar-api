from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Tuple

from app.models.schemas import ReferenceSize, Treatment, TreatmentArm


@dataclass
class StratifiedRandomAssigner:
    seed: int

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def assign(self) -> Treatment:
        # Balanced probabilities across arms (25/50/75 equally likely overall)
        arm_choice = self._rng.choice([TreatmentArm.t25, TreatmentArm.t50, TreatmentArm.t75])
        ref_choice = self._rng.choice([ReferenceSize.n10, ReferenceSize.n100])
        return Treatment(arm=arm_choice, reference_size=ref_choice)

    def reseed(self, seed: int) -> None:
        self.seed = seed
        self._rng.seed(seed)


def probability_for_arm(arm: TreatmentArm) -> float:
    return {TreatmentArm.t25: 0.25, TreatmentArm.t50: 0.5, TreatmentArm.t75: 0.75}[arm]


def compute_normative_message(arm: TreatmentArm, reference_size: ReferenceSize, recent_fives_percentage: float) -> str:
    ref_text = f"últimos {reference_size}"
    return f"Norma descriptiva: {recent_fives_percentage:.0f}% de 5 en {ref_text} (brazo {arm})"

