"""CPU warm-up for the beginning of each gl3 measurement session."""

import argparse
import time


def fibonacci_work():
    a, b = 0, 1
    for _ in range(1000):
        a, b = b, (a + b) % 1_000_000_007
    return a


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120.0)
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("--seconds must be positive")

    start = time.monotonic()
    deadline = start + args.seconds
    batches = 0
    checksum = 0

    while time.monotonic() < deadline:
        checksum ^= fibonacci_work()
        batches += 1

    elapsed = time.monotonic() - start

    print(
        f"Fibonacci warm-up complete: "
        f"{elapsed:.2f} seconds, "
        f"{batches} batches, "
        f"checksum={checksum}",
        flush=True,
    )


if __name__ == "__main__":
    main()