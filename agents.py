"""Agent definitions for the multi-agent debate system."""

import os
from crewai import Agent, LLM
from config import DebateConfig


def create_llm(config: DebateConfig) -> LLM:
    """Create an LLM instance with proper Anthropic configuration."""
    return LLM(
        model=f"anthropic/{config.model_name}",
        temperature=config.temperature,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )


def create_researcher(config: DebateConfig) -> Agent:
    """Create a Researcher agent that gathers evidence and forms initial arguments."""
    return Agent(
        role="Researcher",
        goal=f"Thoroughly research the topic: '{config.topic}' and provide evidence-based arguments from multiple perspectives",
        backstory="""You are an expert researcher with deep knowledge in business,
        technology, and organizational behavior. You excel at finding relevant data,
        case studies, and trends to support informed discussions. You consider both
        sides of an argument and present balanced, evidence-based perspectives.""",
        verbose=config.verbose,
        allow_delegation=False,
        llm=create_llm(config),
    )


def create_critic(config: DebateConfig) -> Agent:
    """Create a Critic agent that challenges arguments and identifies weaknesses."""
    return Agent(
        role="Critic",
        goal="Critically evaluate arguments, identify logical fallacies, gaps in evidence, and potential counterarguments",
        backstory="""You are a sharp critical thinker who excels at identifying
        weaknesses in arguments, spotting unsupported claims, and asking tough questions.
        You play devil's advocate to stress-test ideas and ensure robust reasoning.
        You're not negative for the sake of it - your goal is to strengthen arguments
        through rigorous scrutiny.""",
        verbose=config.verbose,
        allow_delegation=False,
        llm=create_llm(config),
    )


def create_synthesizer(config: DebateConfig) -> Agent:
    """Create a Synthesizer agent that integrates perspectives and refines arguments."""
    return Agent(
        role="Synthesizer",
        goal="Integrate diverse perspectives, resolve contradictions, and synthesize refined arguments that incorporate valid critiques",
        backstory="""You are a master at seeing the big picture and finding common
        ground between opposing viewpoints. You excel at integrating feedback,
        resolving contradictions, and producing refined, nuanced arguments that
        acknowledge complexity. You build bridges between ideas and create coherent
        narratives from multiple perspectives.""",
        verbose=config.verbose,
        allow_delegation=False,
        llm=create_llm(config),
    )


def create_judge(config: DebateConfig) -> Agent:
    """Create a Judge agent that evaluates arguments and issues final verdicts."""
    return Agent(
        role="Judge",
        goal="Evaluate all arguments objectively, score them on the quality rubric (evidence, feasibility, risks, clarity), and issue a final verdict",
        backstory="""You are an impartial judge with expertise in evaluating
        complex arguments. You assess claims based on evidence quality, logical
        coherence, feasibility, risk analysis, and clarity of communication.
        You provide detailed scores (0-5) for each criterion and explain your
        reasoning. You can declare a winner, acknowledge a tie, or state that
        consensus was not reached if the debate remains unresolved.""",
        verbose=config.verbose,
        allow_delegation=False,
        llm=create_llm(config),
    )


def create_devil_advocate(config: DebateConfig) -> Agent:
    """Create a Devil's Advocate agent that challenges consensus and explores contrarian views."""
    return Agent(
        role="Devil's Advocate",
        goal="Challenge emerging consensus by presenting contrarian viewpoints and exploring unconsidered edge cases",
        backstory="""You are a contrarian thinker who thrives on challenging
        conventional wisdom. Your job is to prevent groupthink by presenting
        alternative perspectives, even unpopular ones. You ask 'what if?' questions
        and explore scenarios others might dismiss. You ensure the debate considers
        all angles, no matter how uncomfortable.""",
        verbose=config.verbose,
        allow_delegation=False,
        llm=create_llm(config),
    )


def get_debate_agents(config: DebateConfig) -> list[Agent]:
    """Get the appropriate agents based on configuration."""
    if config.num_agents == 2:
        # Simplified debate: Researcher and Judge only
        return [create_researcher(config), create_judge(config)]
    elif config.num_agents == 4:
        agents = [
            create_researcher(config),
            create_critic(config),
            create_synthesizer(config),
            create_judge(config),
        ]
        if config.include_devil_advocate:
            # Replace Synthesizer with Devil's Advocate for role swap
            agents[2] = create_devil_advocate(config)
        return agents
    else:
        raise ValueError(f"num_agents must be 2 or 4, got {config.num_agents}")
