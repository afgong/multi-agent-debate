"""Task definitions for the debate workflow."""

from crewai import Task, Agent
from config import DebateConfig, RUBRIC_CRITERIA


def create_research_task(researcher: Agent, config: DebateConfig, round_num: int, previous_output: str = "") -> Task:
    """Create research task for gathering and presenting arguments."""
    context_str = f"\n\nPrevious round output:\n{previous_output}" if previous_output else ""

    return Task(
        description=f"""Research and present arguments on the topic: '{config.topic}'

        Round {round_num} of {config.num_rounds}

        Your task:
        1. Present evidence-based arguments considering multiple perspectives
        2. Include relevant data, trends, case studies, or expert opinions
        3. Address both potential benefits and drawbacks
        4. Be specific and concrete in your examples{context_str}

        Provide a structured argument with clear reasoning.""",
        agent=researcher,
        expected_output="A well-researched argument with supporting evidence and multiple perspectives"
    )


def create_critique_task(critic: Agent, config: DebateConfig, round_num: int, research_output: str) -> Task:
    """Create critique task for evaluating arguments."""
    return Task(
        description=f"""Critically evaluate the following argument on '{config.topic}':

        {research_output}

        Your task:
        1. Identify strengths in the argument
        2. Spot weaknesses, logical fallacies, or unsupported claims
        3. Challenge assumptions and identify gaps in evidence
        4. Propose counterarguments or alternative perspectives
        5. Ask probing questions that need to be addressed

        Be thorough but fair in your critique.""",
        agent=critic,
        expected_output="A detailed critique identifying strengths, weaknesses, and areas for improvement"
    )


def create_synthesis_task(synthesizer: Agent, config: DebateConfig, round_num: int,
                         research_output: str, critique_output: str) -> Task:
    """Create synthesis task for integrating perspectives."""
    return Task(
        description=f"""Synthesize and refine the argument on '{config.topic}' based on:

        ORIGINAL ARGUMENT:
        {research_output}

        CRITIQUE:
        {critique_output}

        Your task:
        1. Acknowledge valid points from the critique
        2. Address weaknesses and gaps identified
        3. Integrate counterarguments and nuance
        4. Produce a refined, stronger argument
        5. Resolve contradictions where possible

        Create a balanced, nuanced perspective.""",
        agent=synthesizer,
        expected_output="A refined synthesis that integrates feedback and addresses critiques"
    )


def create_devil_advocate_task(devil_advocate: Agent, config: DebateConfig, round_num: int,
                               research_output: str, critique_output: str) -> Task:
    """Create devil's advocate task for challenging consensus."""
    return Task(
        description=f"""Challenge the emerging consensus on '{config.topic}' based on:

        ORIGINAL ARGUMENT:
        {research_output}

        CRITIQUE:
        {critique_output}

        Your task:
        1. Identify any groupthink or unchallenged assumptions
        2. Present contrarian viewpoints that haven't been considered
        3. Explore edge cases and unconventional scenarios
        4. Question the fundamental premises of the argument
        5. Push the discussion in new, unexpected directions

        Be provocative but intellectually honest.""",
        agent=devil_advocate,
        expected_output="Contrarian perspectives and challenges to consensus thinking"
    )


def create_judge_task(judge: Agent, config: DebateConfig, all_outputs: list[str]) -> Task:
    """Create final judgment task for evaluating the debate."""
    debate_history = "\n\n=== DEBATE HISTORY ===\n\n".join(
        [f"Round {i+1}:\n{output}" for i, output in enumerate(all_outputs)]
    )

    rubric_desc = "\n".join([f"- {k.title()}: {v}" for k, v in RUBRIC_CRITERIA.items()])

    return Task(
        description=f"""Evaluate the complete debate on '{config.topic}' and issue your final verdict.

        {debate_history}

        Your task:
        1. Score the final argument on each rubric criterion (0-5 scale):
        {rubric_desc}

        2. Provide your scores in this exact format:
        SCORES:
        - Evidence: X/5
        - Feasibility: X/5
        - Risks: X/5
        - Clarity: X/5

        3. Determine the outcome:
           - Did the debate reach a clear conclusion?
           - What is your final verdict on the topic?
           - OR state if consensus was not reached

        4. Highlight 1-2 key moments where critique improved the argument

        5. Overall assessment: quality of the debate process

        Be objective, specific, and provide clear reasoning for your scores.""",
        agent=judge,
        expected_output="Rubric scores (0-5), final verdict or non-consensus statement, key excerpts, and overall assessment"
    )
