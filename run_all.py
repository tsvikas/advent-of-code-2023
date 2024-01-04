import importlib
from time import time


def main() -> None:
    solve_times: dict[str, float] = {}
    for day in range(1, 25 + 1):
        solve_times[f"d{day}"] = 0
        for part in ["a", "b"]:
            try:
                module = importlib.import_module(f"aoc2023.d{day}{part}")
            except ModuleNotFoundError:
                continue
            t_start = time()
            answer = module.solution.solve()
            t_end = time()
            t_ms = (t_end - t_start) * 1000
            solve_times[f"d{day}"] += t_ms
            print(f"[{t_ms:7.1f} ms] d{day}{part}: {answer}")

    print("\nMost time-consuming:")
    for day, solve_time in sorted(
        solve_times.items(), key=lambda x: x[1], reverse=True
    )[:5]:
        print(f"{day}: {solve_time:7.1f} ms")


if __name__ == "__main__":
    main()
