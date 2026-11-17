"""Real-time ATS job collectors."""

from src.collectors.ashby import AshbyCollector
from src.collectors.base import BaseATSCollector
from src.collectors.greenhouse import GreenhouseCollector
from src.collectors.lever import LeverCollector
from src.collectors.smartrecruiters import SmartRecruitersCollector
from src.collectors.workable import WorkableCollector

COLLECTOR_REGISTRY: dict[str, type[BaseATSCollector]] = {
    "ashby": AshbyCollector,
    "greenhouse": GreenhouseCollector,
    "lever": LeverCollector,
    "smartrecruiters": SmartRecruitersCollector,
    "workable": WorkableCollector,
}


def get_collector(provider: str) -> BaseATSCollector:
    """Instantiate the collector for a given ATS provider."""
    cls = COLLECTOR_REGISTRY.get(provider.lower())
    if cls is None:
        raise ValueError(f"Unsupported ATS provider: {provider}")
    return cls()


__all__ = [
    "AshbyCollector",
    "BaseATSCollector",
    "GreenhouseCollector",
    "LeverCollector",
    "get_collector",
]

