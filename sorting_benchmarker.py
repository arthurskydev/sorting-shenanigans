"""A module with tools to test sorting functions."""

import random
import time
from typing import Callable


class BenchRuleset:
    """A class with properties that represent guidlines for the creation of unsorted lists."""


    def __init__(self, min_val: int, max_val: int, length: int) -> None:
        self.min_val = min_val
        self.max_val = max_val
        self.length = length


class BenchIncrementalRuleset(BenchRuleset):
    """A class with properties that represent guidlines for the creation of unsorted lists,
       especially for batch benchmarks."""
    iterations: int
    min_val_increment: int
    max_val_incement: int
    length_increment: int

    def __init__(
            self,
            baseMod: BenchRuleset,
            minValueChangePerIteration: int,
            maxValueChangerPerIteration: int,
            lenghthChangerPerIteration: int,
            iterations: int
        ) -> None:
        super().__init__(baseMod.min_val, baseMod.max_val, baseMod.length)
        self.iterations = iterations
        self.min_val_increment = minValueChangePerIteration
        self.max_val_incement = maxValueChangerPerIteration
        self.length_increment = lenghthChangerPerIteration

    def get_iteration(self, iteration: int) -> BenchRuleset:
        """Gets the values of the ruleset according to an iteration."""
        return BenchRuleset(
            self.min_val + self.min_val_increment * iteration,
            self.max_val + self.max_val_incement * iteration,
            self.length + self.length_increment * iteration)


class BenchmarkResult:
    """A class that represents the result of a benchmark."""
    title: str
    is_success: bool
    result_list: list[int]
    duration: int
    time_format_string: str

    def __init__(self, title: str, is_success: bool, result_list: list[int], duration: int,
                 time_format_string: str = "{:.4e}") -> None:
        self.title = title
        self.is_success = is_success
        self.result_list = result_list
        self.duration = duration
        self.time_format_string = time_format_string

    def __str__(self) -> str:
        duration_formatted = self.time_format_string.format(self.duration)
        string: str
        string = "--BENCHMARK RESULT--\n"
        string += f"TITLE {self.title}\n"
        string += "ORDER: "
        string += "CORRECT" if self.is_success else "INCORRECT"
        string += "\n"
        string += f"EXCECUTION TIME: {duration_formatted} NANOSECONDS\n"
        string += "-------------------------------------\n"
        return string


class BenchmarkBatchResult:
    """A class that represents the result of a batch benchmark."""
    title: str
    iterations: int
    success_ratio: float
    time: int
    average_time: int
    results: list[BenchmarkResult]
    time_format_string: str

    def __init__(self, title: str, result_list: list[BenchmarkResult],
                 time_format_string = "{:.4e}") -> None:
        self.title = title
        self.iterations = len(result_list)
        self.time = 0
        self.time_format_string = time_format_string

        n_success: int = 0
        for result in result_list:
            self.time += result.duration
            if result.is_success:
                n_success += 1

        self.success_ratio = round(n_success / self.iterations, 3)
        self.average_time = int(round(self.time / self.iterations, 3))

        self.results = result_list

    def get_times(self) -> list[int]:
        """Outputs a list of the times each iteration took to sort."""
        times: list[int] = []
        for result in self.results:
            times.append(result.duration)
        return times

    def __str__(self) -> str:
        total_time_formatted = self.time_format_string.format(self.time)
        average_time_formatted = self.time_format_string.format(self.average_time)
        string: str
        string = "--BATCH BENCHMARK RESULT--\n"
        string += f"TITLE: {self.title}\n"
        string += f"ITERATIONS: {self.iterations}\n"
        string += f"SUCCESS_RATE: {self.success_ratio}\n"
        string += f"TOTAL_EXEC_TIME: {total_time_formatted} NANOSECONDS\n"
        string += f"AVERAGE_EXEC_TIME: {average_time_formatted} NANOSECONDS\n"
        string += "-------------------------------------\n"
        return string


def error_check(input_list: list[int]) -> bool:
    """Check if list values are in acending order."""
    for i in range(len(input_list)-1):
        if input_list[i] > input_list[i + 1]:
            return False
    return True

def construct_unsorted_list(ruleset: BenchRuleset) -> list[int]:
    """Constructs a list with random values, given the parameters."""
    unsorted_list = []
    for _ in range(ruleset.length):
        unsorted_list.append(random.randint(ruleset.min_val, ruleset.max_val))
    return unsorted_list

class SortingBenchmarker:
    """Assign a sort function to an instance of this class,
       then use it to benchmark the sorting function"""
    sorting_func: Callable[[list[int]], list[int]]
    title: str

    def __init__(self,
                 title: str,
                 sorting_func: Callable[[list[int]], list[int]]):
        self.sorting_func = sorting_func
        self.title = title

    def run(self, ruleset: BenchRuleset = None,
            unordered_list: list[int] = None,) -> BenchmarkResult:
        """Run a single benchmark."""
        if unordered_list is None and ruleset is None:
            raise ValueError("Please provide a list to sort")
        if unordered_list is None and ruleset is not None:
            unordered_list = construct_unsorted_list(ruleset)
        is_success = True

        try:
            start_time = time.time_ns()
            result = self.sorting_func(unordered_list)
            end_time = time.time_ns()
            is_success = error_check(result)
        except:
            is_success = False

        return BenchmarkResult(self.title, is_success, result, end_time - start_time)

    def run_batch(self, ruleset: BenchIncrementalRuleset) -> BenchmarkBatchResult:
        """Run a series of benchmarks."""
        result_collection: list[BenchmarkResult] = []
        for i in range(ruleset.iterations):
            unsorted_list = construct_unsorted_list(ruleset.get_iteration(i))
            result = self.run(None, unsorted_list)
            result_collection.append(result)
        return BenchmarkBatchResult(self.title, result_collection)
