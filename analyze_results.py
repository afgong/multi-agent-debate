"""Analyze debate results and extract key metrics."""

import json
import re
from pathlib import Path
from typing import Dict, Any


def extract_scores(verdict_text: str) -> Dict[str, int]:
    """Extract rubric scores from judge's verdict."""
    scores = {}
    score_pattern = r"(Evidence|Feasibility|Risks|Clarity):\s*(\d+)/5"

    matches = re.findall(score_pattern, verdict_text, re.IGNORECASE)
    for criterion, score in matches:
        scores[criterion.lower()] = int(score)

    return scores


def analyze_debate_file(filepath: Path) -> Dict[str, Any]:
    """Analyze a single debate result file."""
    with open(filepath, "r") as f:
        data = json.load(f)

    config = data["config"]
    verdict = data["final_verdict"]

    # Extract scores
    scores = extract_scores(verdict)

    # Calculate average score
    avg_score = sum(scores.values()) / len(scores) if scores else 0

    # Check for convergence indicators
    convergence_keywords = ["consensus", "agree", "concluded", "resolved"]
    non_convergence_keywords = ["no consensus", "disagreement", "unresolved", "loop"]

    verdict_lower = verdict.lower()
    converged = any(kw in verdict_lower for kw in convergence_keywords)
    diverged = any(kw in verdict_lower for kw in non_convergence_keywords)

    convergence_status = "Converged" if converged and not diverged else \
                        "Diverged" if diverged else "Unclear"

    analysis = {
        "filename": filepath.name,
        "config": config,
        "scores": scores,
        "average_score": round(avg_score, 2),
        "total_duration": round(data["total_duration"], 2),
        "rounds": len(data["rounds"]),
        "convergence": convergence_status,
        "round_durations": [round(r["duration"], 2) for r in data["rounds"]],
    }

    return analysis


def print_analysis(analysis: Dict[str, Any]):
    """Print formatted analysis."""
    print(f"\n{'='*80}")
    print(f"Analysis: {analysis['filename']}")
    print(f"{'='*80}")

    config = analysis["config"]
    print(f"\nConfiguration:")
    print(f"  Agents: {config['num_agents']} ({', '.join(config['agents'])})")
    print(f"  Rounds: {config['num_rounds']}")
    print(f"  Temperature: {config['temperature']}")
    print(f"  Model: {config['model']}")

    print(f"\nScores (0-5):")
    for criterion, score in analysis["scores"].items():
        print(f"  {criterion.title()}: {score}/5")
    print(f"  Average: {analysis['average_score']}/5")

    print(f"\nTiming:")
    print(f"  Total Duration: {analysis['total_duration']}s")
    for i, duration in enumerate(analysis["round_durations"], 1):
        print(f"  Round {i}: {duration}s")

    print(f"\nConvergence: {analysis['convergence']}")
    print(f"{'='*80}\n")


def compare_experiments(analyses: list[Dict[str, Any]]):
    """Compare multiple experiment results."""
    if len(analyses) < 2:
        print("Need at least 2 results to compare.")
        return

    print(f"\n{'='*80}")
    print("EXPERIMENT COMPARISON")
    print(f"{'='*80}\n")

    # Create comparison table
    print(f"{'Metric':<25} | {'Experiment 1':<30} | {'Experiment 2':<30}")
    print(f"{'-'*25}-|-{'-'*30}-|-{'-'*30}")

    a1, a2 = analyses[0], analyses[1]

    # Config differences
    print(f"{'Agents':<25} | {str(a1['config']['num_agents']):<30} | {str(a2['config']['num_agents']):<30}")
    print(f"{'Rounds':<25} | {str(a1['config']['num_rounds']):<30} | {str(a2['config']['num_rounds']):<30}")
    print(f"{'Temperature':<25} | {str(a1['config']['temperature']):<30} | {str(a2['config']['temperature']):<30}")

    # Scores
    print(f"{'-'*25}-|-{'-'*30}-|-{'-'*30}")
    print(f"{'Average Score':<25} | {str(a1['average_score']) + '/5':<30} | {str(a2['average_score']) + '/5':<30}")

    for criterion in ["evidence", "feasibility", "risks", "clarity"]:
        s1 = a1['scores'].get(criterion, "N/A")
        s2 = a2['scores'].get(criterion, "N/A")
        print(f"{criterion.title():<25} | {str(s1) + '/5' if isinstance(s1, int) else s1:<30} | {str(s2) + '/5' if isinstance(s2, int) else s2:<30}")

    # Timing
    print(f"{'-'*25}-|-{'-'*30}-|-{'-'*30}")
    print(f"{'Total Duration (s)':<25} | {str(a1['total_duration']):<30} | {str(a2['total_duration']):<30}")

    # Convergence
    print(f"{'Convergence':<25} | {a1['convergence']:<30} | {a2['convergence']:<30}")

    print(f"{'='*80}\n")


def main():
    """Analyze all results in the results directory."""
    results_dir = Path("results")

    if not results_dir.exists():
        print("No results directory found. Run some debates first!")
        return

    json_files = list(results_dir.glob("*.json"))

    if not json_files:
        print("No result files found in results/")
        return

    # Sort by timestamp (newest first)
    json_files.sort(reverse=True)

    print(f"\nFound {len(json_files)} result files\n")

    analyses = []
    for filepath in json_files:
        analysis = analyze_debate_file(filepath)
        print_analysis(analysis)
        analyses.append(analysis)

    # If we have multiple results, compare them
    if len(analyses) >= 2:
        # Compare the two most recent
        compare_experiments(analyses[:2])


if __name__ == "__main__":
    main()
