from __future__ import annotations

from agent_factory import build_agent_executor


def run_examples() -> None:
    agent_executor = build_agent_executor()

    queries = [
        "What will be the date 45 days from today?",
        "Analyze this paragraph and summarize the sentiment: I love the UI but I hate the slow loading time.",
        "What is (234 × 12) + 98?",
        "Calculate the total cost if I buy 3 items priced at 499 each, and tell me the delivery date if shipping takes 7 days.",
        "What is today’s weather in Chandigarh and suggest clothing accordingly.",
    ]

    for q in queries:
        print("\n" + "=" * 90)
        print("USER:", q)

        result = agent_executor.invoke({"input": q})

        print("\nFINAL ANSWER:\n", result.get("output"))

        steps = result.get("intermediate_steps", [])
        if steps:
            print("\nINTERMEDIATE STEPS (raw):")
            for i, step in enumerate(steps, start=1):
                print(f"\n--- Step {i} ---")
                print(step)


if __name__ == "__main__":
    run_examples()
