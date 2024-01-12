# Helpers functions

import time
from typing import List


class Timer:
    """
    Context manager class to output
    elapsed time of functions
    """

    @staticmethod
    def _print(header: str, elapsed_in_ns: int = 0) -> None:
        if not elapsed_in_ns:
            print(f" -- {header} -- ")
        else:
            print(f" -- {header} : {elapsed_in_ns * 1.e-6:.3f} ms -- ")

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
        self._print('total elapsed', self.checkpoints[-1] - self.checkpoints[0])
