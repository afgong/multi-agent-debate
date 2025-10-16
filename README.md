# Multi-Agent Debate

Running a multi-agent debate on my laptop

## Assignment Overview

### What to Build (Minimum Viable Debate)

- **2–4 agents** with distinct roles (e.g., Researcher, Critic, Synthesizer, Judge)
- **Protocol**: at least 2 rounds (argue → critique → revise), then Judge issues a final verdict (or states non-consensus)
- **Run locally** on a single machine. One model is fine; roles differ by instructions

### Experiments (Keep It Light)

Run any 2 of these toggles (short runs are fine):

- **Agents**: 2 vs 4
- **Rounds**: 1 vs 3
- **Role swap**: add/remove a Devil's Advocate
- **Temperature**: low vs high

### Measure (Simple + Concrete)

- **Quality rubric (0–5)**: evidence, feasibility, risks, clarity
- **Convergence**: did they agree or loop?
- **Latency (optional)**: wall-clock per round
- Include 2–4 short excerpts (e.g., critic catching an error)

### Deliverables

#### Proof It Runs (1 page or 2–4 slides)

- Small diagram of roles & message flow
- Screenshot(s) showing ≥2 rounds and a final verdict
- Config summary (model, temp, memory on/off)

#### Mini-Report (1–2 pages)

- Scenario you tested + acceptance criteria
- Results table (your rubric and any timing)
- What changed with your two toggles
- One paragraph: limits + next step you'd try

### Minimal Example (Pattern to Follow)

- **Agents**: Researcher → Critic → Synthesizer → Judge
- **Rounds**: 2
- **Toggles tried**: (a) 2 vs 4 agents, (b) 1 vs 3 rounds
- **Rubric columns**: Feasibility / Evidence / Risks / Clarity (0–5)

---

## Implementation

### Topic
**"Will agentic AI displace the need for MBA talent?"**

### Setup

1. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up your Anthropic API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

### Project Structure

```
multi-agent-debate/
├── config.py              # Configuration for experiments
├── agents.py              # Agent definitions (Researcher, Critic, Synthesizer, Judge)
├── tasks.py               # Task definitions for each agent
├── debate.py              # Main debate orchestration logic
├── run_experiments.py     # Run multiple experiments
├── analyze_results.py     # Analyze and compare results
├── results/               # Output directory for debate results
└── requirements.txt       # Python dependencies
```

### Usage

#### Run a Single Debate

```bash
# Run with default configuration (4 agents, 2 rounds)
python debate.py
```

#### Run Experiments

```bash
# Run default experiments (1 and 2)
python run_experiments.py

# Run specific experiments
python run_experiments.py 1 3  # Run experiments 1 and 3
```

**Available experiments:**
1. **2 agents vs 4 agents** - Compare simple vs full debate
2. **1 round vs 3 rounds** - Test iteration depth
3. **Synthesizer vs Devil's Advocate** - Role swap experiment
4. **Low temp (0.3) vs High temp (0.9)** - Temperature variation

#### Analyze Results

```bash
# Analyze all results and compare the two most recent
python analyze_results.py
```

### Agent Roles

- **Researcher**: Gathers evidence and forms initial arguments from multiple perspectives
- **Critic**: Challenges arguments, identifies weaknesses, and proposes counterarguments
- **Synthesizer**: Integrates perspectives and refines arguments based on critiques
- **Devil's Advocate**: Challenges consensus with contrarian viewpoints (optional role swap)
- **Judge**: Evaluates arguments using the quality rubric and issues final verdict

### Configuration Options

Edit `config.py` or create custom configurations:

```python
from config import DebateConfig
from debate import run_debate

config = DebateConfig(
    topic="Your debate topic",
    num_agents=4,           # 2 or 4
    num_rounds=2,           # 1, 2, or 3
    temperature=0.7,        # 0.3 (low) to 0.9 (high)
    include_devil_advocate=False,  # True to replace Synthesizer
    model_name="claude-3-5-sonnet-20241022",
    verbose=True,
    save_results=True
)

results = run_debate(config)
```

### Quality Rubric (0-5 scale)

Each debate is scored on:
- **Evidence**: Quality and relevance of supporting evidence
- **Feasibility**: Practicality and realism of arguments
- **Risks**: Identification and assessment of potential risks
- **Clarity**: Clarity and coherence of communication

### Output

Results are saved as JSON files in `results/` with:
- Configuration details
- Full debate transcript (all rounds)
- Final verdict with rubric scores
- Timing information (total duration and per-round)
- Convergence status

### Tech Stack

- **CrewAI** - Multi-agent orchestration framework
- **Anthropic Claude** - LLM (Claude 3.5 Sonnet)
- **Python 3.9+**
