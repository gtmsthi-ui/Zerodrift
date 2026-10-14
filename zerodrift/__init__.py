"""
ZeroDrift Systems - Deterministic Architecture, Differential Migration & Forensics Suite
"""

__version__ = "0.9.4"
__author__ = "Gautam Sethi & ZeroDrift Systems Research Group"

from .shadow_replay import ShadowReplayEngine, ReplayResult
from .flight_recorder import FlightRecorder, AgentEvent, SecurityViolation
from .autosandbox import AutoSandboxEngine, IncidentReport
