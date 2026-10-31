---
name: genpark-reasoning-mcts-step-verity-evaluator-skill
description: GenPark Reasoning MCTS Step Verity Evaluator - Implements Monte Carlo Tree Search (MCTS) Step-Level Process Reward Modeling (PRM) & Hallucination Branch Pruning.
category: Service
version: 1.0.0
license: MIT
tools:
  - execute_reasoning_mcts_step
---

# Genpark Reasoning Mcts Step Verity Evaluator Skill

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Genpark Reasoning Mcts Step Verity Evaluator Skill**.
Your primary directive is to execute: GenPark Reasoning MCTS Step Verity Evaluator - Implements Monte Carlo Tree Search (MCTS) Step-Level Process Reward Modeling (PRM) & Hallucination Branch Pruning.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `execute_reasoning_mcts_step`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `execute_reasoning_mcts_step`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
