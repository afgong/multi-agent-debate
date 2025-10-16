# Multi-Agent Debate System - Project Context

## Project Overview

This is a multi-agent debate system built with CrewAI and Anthropic's Claude for an academic assignment. The system orchestrates intelligent agents in structured debates to explore complex topics through collaborative argumentation.

**Current Debate Topic:** "Will agentic AI displace the need for MBA talent?"

## Architecture

### Core Components

1. **config.py** - Central configuration management
   - Debate parameters (topic, agents, rounds)
   - Model settings (temperature, model name)
   - Quality rubric criteria definitions

2. **agents.py** - Agent definitions with distinct roles
   - Researcher: Evidence gathering and balanced perspective
   - Critic: Argument analysis and weakness identification
   - Synthesizer: Integration of perspectives and refinement
   - Devil's Advocate: Contrarian thinking (optional role swap)
   - Judge: Objective evaluation with rubric scoring

3. **tasks.py** - Task definitions for each debate phase
   - Research tasks with context from previous rounds
   - Critique tasks that evaluate arguments
   - Synthesis/Devil's Advocate tasks for refinement
   - Judge tasks for final verdict and scoring

4. **debate.py** - Main orchestration logic
   - DebateOrchestrator class manages the debate flow
   - Handles multi-round debates
   - Tracks timing and performance metrics
   - Saves results as JSON

5. **run_experiments.py** - Experiment runner
   - 4 pre-configured experiment types
   - Toggles: agents (2 vs 4), rounds (1 vs 3), role swap, temperature

6. **analyze_results.py** - Post-debate analysis
   - Extracts rubric scores from judge verdicts
   - Calculates metrics and convergence status
   - Compares multiple experiments side-by-side

## Agent Design Philosophy

### Role-Based Specialization
Each agent has a specific role with tailored instructions:

- **Researcher** - Balanced, evidence-focused, considers multiple viewpoints
- **Critic** - Rigorous, challenges assumptions, identifies gaps
- **Synthesizer** - Integrative, resolves contradictions, builds consensus
- **Devil's Advocate** - Provocative, challenges groupthink, explores edge cases
- **Judge** - Impartial, systematic evaluation, clear scoring

### Debate Flow (4 agents, single round)

```
Researcher → presents initial arguments
     ↓
Critic → evaluates and challenges
     ↓
Synthesizer/Devil's Advocate → refines or challenges
     ↓
(Multiple rounds repeat the above)
     ↓
Judge → final evaluation and verdict
```

### Debate Flow (2 agents)

```
Researcher → presents arguments (informed by previous round)
     ↓
(Multiple rounds of research)
     ↓
Judge → final evaluation and verdict
```

## Quality Rubric

All debates are evaluated on a 0-5 scale across four criteria:

1. **Evidence** - Quality and relevance of supporting data
2. **Feasibility** - Practicality and realism of arguments
3. **Risks** - Identification and assessment of potential risks
4. **Clarity** - Coherence and clarity of communication

## Experiment Framework

The system supports 4 experimental toggles:

1. **Agents (2 vs 4)** - Simple vs full debate structure
2. **Rounds (1 vs 3)** - Iteration depth and refinement
3. **Role Swap** - Synthesizer vs Devil's Advocate
4. **Temperature (0.3 vs 0.9)** - Conservative vs creative responses

Assignment requires running any 2 experiments.

## Output Format

Results are saved as JSON files in `results/` directory:

```json
{
  "config": {
    "topic": "...",
    "num_agents": 4,
    "num_rounds": 2,
    "temperature": 0.7,
    "model": "claude-3-5-sonnet-20241022",
    "agents": ["Researcher", "Critic", "Synthesizer", "Judge"]
  },
  "rounds": [
    {
      "round": 1,
      "output": "...",
      "duration": 45.2
    }
  ],
  "final_verdict": "...",
  "total_duration": 120.5,
  "timestamp": "2025-10-14T..."
}
```

## Key Design Decisions

### Why CrewAI?
- Role-based agent abstraction fits the debate structure
- Built-in task orchestration and sequencing
- Native support for Anthropic Claude
- Simpler than LangGraph for this use case

