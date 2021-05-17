"""
@author: Yuzhuo Ma 31284922
email: ymaa0058@student.monash.edu

"""
# Question 1

def best_interval(transaction: bytearray, t: int) -> tuple:
    """
     Overall the total complexity of this function is limited by O(n*k),
     n is the number of elements in transactions
     k is the greatest number of digits in any element in transactions
     for the radix sort part is O(k*n) for the worst case
     for the check interval part is O(n*2) for the worst case, and can be limit be O(n)
     So the total complexity for this function is O(n)
    :param transaction: list of unsorted number
    :param t: integer number of interval
    :return: the tuple with two element tuple
    """

    # error handling
    if len(transaction) == 0:
        return 0, 0
    # start radix sort
    max_num = max(transaction)
    place = 1
    while max_num >= 10 ** place:
        place += 1
    # place is the k length regard for complexity
    for i in range(place):
        buckets = []
        for _ in range(10):
            buckets.append([])
        for num in transaction:
            radix = int(num / (10 ** i) % 10)
            buckets[radix].append(num)
        j = 0
        for k in range(10):
            for num in buckets[k]:
                transaction[j] = num
                j += 1
    result = []
    # end radix sort
    start_pointer = 0
    end_pointer = 0

    # error handling
    if t > max(transaction):
        return 0, len(transaction)
    for index_end in range(len(transaction)):
        if transaction[index_end] >= t:
            end_pointer = index_end
            break

    #  the main alogorithm of the interval check, it use end pointer as the anchor point, and loop the list
    #  and keep check the number of difference between the end pointer and start pointer to use as count
    #  the innside while is used for track the loop number and it will be constant complexity with is the
    #  length of the list for worse case.
    out = 0
    for i in range(len(transaction)):
        # when check to the last element, it should break the outside loop
        if i + 1 == len(transaction):
            end_pointer = i
            while transaction[start_pointer] < transaction[end_pointer] - t:
                out += 1
                start_pointer += 1
            count = end_pointer - start_pointer + 1
            up_bound = transaction[end_pointer]
            result.append((up_bound - t, count))
            break
        if transaction[i + 1] > transaction[end_pointer] and transaction[i + 1] != transaction[i]:
            end_pointer = i
            while transaction[start_pointer] < transaction[end_pointer] - t:
                out += 1
                start_pointer += 1
            count = end_pointer - start_pointer + 1
            up_bound = transaction[end_pointer]
            result.append((up_bound - t, count))
    max_index = 0
    print(out)
    # check the max count of the list
    for k in range(len(result)):
        if int(result[k][1]) > result[max_index][1]:
            max_index = k
    return result[max_index]


# Question 2

def radix_sort_for_tuple(obj_list, max_num):
    """
    radix sort for the tuple of the list, complexity is O(M*K), M is the length of the input list,
    k is the length of the largest element in list
    :param obj_list:
    :param max_num:
    :return:
    """
    digit_num = 1
    while max_num >= 10 ** digit_num:
        digit_num += 1
    for i in range(digit_num):
        buckets = []
        for index in range(10):
            buckets.append([])
        for num in range(len(obj_list)):
            radix = int(obj_list[num][1] / (10 ** i) % 10)
            buckets[radix].append(obj_list[num])
        j = 0
        for k in range(10):
            for num in buckets[k]:
                obj_list[j] = num
                j += 1


def rearrange_list(list):
    """
    this function is used for sorting the string inside the string list
    the complexity is O(M*27+M*K), and can be limited by O(M*K), M is the length of the input list,
    k is the length of the largest element in list

    :param list:
    :return:
    """
    original_list = list
    rearrange_list_1 = []
    for i in range(len(list)):
        digit_list = ""
        alphabet = [0] * 27
        # assign the digit to alphabet table in order to sort them , similar as count sort
        for m in list[i]:
            temp = ord(m) - 97
            alphabet[temp] += 1
        for _ in range(len(alphabet)):
            if alphabet[_] != 0:
                digit_list += alphabet[_] * (chr(_ + 97))
        rearrange_list_1.append((digit_list, original_list[i]))
    return rearrange_list_1


def merge_for_tuple(list1):
    """
    merge the number of list element to the list
    :param list1:
    :return:
    """
    list_for_tuple = []
    for i in list1:
        x = 0
        mult = 1
        for j in i[0]:
            x += mult * (ord(j) - 96)
            mult += 1
        list_for_tuple.append((i, x))
    return list_for_tuple


