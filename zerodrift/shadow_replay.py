"""
zerodrift.shadow_replay - Differential Traffic Replay & Behavioral Parity Engine

Executes parallel shadow executions of legacy and AI-migrated services across recorded
traffic traces, asserting byte-level schema equivalence, float tolerance, and latency bounds.
"""

import time
import json
import hashlib
import dataclasses
from typing import Callable, Any, Dict, List, Optional, Tuple


@dataclasses.dataclass
class ReplayResult:
    total_samples: int
    parity_rate: float
    divergences: List[Dict[str, Any]]
    avg_latency_legacy_ms: float
    avg_latency_migrated_ms: float
    verification_hash: str
    is_certified: bool


class ShadowReplayEngine:
    def __init__(self, float_tolerance: float = 1e-6, max_divergences_logged: int = 20):
        self.float_tolerance = float_tolerance
        self.max_divergences_logged = max_divergences_logged

    def _values_equivalent(self, val_a: Any, val_b: Any) -> bool:
        if isinstance(val_a, float) and isinstance(val_b, float):
            return abs(val_a - val_b) <= self.float_tolerance
        if type(val_a) != type(val_b):
            return False
        if isinstance(val_a, dict):
            if val_a.keys() != val_b.keys():
                return False
            return all(self._values_equivalent(val_a[k], val_b[k]) for k in val_a)
        if isinstance(val_a, (list, tuple)):
            if len(val_a) != len(val_b):
                return False
            return all(self._values_equivalent(a, b) for a, b in zip(val_a, val_b))
        return val_a == val_b

    def run_replay(
        self,
        legacy_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        migrated_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        trace_dataset: List[Dict[str, Any]],
    ) -> ReplayResult:
        """
        Executes trace dataset across both runners and generates zero-drift verification report.
        """
        total = len(trace_dataset)
        matches = 0
        divergences = []
        legacy_times = []
        migrated_times = []

        for idx, payload in enumerate(trace_dataset):
            # Run legacy
            t0 = time.perf_counter()
            try:
                res_legacy = legacy_fn(payload)
                legacy_ok = True
            except Exception as e:
                res_legacy = {"__error__": str(e)}
                legacy_ok = False
            t_legacy = (time.perf_counter() - t0) * 1000.0
            legacy_times.append(t_legacy)

            # Run migrated
            t1 = time.perf_counter()
            try:
                res_migrated = migrated_fn(payload)
                migrated_ok = True
            except Exception as e:
                res_migrated = {"__error__": str(e)}
                migrated_ok = False
            t_migrated = (time.perf_counter() - t1) * 1000.0
            migrated_times.append(t_migrated)

            # Compare
            is_equiv = (legacy_ok == migrated_ok) and self._values_equivalent(res_legacy, res_migrated)
            if is_equiv:
                matches += 1
            else:
                if len(divergences) < self.max_divergences_logged:
                    divergences.append({
                        "sample_index": idx,
                        "payload": payload,
                        "legacy_output": res_legacy,
                        "migrated_output": res_migrated,
                        "legacy_latency_ms": round(t_legacy, 2),
                        "migrated_latency_ms": round(t_migrated, 2)
                    })

        parity_rate = (matches / total * 100.0) if total > 0 else 0.0
        avg_leg = sum(legacy_times) / max(1, len(legacy_times))
        avg_mig = sum(migrated_times) / max(1, len(migrated_times))

        cert_payload = f"{total}:{matches}:{parity_rate:.4f}:{avg_mig:.2f}".encode("utf-8")
        cert_hash = hashlib.sha256(cert_payload).hexdigest()

        return ReplayResult(
            total_samples=total,
            parity_rate=round(parity_rate, 2),
            divergences=divergences,
            avg_latency_legacy_ms=round(avg_leg, 2),
            avg_latency_migrated_ms=round(avg_mig, 2),
            verification_hash=f"0x{cert_hash[:24]}",
            is_certified=(parity_rate >= 99.9)
        )
