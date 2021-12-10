# Unoptimized version
def sort_debug(s_list):
    length = len(s_list)
    for i in range(length):
        for j in range(length - 1):
            if s_list[j] > s_list[j + 1]:
                s_list[j], s_list[j + 1] = s_list[j + 1], s_list[j]

    return s_list


# Optimized exit
def sort(s_list):
    length = len(s_list)
    while True:
        swapped = False
        for i in range(length - 1):
            if s_list[i] > s_list[i + 1]:
                s_list[i], s_list[i + 1] = s_list[i + 1], s_list[i]
                swapped = True
        if not swapped:
            return s_list
