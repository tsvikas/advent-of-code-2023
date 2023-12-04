import importlib
from time import time


def main() -> None:
    for day in range(1, 25 + 1):
        for part in ["a", "b"]:
            try:
                module = importlib.import_module(f"aoc2023.d{day}{part}")
            except ModuleNotFoundError:
                continue
            t_start = time()
            answer = module.main()
            t_end = time()
            t_ms = (t_end - t_start) * 1000
            print(f"[{t_ms:7.1f} ms] d{day}{part}: {answer}")


if __name__ == "__main__":
    main()
