def sequential_search(lst, target):

    for i, value in enumerate(lst):
        if value == target:
            return i
    return -1

def binary_search(lst, target):

    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1