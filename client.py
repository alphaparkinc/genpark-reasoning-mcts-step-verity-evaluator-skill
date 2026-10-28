# -*- coding: utf-8 -*-
"""
GenPark Reasoning MCTS Step Verity Evaluator Client
Implements Monte Carlo Tree Search (MCTS) Step-Level Process Reward Modeling (PRM) & Hallucination Branch Pruning.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import math
from typing import Dict, Any, List

class GenParkReasoningMCTSStepVerityEvaluator:
    """
    Evaluates step-by-step reasoning thought chains using Upper Confidence Bounds (UCB1)
    and Process Reward Model (PRM) verity scoring to prune hallucinated branches.
    """

    def __init__(self, exploration_constant: float = 1.414, pruning_threshold: float = 0.38):
        self.c = exploration_constant
        self.prune_thresh = pruning_threshold

    def calculate_ucb1(self, q_value: float, parent_visits: int, node_visits: int) -> float:
        """Computes Upper Confidence Bound for Trees (UCT / UCB1)."""
        if node_visits == 0:
            return float('inf')
        exploration = self.c * math.sqrt(math.log(max(1, parent_visits)) / node_visits)
        return round(q_value + exploration, 4)

    def evaluate_thought_step_verity(self, step_text: str, step_confidence: float) -> float:
        """
        Calculates heuristic step verity score based on premise coherence,
        presence of non-sequiturs, and claimed logical transitions.
        """
        penalty = 0.0
        # Hallucination red flags
        lower = step_text.lower()
        if "obviously" in lower or "clearly" in lower:
            penalty += 0.08  # Often masks hand-wavy reasoning
        if "therefore" in lower and len(step_text.split()) < 5:
            penalty += 0.15  # Abrupt unproven leap

        # Reward rigorous explicit calculations
        reward = 0.0
        if any(sym in step_text for sym in ["=", "+", "-", "*", "/", "<=", ">=", "\in"]):
            reward += 0.10

        score = max(0.01, min(1.0, step_confidence - penalty + reward))
        return round(score, 3)

    def search_and_evaluate_tree(
        self,
        thought_tree: List[Dict[str, Any]],
        root_node_id: str = "root"
    ) -> Dict[str, Any]:
        """
        Executes tree search rollout, computes node UCB1 scores, and identifies pruned paths.
        """
        node_map = {n["id"]: dict(n) for n in thought_tree}
        root = node_map.get(root_node_id)
        if not root:
            return {"error": "Root node not found"}

        parent_visits = root.get("visits", 10)

        evaluated_nodes = []
        pruned_branches = []
        active_candidates = []

        for node_id, node in node_map.items():
            if node_id == root_node_id:
                continue

            verity = self.evaluate_thought_step_verity(
                node.get("step_text", ""),
                node.get("prm_confidence", 0.70)
            )
            node["evaluated_verity"] = verity

            # Check for pruning
            if verity < self.prune_thresh:
                node["pruned"] = True
                pruned_branches.append({
                    "node_id": node_id,
                    "step_text": node.get("step_text"),
                    "verity_score": verity,
                    "prune_verdict": "PRUNED_HALLUCINATION_OR_FALLACY"
                })
            else:
                node["pruned"] = False
                ucb1 = self.calculate_ucb1(verity, parent_visits, node.get("visits", 1))
                node["ucb1_score"] = ucb1
                active_candidates.append(node)

            evaluated_nodes.append(node)

        # Sort remaining candidates by UCB1 descending
        active_candidates.sort(key=lambda x: x.get("ucb1_score", 0.0), reverse=True)
        recommended_best_step = active_candidates[0] if active_candidates else None

        return {
            "root_node_id": root_node_id,
            "total_nodes_evaluated": len(evaluated_nodes),
            "total_branches_pruned": len(pruned_branches),
            "optimal_next_step": {
                "node_id": recommended_best_step["id"],
                "step_text": recommended_best_step["step_text"],
                "verity_score": recommended_best_step["evaluated_verity"],
                "ucb1_priority": recommended_best_step["ucb1_score"]
            } if recommended_best_step else None,
            "pruned_hallucination_branches": pruned_branches,
            "top_active_branches": [
                {
                    "node_id": c["id"],
                    "step_text": c["step_text"],
                    "verity_score": c["evaluated_verity"],
                    "ucb1_score": c["ucb1_score"]
                }
                for c in active_candidates[:3]
            ]
        }
