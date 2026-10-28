# -*- coding: utf-8 -*-
"""
Example usage of GenParkReasoningMCTSStepVerityEvaluator
Demonstrates MCTS step selection and automated hallucination branch pruning.
"""

from client import GenParkReasoningMCTSStepVerityEvaluator

def main():
    evaluator = GenParkReasoningMCTSStepVerityEvaluator(exploration_constant=1.414, pruning_threshold=0.40)

    sample_tree = [
        {"id": "root", "visits": 25},
        {
            "id": "branch-A",
            "step_text": "Assume f(x) is continuous on [a, b]. By the Intermediate Value Theorem, there exists c such that f(c) = 0.",
            "prm_confidence": 0.94,
            "visits": 8
        },
        {
            "id": "branch-B",
            "step_text": "Obviously therefore the solution is trivial and f(x) = x^2 without justification.",
            "prm_confidence": 0.32,
            "visits": 2
        },
        {
            "id": "branch-C",
            "step_text": "Compute derivative f'(x) = 2x - 4. Set f'(x) = 0 to find critical point x = 2.",
            "prm_confidence": 0.91,
            "visits": 6
        }
    ]

    res = evaluator.search_and_evaluate_tree(sample_tree, "root")

    print("================================================================")
    print("GenPark Reasoning MCTS Step Verity Evaluator - Live Runs")
    print("================================================================\n")
    print(f"Total Nodes Evaluated : {res['total_nodes_evaluated']}")
    print(f"Hallucinations Pruned : {res['total_branches_pruned']}\n")

    if res['optimal_next_step']:
        opt = res['optimal_next_step']
        print(f"Optimal Next Step     : [{opt['node_id']}] (Verity: {opt['verity_score']}, UCB1: {opt['ucb1_priority']})")
        print(f"  Step Text           : {opt['step_text']}\n")

    print("Pruned Branches:")
    for pb in res['pruned_hallucination_branches']:
        print(f"  [X] [{pb['node_id']}] Verity: {pb['verity_score']} -> {pb['step_text']}")

if __name__ == "__main__":
    main()
