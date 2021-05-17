def merge(left, right):
    """
    this is the merge step for the array
    :param left: left part array
    :param right: right part array
    :return:
    """
    res = []
    while left and right:
        min_val = left.pop(0) if left[0][1] < right[0][1] else right.pop(0)
        res.append(min_val)
    res += left if left else right
    return res


def merge_sort(obj_Array):
    """
    merge sort here take O(N*logN) time complexity, and O(N) space N is the length of the obj_Array
    :param obj_Array:
    :return:
    """
    if len(obj_Array) <= 1:
        res = obj_Array
    else:
        mid = len(obj_Array) // 2
        left, right = merge_sort(obj_Array[:mid]), merge_sort(obj_Array[mid:])
        res = merge(left, right)
    return res


def best_schedule(regular_work, special_events):
    """
    this function is used to maximise the amount of money the user can earn by comparing
     job as a personal trainer with participating in competitions, and the user will get the maximum profit by this.
    time complexity for this function is limited by O(N*log(N))
    and the space complexity is limited by O(N)
     N is the sum number of length of regular_work list and special_events.
    Actually in the function the time complexity is limited by O(M*logM) from merge sort
    and space complexity is limited by O(M) as well , M is the length of special_events.
    :param regular_work: is a list of non-negative integers,
    :param special_events: is a list of tuples,
    :return: an integer
    """
    # space complexity will be the O(N) - N is the length of the regular_work
    memo_array = [0] * (len(regular_work))
    if not regular_work:
        return 0
    # sort the special_events by the ending time of every event by merge sort, worst time complexity is
    # O(M*logM), and space complexity here is O(M) , M is the length of special_events.
    special_events = merge_sort(special_events)
    position = 0
    compare_b = 0
    memo_array[0] = regular_work[0]
    temp = 0
    events_zero_week = []
    # x here for present complexity
    x = 0
    # base case for first week, time complexity here is under N, because is only loop the event with the start time and
    # end time are 0
    # this part is used for update the first element of memo_array
    if special_events:
        # this while loop combine next while loop will only run the time of length of special_events
        while special_events[temp][0] == 0 and special_events[temp][1] == 0:
            # x here for present complexity
            x += 1
            events_zero_week.append(special_events[temp][2])
            temp += 1
            if temp == len(special_events):
                break
        if events_zero_week and max(events_zero_week) > regular_work[0]:
            memo_array[0] = max(events_zero_week)
    max_compare_b = 0
    # bottom up method,
    # total time complexity of this part function is O(N) -- from for loop,
    # inside while loop will be limited in linear
    # this part do not create any new space
    for i in range(1, len(regular_work)):
        # get the element in memo_array and regular work
        compare_a = regular_work[i] + memo_array[i - 1]
        if (special_events is not []) and (position != len(special_events)):
            # this while-loop only run the time of length of special_events
            while special_events[position][1] == i:
                x += 1
                # if there is case that special_events exist, get that number
                compare_b = memo_array[special_events[position][0] - 1] + special_events[position][2]
                # error handling if there are more than one event happen at same time
                if compare_b > max_compare_b:
                    max_compare_b = compare_b
                else:
                    compare_b = max_compare_b
                position += 1
                if position == len(special_events):
                    break
        # in each loop check if the regular work have higher profit, or do event have higher profit
        max_compare_b = 0
        memo_array[i] = max(compare_a, compare_b)
    # result will always be the last element of array
    result = memo_array[len(memo_array) - 1]
    return result


weekly_income = [3, 7, 2, 1, 8, 4, 5]
competitions = [(1, 3, 15), (2, 2, 8), (0, 4, 30), (3, 5, 19)]


print(best_schedule(weekly_income, competitions)== 42)


