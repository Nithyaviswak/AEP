import os
import random  
from typing import Dict, Any

class AutomaticPromptEngineer:
    def __init__(self, api_key: str, mock: bool = False):
        self.api_key = api_key
        self.mock = mock

    def run(
        self,
        task: str,
        n_variations: int = 5,
        top_k: int = 2,
        idea: str = None,
        expected_output: str = None
    ) -> Dict[str, Any]:
        """Run the whole pipeline: generate, evaluate, refine."""
        print("--- Starting the APE process ---")
        if idea is None:
            idea = input("💡 Do you have an idea for how the prompt should be phrased? (Press Enter to skip) ") or None
        if expected_output is None:
            expected_output = input("📄 What kind of output do you expect? (Press Enter to skip) ") or None

        print("\n[1] Generating prompt variations...")
        prompts = self.generate_prompt_variations(task, n=n_variations, idea=idea)
        
        print(f"\n[2] Evaluating {len(prompts)} prompts...")
        results = self.evaluate_prompts(prompts, task, expected_output=expected_output)
        
        print(f"\n[3] Refining top {top_k} prompts...")
        refined_prompts = self.refine_prompts(results, top_k=top_k)
        print("\n--- APE process complete ---")

        return {
            "initial_prompts": prompts,
            "evaluations": results,
            "refined_prompts": refined_prompts
        }

    def generate_prompt_variations(self, task: str, n: int, idea: str):
        """
        Generates diverse prompt variations using a more robust method.
        """
        settings = [
            "on a scenic mountain road", "in a bustling city at night", "parked by a serene lake",
            "speeding on a futuristic highway", "in a rustic countryside setting", "at a modern auto show",
            "covered in morning dew in a forest", "in an underground garage"
        ]
        styles = [
            "highly detailed 8k photograph", "cinematic shot", "advertisement style",
            "vintage photo effect", "digital art", "concept art", "Blueprint schematics",
            "watercolor painting"
        ]
        details = [
            "with glossy paint reflecting the environment", "showcasing the interior", "with headlights on",
            "splashing through a puddle", "from a low-angle perspective", "in motion blur",
            "highlighting the alloy wheels", "covered in light snow"
        ]

        generated_prompts = []
        for i in range(n):
            prompt_parts = {task}
            if idea:
                prompt_parts.add(idea)

            prompt_parts.add(random.choice(settings))
            prompt_parts.add(random.choice(styles))
            prompt_parts.add(random.choice(details))

            prompt_parts.discard("")
            prompt_parts.discard(None)

            final_prompt = ", ".join(sorted(list(prompt_parts)))
            generated_prompts.append(final_prompt)

        return generated_prompts

    def evaluate_prompts(self, prompts, task, expected_output):
        return [{"prompt": p, "output": f"Mock output for {p}", "score": 10 - i} for i, p in enumerate(prompts)]

    def refine_prompts(self, results, top_k):
        top_results = sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]
        return [r['prompt'] for r in top_results]

def run_demo(mock: bool = True):
    """Run a demonstration of the APE pipeline."""
    api_key = os.getenv("OPENAI_API_KEY") 

    task_description = input("📝 What task do you want the AI to perform? ")
    
    ape = AutomaticPromptEngineer(api_key=api_key, mock=mock)

    result = ape.run(task_description, n_variations=7)

    print("\n✅ Final Results\n" + "="*20)
    print("\nInitial Prompts:")
    for p in result["initial_prompts"]:
        print("-", p)

    print("\nEvaluations:")
    for r in result["evaluations"]:
        print(f"Prompt: {r['prompt']}\nOutput: {r['output']}\nScore: {r['score']}\n")

    print("\nRefined Prompts:")
    for rp in result["refined_prompts"]:
        print("-", rp)

if __name__ == "__main__":
    run_demo(mock=True)