### Why Sequential Tasks?
- Debate requires strict ordering (argue → critique → synthesize)
- Each agent needs output from previous agents
- No parallel execution needed for this workflow

### Why JSON Storage?
- Preserves full debate transcript
- Easy to parse for analysis
- Human-readable for debugging
- Compatible with analysis tools

### Temperature Strategy
- Default 0.7: Balance between consistency and creativity
- Low (0.3): More factual, conservative arguments
- High (0.9): More creative, diverse perspectives

## Development Guidelines

### Adding New Agents
1. Define agent in `agents.py` with role, goal, and backstory
2. Create corresponding task in `tasks.py`
3. Update `get_debate_agents()` logic if needed
4. Consider impact on debate flow

### Adding New Experiments
1. Add function to `run_experiments.py`
2. Create two DebateConfig objects with different parameters
3. Run both debates and return results
4. Update main menu

### Modifying the Rubric
1. Update `RUBRIC_CRITERIA` in `config.py`
2. Update judge task description in `tasks.py`
3. Update analysis regex in `analyze_results.py`

### Testing Changes
1. Run single debate: `python debate.py`
2. Check console output for errors
3. Verify JSON results in `results/`
4. Run analysis: `python analyze_results.py`

## Common Issues

### Dependency Conflicts
- CrewAI requires `crewai-tools>=0.17.0`
- Use flexible version ranges in requirements.txt

### API Rate Limits
- Each debate makes multiple LLM calls
- Consider delays between experiments
- Monitor Anthropic API usage

### Memory Usage
- Full debate transcripts stored in memory
- Large experiments may need optimization

### Judge Score Extraction
- Judge must follow exact format: "Evidence: X/5"
- Regex parsing in analyze_results.py depends on format
- Instruct judge clearly in task description

## Assignment Deliverables Checklist

- [ ] Run 2 experiments (pick from 4 toggles)
- [ ] Capture screenshots showing ≥2 rounds + verdict
- [ ] Extract rubric scores from judge verdicts
- [ ] Document convergence status
- [ ] Note timing per round
- [ ] Collect 2-4 excerpts showing critique impact
- [ ] Create diagram of agent flow
- [ ] Write mini-report (1-2 pages)
- [ ] Create proof-of-concept slides (1 page or 2-4 slides)

## Future Enhancements

### Potential Improvements
1. **Memory System** - Agents remember insights across debates
2. **Parallel Critiques** - Multiple critics evaluate simultaneously
3. **Human-in-the-loop** - Allow user to inject questions mid-debate
4. **Visualization** - Real-time debate flow visualization
5. **Multi-topic** - Run same agents on different topics
6. **Consensus Detection** - Automatic convergence detection
7. **Argument Mapping** - Visual argument structure extraction

### Advanced Features
- Dynamic agent spawning based on debate complexity
- Meta-judge that evaluates judge quality
- Adversarial red team agent
- Citation tracking and fact-checking
- Export to different formats (PDF, markdown, slides)

## Tech Stack

- **Python 3.9+** - Core language
- **CrewAI** - Multi-agent orchestration framework
- **Anthropic Claude** - Large language model (3.5 Sonnet)
- **pydantic** - Configuration validation
- **python-dotenv** - Environment variable management

## Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required for Claude API access
```

## Usage Examples

### Quick Start
```bash
# Run default debate (4 agents, 2 rounds)
python debate.py
```

### Custom Configuration
```python
from config import DebateConfig
from debate import run_debate

config = DebateConfig(
    topic="Should AI systems be open source?",
    num_agents=4,
    num_rounds=3,
    temperature=0.5,
    include_devil_advocate=True
)

results = run_debate(config)
```

### Run All Experiments
```bash
# Run experiments 1, 2, 3, and 4
python run_experiments.py 1 2 3 4
```

### Analyze Results
```bash
python analyze_results.py
```

## Project Status

**Current Phase:** Implementation Complete
**Next Steps:** Run experiments and collect data for assignment deliverables

## Notes for Claude

- This is an academic project - focus on learning and experimentation
- The debate topic is deliberately nuanced to encourage rich discussion
- Agent prompts emphasize intellectual honesty and evidence-based reasoning
- Results should demonstrate both strengths and limitations of multi-agent systems
- Keep experiments lightweight - this is an MVP, not production system
