def merge_sort_asc(lst, index):
    if len(lst) > 1:
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]
        merge_sort_asc(left, index)
        merge_sort_asc(right, index)
        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            # 
            if left[i][index] <= right[j][index]:
                lst[k] = left[i]
                i += 1
                pass
            else:
                lst[k] = right[j]
                j += 1
                pass
            k += 1
            pass
        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1
            pass
        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1
            pass
        pass
    pass


def merge_sort_desc(lst, index):
    if len(lst) > 1:
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]
        merge_sort_desc(left, index)
        merge_sort_desc(right, index)
        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            #
            if left[i][index] >= right[j][index]:
                lst[k] = left[i]
                i += 1
                pass
            else:
                lst[k] = right[j]
                j += 1
                pass
            k += 1
            pass
        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1
            pass
        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1
            pass
        pass
    pass