def words_with_anagrams(list1, list2):
    """
    Overall the total complexity of this function is limited by O(L1M1 + L2M2),
    L1 is the number of elements in list1
    L2 is the number of elements in list2
    M1 is the number of characters in the longest string in list1
    M2 is the number of characters in the longest string in list2
    for two times call of merge_for_tuple() function the worse case complexity is L1*M1 + L2*M2
    for two times call of radix_sort_for_tuple(), the worse case complexity is L1M1 + L2M2
    for the result list append part, the worse case complexity is limited by the O(M1+constant), because the inside loop
    will execute at most the number of the length of  result list times. so it can be seems as linear.
    So the overall complexity can be seems as O(L1*M1 + L2*M2+ L1*M1 + L2*M2 + M1+constant)
    So the total complexity for this function is O(L1*M1 + L2*M2)

    :param list1: the input string list
    :param list2: the input string list
    :return: A list of strings from list1 have at least one anagram appearing in list2
    """
    # error handling
    result = []
    if list1 == [] or list1 == ['']:
        return list1
    if list2 == [] or list2 == ['']:
        return list2
    # sort the string inside the string list
    list1 = rearrange_list(list1)
    list2 = rearrange_list(list2)

    # get the tuple for list
    list_for_1_tuple = merge_for_tuple(list1)
    list_for_2_tuple = merge_for_tuple(list2)

    # sort the string list
    radix_sort_for_tuple(list_for_1_tuple, 300)
    radix_sort_for_tuple(list_for_2_tuple, 300)


    # append result list and return, similar idea as Question1
    # because the inside loop will execute at most the number of the length of
    # result list times. so it can be seems as linear.
    # the inside loop here is like a pointer to avoid the inside loop because two list are sorted
    pointer = 0
    for k in range(len(list_for_1_tuple)):
        while list_for_1_tuple[k][1] > list_for_2_tuple[pointer][1]:
            pointer += 1
            if pointer > len(list_for_2_tuple) - 1:
                return result
        if list_for_1_tuple[k][1] == list_for_2_tuple[pointer][1]:
            result.append(list_for_1_tuple[k][0][1])
    return result


if __name__ == '__main__':
    list1 = ['spot', 'tops', 'dad', 'simple', 'dine', 'cats']
    list2 = ['pots', 'add', 'simple', 'dined', 'acts', 'cast']

    list = [11, 1, 3, 1, 4, 10, 5, 7, 10]
    test_list = [2511, 1222, 3333, 1343, 4224, 1028, 5227, 7322, 1022]
    transactions = [1615958206, 1615958306, 1615958406, 10, 566666]
    t = 1000
    expected = (1615957406, 3)
    print(best_interval([1, 5, 6], 5) == (1, 3))  # (0 - 5) contains 2 items but (1 - 6) contains 3 items
    print(best_interval([1, 5, 5], 5) == (0, 3))  # (0 - 5) contains 3 items
    print(best_interval([1, 5], 5) == (0, 2))  # (0 - 5) contains 2 items
    print(best_interval([1], 5) == (0, 1))  # (0 - 1) contains 1 items
    print(best_interval([1], 1) == (0, 1))  # (0 - 1) contains 1 items
    print(best_interval([1, 2, 3, 4, 5, 6, 7], 0) == (1, 1))
    print(best_interval([11, 1, 3, 1, 4, 10, 5, 7, 10], 5) == (0, 5))
    print(best_interval([11, 1, 3, 1, 4, 10, 5, 7, 10], 6) == (1, 6))
    print(best_interval([], 6) == (0, 0))
    print(best_interval([0], 2) == (0, 1))
    print(best_interval([0], 1) == (0, 1))
    print(best_interval([0], 4) == (0, 1))
    print(best_interval([0, 2, 3], 4) == (0, 3))
    print(best_interval([0, 2, 3], 0) == (0, 1))
    print(best_interval([0], 0) == (0, 1))
    print(best_interval([1], 1) == (0, 1))
    print(best_interval([0], 1) == (0, 1))
    print(best_interval([0, 0, 0, 0, 0], 1) == (0, 5))  #######
    print(best_interval(
        [11, 1, 3, 1, 4, 10, 5, 7, 10, 11, 11, 11, 12, 11, 11, 11, 13, 13, 13, 14, 14, 14, 14, 15, 15, 15, 15, 16],
        5) == (10, 21))
    print(best_interval([11, 1, 3, 1, 4, 10, 5, 7, 10], 11) == (0, 9))
    print(best_interval([1, 1, 1, 1, 1, 1, 1, 1], 0) == (1, 8))
    print(best_interval([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 0) == (2, 10))

    print(words_with_anagrams(list1, list2))