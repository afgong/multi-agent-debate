"""Configuration for the multi-agent debate system."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class DebateConfig:
    """Configuration for debate experiments."""

    # Debate setup
    topic: str = "Will agentic AI displace the need for MBA talent?"
    num_agents: Literal[2, 4] = 4  # 2 or 4 agents
    num_rounds: int = 2  # Number of debate rounds

    # Model configuration
    model_name: str = "claude-3-haiku-20240307"
    temperature: float = 0.7  # Low (0.3) vs High (0.9)

    # Agent roles
    include_devil_advocate: bool = False  # Role swap toggle

    # Output
    save_results: bool = True
    verbose: bool = True


# Quality rubric criteria (0-5 scale)
RUBRIC_CRITERIA = {
    "evidence": "Quality and relevance of evidence provided",
    "feasibility": "Practicality and realism of arguments",
    "risks": "Identification and assessment of potential risks",
    "clarity": "Clarity and coherence of communication"
}
