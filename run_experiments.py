"""Run multiple debate experiments with different configurations."""

import sys
from config import DebateConfig
from debate import run_debate


def run_experiment_1():
    """Experiment 1: 2 agents vs 4 agents (2 rounds each)."""
    print("\n" + "="*100)
    print("EXPERIMENT 1: 2 Agents vs 4 Agents")
    print("="*100 + "\n")

    # Run with 2 agents
    print("\n>>> Running with 2 agents...")
    config_2 = DebateConfig(
        num_agents=2,
        num_rounds=2,
        temperature=0.7,
        verbose=True
    )
    results_2 = run_debate(config_2)

    # Run with 4 agents
    print("\n>>> Running with 4 agents...")
    config_4 = DebateConfig(
        num_agents=4,
        num_rounds=2,
        temperature=0.7,
        verbose=True
    )
    results_4 = run_debate(config_4)

    return {"2_agents": results_2, "4_agents": results_4}


def run_experiment_2():
    """Experiment 2: 1 round vs 3 rounds (4 agents each)."""
    print("\n" + "="*100)
    print("EXPERIMENT 2: 1 Round vs 3 Rounds")
    print("="*100 + "\n")

    # Run with 1 round
    print("\n>>> Running with 1 round...")
    config_1 = DebateConfig(
        num_agents=4,
        num_rounds=1,
        temperature=0.7,
        verbose=True
    )
    results_1 = run_debate(config_1)

    # Run with 3 rounds
    print("\n>>> Running with 3 rounds...")
    config_3 = DebateConfig(
        num_agents=4,
        num_rounds=3,
        temperature=0.7,
        verbose=True
    )
    results_3 = run_debate(config_3)

    return {"1_round": results_1, "3_rounds": results_3}


def run_experiment_3():
    """Experiment 3: With vs without Devil's Advocate (4 agents, 2 rounds)."""
    print("\n" + "="*100)
    print("EXPERIMENT 3: Synthesizer vs Devil's Advocate")
    print("="*100 + "\n")

    # Run without Devil's Advocate
    print("\n>>> Running with Synthesizer (no Devil's Advocate)...")
    config_no_da = DebateConfig(
        num_agents=4,
        num_rounds=2,
        temperature=0.7,
        include_devil_advocate=False,
        verbose=True
    )
    results_no_da = run_debate(config_no_da)

    # Run with Devil's Advocate
    print("\n>>> Running with Devil's Advocate...")
    config_da = DebateConfig(
        num_agents=4,
        num_rounds=2,
        temperature=0.7,
        include_devil_advocate=True,
        verbose=True
    )
    results_da = run_debate(config_da)

    return {"synthesizer": results_no_da, "devil_advocate": results_da}


def run_experiment_4():
    """Experiment 4: Low temperature vs High temperature (4 agents, 2 rounds)."""
    print("\n" + "="*100)
    print("EXPERIMENT 4: Low Temperature (0.3) vs High Temperature (0.9)")
    print("="*100 + "\n")

    # Run with low temperature
    print("\n>>> Running with low temperature (0.3)...")
    config_low = DebateConfig(
        num_agents=4,
        num_rounds=2,
        temperature=0.3,
        verbose=True
    )
    results_low = run_debate(config_low)

    # Run with high temperature
    print("\n>>> Running with high temperature (0.9)...")
    config_high = DebateConfig(
        num_agents=4,
        num_rounds=2,
        temperature=0.9,
        verbose=True
    )
    results_high = run_debate(config_high)

    return {"low_temp": results_low, "high_temp": results_high}


def main():
    """Run selected experiments."""
    print("\n" + "="*100)
    print("MULTI-AGENT DEBATE - EXPERIMENT RUNNER")
    print("="*100)
    print("\nAvailable experiments:")
    print("1. 2 agents vs 4 agents")
    print("2. 1 round vs 3 rounds")
    print("3. Synthesizer vs Devil's Advocate")
    print("4. Low temperature (0.3) vs High temperature (0.9)")
    print("\nYou need to run 2 experiments for the assignment.")
    print("="*100 + "\n")

    if len(sys.argv) > 1:
        # Run specific experiments from command line
        experiment_nums = [int(x) for x in sys.argv[1:]]
    else:
        # Default: run experiments 1 and 2
        print("Running default experiments: #1 (agents) and #2 (rounds)")
        experiment_nums = [1, 2]

    results = {}
    for num in experiment_nums:
        if num == 1:
            results["experiment_1"] = run_experiment_1()
        elif num == 2:
            results["experiment_2"] = run_experiment_2()
        elif num == 3:
            results["experiment_3"] = run_experiment_3()
        elif num == 4:
            results["experiment_4"] = run_experiment_4()
        else:
            print(f"Unknown experiment number: {num}")

    print("\n" + "="*100)
    print("ALL EXPERIMENTS COMPLETED")
    print("="*100)
    print(f"\nResults saved in the 'results/' directory")
    print("Check the JSON files for detailed outputs and timing information.")
    print("="*100 + "\n")


if __name__ == "__main__":
    main()
