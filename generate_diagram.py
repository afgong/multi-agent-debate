"""Generate a simple text-based diagram of the debate flow."""


def generate_flow_diagram():
    """Generate ASCII diagram of debate flow."""

    diagram_4_agents = """
DEBATE FLOW - 4 AGENTS (2 ROUNDS)
=================================

Topic: "Will agentic AI displace the need for MBA talent?"

┌─────────────────────────────────────────────────────────────┐
│                         ROUND 1                              │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  RESEARCHER  │  Gathers evidence, presents balanced
    │              │  arguments from multiple perspectives
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │    CRITIC    │  Identifies weaknesses, challenges
    │              │  assumptions, finds gaps in evidence
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ SYNTHESIZER  │  Integrates feedback, refines arguments,
    │              │  resolves contradictions
    └──────┬───────┘
           │
           ▼

┌─────────────────────────────────────────────────────────────┐
│                         ROUND 2                              │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  RESEARCHER  │  Builds on Round 1 synthesis,
    │              │  addresses critiques
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │    CRITIC    │  Re-evaluates refined arguments,
    │              │  identifies remaining issues
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ SYNTHESIZER  │  Final integration and refinement
    │              │
    └──────┬───────┘
           │
           ▼

┌─────────────────────────────────────────────────────────────┐
│                    FINAL JUDGMENT                            │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │    JUDGE     │  Evaluates all rounds on rubric:
    │              │  • Evidence (0-5)
    │              │  • Feasibility (0-5)
    │              │  • Risks (0-5)
    │              │  • Clarity (0-5)
    │              │  Issues final verdict
    └──────────────┘
"""

    diagram_2_agents = """
DEBATE FLOW - 2 AGENTS (2 ROUNDS)
=================================

Topic: "Will agentic AI displace the need for MBA talent?"

┌─────────────────────────────────────────────────────────────┐
│                         ROUND 1                              │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  RESEARCHER  │  Presents initial arguments with
    │              │  evidence from multiple perspectives
    └──────┬───────┘
           │
           ▼

┌─────────────────────────────────────────────────────────────┐
│                         ROUND 2                              │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  RESEARCHER  │  Refines arguments based on Round 1,
    │              │  adds more depth and nuance
    └──────┬───────┘
           │
           ▼

┌─────────────────────────────────────────────────────────────┐
│                    FINAL JUDGMENT                            │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │    JUDGE     │  Evaluates all arguments on rubric:
    │              │  • Evidence (0-5)
    │              │  • Feasibility (0-5)
    │              │  • Risks (0-5)
    │              │  • Clarity (0-5)
    │              │  Issues final verdict
    └──────────────┘
"""

    return diagram_4_agents, diagram_2_agents


def main():
    """Generate and save diagrams."""
    import os

    output_dir = "deliverables"
    os.makedirs(output_dir, exist_ok=True)

    diagram_4, diagram_2 = generate_flow_diagram()

    with open(f"{output_dir}/flow_diagram_4_agents.txt", "w") as f:
        f.write(diagram_4)

    with open(f"{output_dir}/flow_diagram_2_agents.txt", "w") as f:
        f.write(diagram_2)

    print("✓ Diagrams generated in deliverables/")
    print("  - flow_diagram_4_agents.txt")
    print("  - flow_diagram_2_agents.txt")
    print("\nYou can copy these into your slides/document!")


if __name__ == "__main__":
    main()
