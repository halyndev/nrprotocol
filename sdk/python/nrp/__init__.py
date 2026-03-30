# Copyright (c) 2026 Elmadani SALKA. 
"""
NRP — Node Reach Protocol

The universal protocol for AI-to-world control.
MCP connects LLMs to software. NRP connects LLMs to everything else.

    from nrp import NRPDriver, NRPId, NRPManifest, EventBus

https://github.com/navigia/nrp
"""

from .identity import NRPId
from .manifest import NRPManifest, ChannelSpec, ActionSpec, ShieldSpec
from .events import NRPEvent, EventBus, EventSSE, Severity
from .driver import NRPDriver, ShieldRule, ShieldType

__version__ = "0.1.0"
__author__ = "Elmadani SALKA"
__license__ = "MIT"

__all__ = [
    "NRPId",
    "NRPManifest", "ChannelSpec", "ActionSpec", "ShieldSpec",
    "NRPEvent", "EventBus", "EventSSE", "Severity",
    "NRPDriver", "ShieldRule", "ShieldType",
]

