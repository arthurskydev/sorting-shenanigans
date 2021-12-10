import algoBenchmarker
from algoBenchmarker import AlgoBenchmarker
import bubbleSort

# Sort function must only take a list as the only parameter, and it must return a list.

# Create a new benchmarker for a sort function.
bubbleBenchmarker = AlgoBenchmarker(bubbleSort.sort, "BUBBLE SORT")

# Create a ruleset that the benchmarker can use to make unsorted lists.
# Parameters:
# min value, increment
# max value, increment
# length, increment
# number of iterations
ruleset = algoBenchmarker.construct_ruleset(0, 0, 100, 0, 1000, 0, 100)

# Run a batch benchmark.
# First parameter "True" will print the result to the console in a formatted style.
_ = bubbleBenchmarker.run_batch_benchmark(True, ruleset, False)
