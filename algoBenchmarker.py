import random
import time


def error_check(s_list):
    for i in range(len(s_list)-1):
        if s_list[i] > s_list[i + 1]:
            return False
    return True


def construct_unsorted_list(min_v, max_v, length):
    t_list = []
    for _ in range(length):
        t_list.append(random.randint(min_v, max_v))
    return t_list


def construct_ruleset(min_v, min_v_incs, max_v, max_v_incs, length, length_incs, steps):
    return steps, min_v, min_v_incs, max_v, max_v_incs, length, length_incs


def construct_bm_result(title, is_success, result, duration):
    return title, is_success, result, duration


def construct_batch_bm_result(title, r_col):
    average_time = 0
    success_count = 0
    length = len(r_col)
    for i in r_col:
        average_time += i[3]
        if i[1]:
            success_count += 1

    average_time /= length
    return title, (success_count, length), r_col, average_time


def print_bm(result):
    print("ALGORITHM NAME:", result[0])
    if result[1]:
        print("THE ALGORITHM SUCCEEDED")
    else:
        print("SORTED ARRAY CONTAINS MISTAKES")
    print("EXECUTION TIME TOOK:", result[3], "NANOSECONDS")
    print("-------------------------------------")


def print_batch_bm(result):
    print("--BATCH BENCHMARK--")
    print("ALGORITHM NAME:", result[0])
    print(result[1][1], "ITERATIONS")
    print("SUCCESS RATE:", result[1][0], "/", result[1][1])
    print("AVERAGE EXECUTION TIME:", result[3], "NANOSECONDS")
    print("-------------------------------------")


class AlgoBenchmarker:
    def __init__(self, s_func, algo_name, t_list=None):
        self.s_func = s_func
        self.algo_name = algo_name
        self.t_list = t_list

    def make_t_list(self, min_v, max_v, length, t_list=None):
        if t_list is not None:
            self.t_list = t_list
            return
        self.t_list = construct_unsorted_list(min_v, max_v, length)

    def run_benchmark(self, do_print, t_list=None):
        if self.t_list is None and t_list is None:
            raise ValueError("No unsorted list found (t_list)")
        if t_list is None:
            t_list = self.t_list
        start_time, result, end_time = 0, 0, 0
        try:
            start_time = time.time_ns()
            result = self.s_func(t_list)
            end_time = time.time_ns()
        except Exception as ex:
            print("An error occurred during sort:")
            print(ex)
        duration = end_time - start_time
        is_success = error_check(result)
        bm_res = construct_bm_result(self.algo_name, is_success, result, duration)
        if do_print:
            print_bm(bm_res)
        return bm_res

    def run_batch_benchmark(self, do_print, t_ruleset, do_deeplog):
        result_collection = []
        for i in range(t_ruleset[0]):
            t_list = construct_unsorted_list(t_ruleset[1] + t_ruleset[2] * i,
                                             t_ruleset[3] + t_ruleset[4] * i,
                                             t_ruleset[5] + t_ruleset[6] * i)
            result_collection.append(self.run_benchmark(do_deeplog, t_list))
        result = construct_batch_bm_result(self.algo_name, result_collection)
        if do_print:
            print_batch_bm(result)
        return result
