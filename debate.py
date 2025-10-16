"""Main debate orchestration logic."""

import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from crewai import Crew, Process
from dotenv import load_dotenv

from config import DebateConfig
from agents import get_debate_agents
from tasks import (
    create_research_task,
    create_critique_task,
    create_synthesis_task,
    create_devil_advocate_task,
    create_judge_task,
)


class DebateOrchestrator:
    """Orchestrates the multi-agent debate."""

    def __init__(self, config: DebateConfig):
        self.config = config
        self.agents = get_debate_agents(config)
        self.round_outputs = []
        self.start_time = None
        self.end_time = None

    def run_debate(self) -> dict:
        """Run the complete debate and return results."""
        print(f"\n{'='*80}")
        print(f"MULTI-AGENT DEBATE")
        print(f"{'='*80}")
        print(f"Topic: {self.config.topic}")
        print(f"Agents: {self.config.num_agents} ({', '.join([a.role for a in self.agents])})")
        print(f"Rounds: {self.config.num_rounds}")
        print(f"Temperature: {self.config.temperature}")
        print(f"Model: {self.config.model_name}")
        print(f"{'='*80}\n")

        self.start_time = time.time()

        # Run debate rounds
        previous_output = ""
        for round_num in range(1, self.config.num_rounds + 1):
            print(f"\n{'='*80}")
            print(f"ROUND {round_num}/{self.config.num_rounds}")
            print(f"{'='*80}\n")

            round_start = time.time()
            round_output = self._run_round(round_num, previous_output)
            round_end = time.time()

            self.round_outputs.append({
                "round": round_num,
                "output": round_output,
                "duration": round_end - round_start
            })

            previous_output = round_output
            print(f"\nRound {round_num} completed in {round_end - round_start:.2f}s")

        # Final judgment
        print(f"\n{'='*80}")
        print(f"FINAL JUDGMENT")
        print(f"{'='*80}\n")

        final_verdict = self._run_final_judgment()
        self.end_time = time.time()

        # Compile results
        results = {
            "config": {
                "topic": self.config.topic,
                "num_agents": self.config.num_agents,
                "num_rounds": self.config.num_rounds,
                "temperature": self.config.temperature,
                "model": self.config.model_name,
                "agents": [a.role for a in self.agents],
                "include_devil_advocate": self.config.include_devil_advocate,
            },
            "rounds": self.round_outputs,
            "final_verdict": final_verdict,
            "total_duration": self.end_time - self.start_time,
            "timestamp": datetime.now().isoformat(),
        }

        # Save results if configured
        if self.config.save_results:
            self._save_results(results)

        return results

    def _run_round(self, round_num: int, previous_output: str) -> str:
        """Run a single debate round."""
        if self.config.num_agents == 2:
            # Simple 2-agent debate: Researcher only
            researcher = self.agents[0]
            task = create_research_task(researcher, self.config, round_num, previous_output)

            crew = Crew(
                agents=[researcher],
                tasks=[task],
                process=Process.sequential,
                verbose=self.config.verbose,
            )

            result = crew.kickoff()
            return str(result)

        elif self.config.num_agents == 4:
            # Full 4-agent debate: Researcher → Critic → Synthesizer/Devil's Advocate
            researcher, critic, third_agent, _ = self.agents

            # Research task
            research_task = create_research_task(researcher, self.config, round_num, previous_output)
            research_crew = Crew(
                agents=[researcher],
                tasks=[research_task],
                process=Process.sequential,
                verbose=self.config.verbose,
            )
            research_output = str(research_crew.kickoff())

            # Critique task
            critique_task = create_critique_task(critic, self.config, round_num, research_output)
            critique_crew = Crew(
                agents=[critic],
                tasks=[critique_task],
                process=Process.sequential,
                verbose=self.config.verbose,
            )
            critique_output = str(critique_crew.kickoff())

            # Synthesis or Devil's Advocate task
            if self.config.include_devil_advocate:
                synthesis_task = create_devil_advocate_task(
                    third_agent, self.config, round_num, research_output, critique_output
                )
            else:
                synthesis_task = create_synthesis_task(
                    third_agent, self.config, round_num, research_output, critique_output
                )

            synthesis_crew = Crew(
                agents=[third_agent],
                tasks=[synthesis_task],
                process=Process.sequential,
                verbose=self.config.verbose,
            )
            synthesis_output = str(synthesis_crew.kickoff())

            # Combine outputs for this round
            return f"""RESEARCHER:
{research_output}

CRITIC:
{critique_output}

{third_agent.role.upper()}:
{synthesis_output}"""

    def _run_final_judgment(self) -> str:
        """Run the final judgment phase."""
        judge = self.agents[-1]  # Judge is always last

        all_outputs = [r["output"] for r in self.round_outputs]
        judge_task = create_judge_task(judge, self.config, all_outputs)

        judge_crew = Crew(
            agents=[judge],
            tasks=[judge_task],
            process=Process.sequential,
            verbose=self.config.verbose,
        )

        result = str(judge_crew.kickoff())
        return result

    def _save_results(self, results: dict) -> None:
        """Save results to a JSON file."""
        output_dir = Path("results")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debate_{self.config.num_agents}agents_{self.config.num_rounds}rounds_{timestamp}.json"
        filepath = output_dir / filename

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*80}")
        print(f"Results saved to: {filepath}")
        print(f"{'='*80}\n")


def run_debate(config: Optional[DebateConfig] = None) -> dict:
    """Convenience function to run a debate with the given configuration."""
    load_dotenv()

    # Verify API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment. "
            "Please create a .env file with your API key."
        )

    if config is None:
        config = DebateConfig()

    orchestrator = DebateOrchestrator(config)
    return orchestrator.run_debate()


if __name__ == "__main__":
    # Run with default configuration
    run_debate()
