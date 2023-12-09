# Helpers functions

import time


class Timer:
    """
    Context manager class to output
    elapsed time of functions
    """

    def __enter__(self):
        print(" -- start timer -- ")
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, type, value, traceback):
        self.elapsed = time.perf_counter_ns() - self.start
        print(f" -- elapsed time: {self.elapsed * 1.e-6:.3f} ms -- \n")
