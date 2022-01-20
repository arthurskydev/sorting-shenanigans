"""Demonstration of the sorting function benchmarker."""

from sorting_benchmarker import SortingBenchmarker, BenchRuleset, BenchIncrementalRuleset
import bubble_sort

# Not multithreaded.

# Run a single benchmark.
# Create a benchmarker.
bubble_benchmarker = SortingBenchmarker("BUBBLE SORT", bubble_sort.sort)

# Create a guidline for the random unsorted list generator:
# Example:
# Mininmum value: 0
# Maximum value: 1000
# Positions in list: 1000
ruleset = BenchRuleset(0, 1000, 1000)

# Run the benchmark.
result = bubble_benchmarker.run(ruleset)

# Print a formatted version of the result.
print(result)

# Batch benchmark example:
# Base values from "ruleset"
# Increment minValue by 0,
# maxVal by 10,
# length by 10,
# Do 100 iterations.
batch_rules = BenchIncrementalRuleset(ruleset, 0, 100, 100, 10)

# Run batch.
batch_result = bubble_benchmarker.run_batch(batch_rules)

# Formatted print.
print(batch_result)

# Output a list of the times each iteration took.
times = batch_result.get_times()
print(times)
