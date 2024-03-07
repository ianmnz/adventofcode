# Helpers functions

import time
from functools import wraps
from typing import List, Callable, TypeVar
from typing_extensions import ParamSpec     # After 3.10, import directly from typing

R = TypeVar("R")    # Callable return type
P = ParamSpec("P")  # Callable parameters type

class Timer:
    """
    Context manager class to output
    elapsed time of functions
    """

    @staticmethod
    def _print(header: str, elapsed_in_ns: int = 0) -> None:
        print(f" -- {header:<35} : {elapsed_in_ns * 1.e-6:>10.3f} ms -- ")

    @staticmethod
    def timeit(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter_ns()
            res = func(*args, **kwargs)
            end = time.perf_counter_ns()
            Timer._print(f"{func.__name__!r} took", end - start)
            return res
        return wrapper

    def __init__(self) -> None:
        self.checkpoints: List[int] = []

    def __enter__(self):
        self._print("start timer")
        self.checkpoints.append(time.perf_counter_ns())
        return self

    def step(self, checkpoint: str = "step") -> None:
        self.checkpoints.append(time.perf_counter_ns())
        self._print(f"{checkpoint}", self.checkpoints[-1] - self.checkpoints[-2])

    def __exit__(self, type, value, traceback) -> None:
        self.checkpoints.append(time.perf_counter_ns())
        if len(self.checkpoints) > 2:
            self._print('end timer', self.checkpoints[-1] - self.checkpoints[-2])
        self._print('total elapsed time', self.checkpoints[-1] - self.checkpoints[0])