def best_itinerary(profit, quarantime_time, home):
    """
    this function is used for user to plan the maximum amount of money he can earn by working in days and
    this combine whether travel to the other city to work or stay working in same city can get higher profit.
    here inside function we create the 2 n*d size array, so the space complexity will be limited by O(nd)
    for complexity, it was also limited by O(nd). and the detailed time complexity is presented before every
    part of loop, so O(n)+O(nd)+O(nd)+O(nd)+O(nd)+O(n) so limited by O(nd)
    where n is the number of cities, and d is the number of days
    :param profit:  is a list of lists, All interior lists are length n. Each interior list represents a differ- ent day
    :param quarantime_time: is a list of non-negative integers
    :param home: is an integer between 0 and n-1 inclusive
    :return: an integer
    """
    # base case and create DP list
    DP_list = []
    total_travel_cost = []
    # get the total cost of the list
    # base case for 0 city
    if len(profit) == 0:
        return 0
    # this part is used for writing 0 to the list that sales can not arrive
    # time complexity here is O(n)  n is the number of cities
    for city in range(len(profit[0])):
        total_travel_cost.append((abs(home - city)) + quarantime_time[city] + 1)
    # create list and give -1 as sign to present the place that not calculated
    # time complexity here is O(nd)  n is the number of cities, d is the number of days
    for day in range(len(profit)):
        DP_list.append([])
        for city in range(len(profit[day])):
            DP_list[day].append(-1)
    count = 0
    # write 0 for the place that the sales can not arrive
    # time complexity here is limited by O(nd), n is the number of cities, d is the number of days
    for city in range(len(profit[0])):
        count += 1
        for days in range(len(profit)):
            if days != total_travel_cost[count - 1] and city != home:
                DP_list[days][city] = 0
            else:
                break
    # base case
    # write the first two day that sales will get the max profit
    DP_list[0][home] = profit[0][home]
    if len(profit) > 1:
        DP_list[1][home] = profit[0][home] + profit[1][home]

    # base case for only 1 city
    if len(profit[0]) == 1:
        result = 0
        for i in range(len(profit)):
            result += profit[i][0]
        return result
    # create the n*d size array that will store how much the sales can get from continues travel
    #  time complexity here is limited by O(nd), n is the number of cities, d is the number of days
    continue_travel_list = [[0 for i in range(len(profit[0]))] for j in range(len(profit))]
    # DP approach bottom up
    #  time complexity here is limited by O(nd), n is the number of cities, d is the number of days
    for day in range(1, len(profit)):
        for city in range(len(profit[0])):
            left_part = 0
            right_part = 0
            # for edge case
            if city == 0:
                # check if the less than 2 days, avoid index out of range
                if day < 2 or day - 2 - quarantime_time[city] < 0:
                    left_part = DP_list[day - 1][city]
                    # left_part = max(DP_list[day - 1][city][0], profit[day][city])
                else:
                    # every part here will compare with the (Maximum gain without going through the quarantine period)
                    # and  (Maximum gain from having experienced the quarantine period)
                    left_part = max(DP_list[day - 1][city], DP_list[day - (2 + quarantime_time[city])][city + 1],
                                    continue_travel_list[day - (2 + quarantime_time[city])][city + 1])
                right_part = max(continue_travel_list[day - 1][city + 1], DP_list[day - 1][city + 1])
            # for edge case
            elif city == (len(quarantime_time) - 1):
                # check if the less than 2 days, avoid index out of range
                if day < 2 or day - 2 - quarantime_time[city] < 0:
                    left_part = DP_list[day - 1][city]
                else:
                    left_part = max(DP_list[day - 1][city], DP_list[day - (2 + quarantime_time[city])][city - 1],
                                    continue_travel_list[day - (2 + quarantime_time[city])][city - 1])
                right_part = max(continue_travel_list[day - 1][city - 1], DP_list[day - 1][city - 1])
            # for normal case that check adjecnt city
            else:
                # check if the less than 2 days, avoid index out of range
                if day < 2 or (day - 2 - quarantime_time[city]) < 0:
                    left_part = DP_list[day - 1][city]
                else:
                    # every part here will compare with the (Maximum gain without going through the quarantine period)
                    # and  (Maximum gain from having experienced the quarantine period)
                    left_part = max(DP_list[day - 1][city],
                                    DP_list[day - 2 - quarantime_time[city]][city - 1],
                                    DP_list[day - 2 - quarantime_time[city]][city + 1],
                                    continue_travel_list[day - (2 + quarantime_time[city])][city - 1],
                                    continue_travel_list[day - (2 + quarantime_time[city])][city + 1])
                right_part = max(continue_travel_list[day - 1][city - 1], DP_list[day - 1][city - 1],
                                 DP_list[day - 1][city + 1], continue_travel_list[day - 1][city + 1])

            # check if the first day travel or not， if travel, check if larger update the dp list
            if day == abs(home - city) + quarantime_time[city] and city != home:
                if left_part < profit[day][city] and abs(home - city) <= day:
                    left_part = profit[day][city]

            #     update the DP_list and continue_travel_list
            # for keep traveling we will not update the DP_list, we only get the max previous dp_list
            if DP_list[day][city] == 0:
                DP_list[day][city] = left_part
                continue_travel_list[day][city] = right_part
            #     need consider the add number if sales do not keep traveling
            else:
                DP_list[day][city] = left_part + profit[day][city]
                continue_travel_list[day][city] = right_part
    # find the max of the last list 2d DP_list, and complexity here is O(n) where n is the number of cities
    max_tuple = max(DP_list[-1])
    return max_tuple


quarantine = [3, 1, 1, 1, 1]

profit = [[6, 9, 7, 5, 9],
          [4, 7, 3, 10, 9],
          [7, 5, 4, 2, 8],
          [2, 7, 10, 9, 5],
          [2, 5, 2, 6, 1],
          [4, 9, 4, 10, 6],
          [2, 2, 4, 8, 7],
          [4, 10, 2, 7, 4]]

print(best_itinerary(profit, quarantine, 0))
