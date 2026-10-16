
import argparse
import importlib.util
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent.parent


def load_solution(path):
    spec = importlib.util.spec_from_file_location("benchmark_solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Solution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--treatment",
        choices=["original", "modified"],
        required=True,
    )
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--problem", type=int, default=322)
    parser.add_argument("--variant", type=int, choices=[1, 2, 3], default=1)
    args = parser.parse_args()

    if args.problem != 322 or args.variant != 1:
        parser.error(
            "Only problem 322, variant 1 is implemented in this pilot"
        )

    if args.iterations < 1:
        parser.error("--iterations must be positive")

    folder = (
        "baseline"
        if args.treatment == "original"
        else "guideline-adherent"
    )

    path = (
        ROOT
        / "problems_nikola"
        / folder
        / "322_coin_change"
        / f"problem_{args.variant}.py"
    )

    Solution = load_solution(path)

    # Fixed, deterministic input.
    original_coins = [1, 2, 5]
    target = 11

    # Warm-up outside the timed loop.
    assert Solution.coinChange(original_coins.copy(), target) == 3

    start = time.perf_counter()

    for _ in range(args.iterations):
        # Fresh list because the solution modifies its input.
        coins = original_coins.copy()
        result = Solution.coinChange(coins, target)

        if result != 3:
            raise RuntimeError(f"Unexpected result: {result}")

    elapsed = time.perf_counter() - start

    print(f"Treatment: {args.treatment}")
    print(f"Iterations: {args.iterations}")
    print(f"Elapsed time: {elapsed:.6f} seconds")
    print("Validation: PASS")


if __name__ == "__main__":
    main()
