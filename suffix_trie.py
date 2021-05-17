"""
@author Yuzhuo Ma 31284922
email: ymaa0058@student.monash.edu
"""
class TrieNode:
    def __init__(self, char):
        """
        init method for TrieNode, contain count, max_string, isEnd, next_nodelist, father, char, max_node
        :param char:
        """
        self.count = 0
        self.max_string = ""
        self.next_nodelist = [None] * 5
        self.father = None
        self.char = char
        self.max_node = None


class SequenceDatabase:
    """
    database for various different drug resistant gene sequences over the course of the study.
    """

    def __init__(self):
        """
        init method for the SeqeunceDatabase, set the root node with "", constructor
        """
        self.root = TrieNode("")

    def addSequence(self, s: str):
        """
        main method of adding node, the total time complexity of this functionality is O(len(s)), s is the input string,
        the max complexity happen in the for loop and while loop, for the for-loop, it will loop the len(s) time to add
        node or update node,  for the while-loop it will loop back to the root node, from bottom which is
        len(s)+1 time, (can e limited into len(s)) the plus one is the root.
        So, the over all complexity of this function is O(len(s)+O(len(s))) => limited to O(len(s))

        :param s: object list
        :return: this method will not return anything, but only add the node to the prefix trie
        """
        node = self.root
        inside = False
        s += "$"
        for char in range(len(s)):
            ind = int(ord(s[char]) - ord("A"))
            if s[char] == "$":
                ind = 4
            # if can not find the node, create new node for the  children list
            if node.next_nodelist[ind] is None:
                # create node
                node.next_nodelist[ind] = TrieNode(s[char])
                node.next_nodelist[ind].father = node
            else:
                # update count of the node
                node.next_nodelist[ind].count += 1
            # update the node
            node = node.next_nodelist[ind]
            temp_string = node.char
        # after finish the add method, we need traverse back to update the max_string which will be used for query
        # the worse case time complexity of this while loop is O(len(s)) s is the input string

        # oncemore is loop one more times for updating the root
        oncemore = iter([True, False])
        while (node.father is not None) or next(oncemore):
            # if this node's father is not none means this node have be written before we need check the condition to
            # update the string
            # if node has no father node, break the loop
            if node.father is None:
                break
            if node.father.max_node is not None:
                # condition here is for checking if the incoming node's count greater than the original max_string's count
                # or equal but have smaller lexicographically order, we need to update the original list's max string
                if node.count > node.father.max_node.count or (inside is True) or (
                        node.count == node.father.max_node.count and node.char < node.father.max_node.char):
                    # if the string inside the list get update, which means the all the father node need to update
                    inside = True
                    # update the max_string of the father node and update temp node
                    node.father.max_node = node
                    node.father.max_string = temp_string
                temp_string = node.father.char + temp_string
                node = node.father
            else:
                # only do once, for updating the node of max_string in the trie
                # update the max_string of the father node and update temp node
                node.father.max_node = node
                node.father.max_string = temp_string
                # update the temp_string
                temp_string = node.father.char + temp_string
                node = node.father

    def query(self, q):
        """
        query method, will return the higher frequency string in the database, or same frequency, but smaller
         lexicographically one. the time complexity if this function is (len(q)), happen in the for -loop, it will loop
         the input string and get the last node, and result will keep update the string and add that max_string in the
         node.
        :param q: the prefix string
        :return: higher frequency string in the database, or same frequency, but smaller lexicographically.
        """
        node = self.root
        # base case of "" input and no "string in the database"
        if q == "" and node.max_string == "$":
            return None
        # base case of "", return the max_string in root
        if q == "":
            result = node.max_string
            return result[:-1]
        result = ""
        # loop the q until the last index to get that max_string
        for index in range(len(q)):
            ind = int(ord(q[index]) - ord("A"))
            # update result
            result += q[index]
            # if string not found
            if node.next_nodelist[ind] is None:
                return None
            node = node.next_nodelist[ind]
        result += node.max_string
        return result[:-1]


seq = SequenceDatabase()


class TrieNode_Q2:
    """
    trie node for Question 2, some attribute is not needed, and need an exist list here
    """

    def __init__(self, char):
        self.next_nodelist = [None] * 5
        self.char = char
        self.index = 0
        self.exist_list = []


class suffix_trie():
    def __init__(self):
        """
        init method for the suffix_trie, set the root node with "", constructor
        """
        self.root = TrieNode_Q2("")

    def suffix_trie_creater(self, string, index):
        """
        create the suffix trie, complexity of this function is O(len(string)), in for loop. and update the father node,
        node index,  exist_list and count for the suffix trie
        :param string:
        :param index:
        :return: do not return anything
        """
        node = self.root
        for char in range(len(string)):
            ind = int(ord(string[char]) - ord("A"))
            if string[char] == "$":
                ind = 4
            if node.next_nodelist[ind] is None:
                # create node
                node.next_nodelist[ind] = TrieNode_Q2(string[char])
                # update the index of the node
                node.next_nodelist[ind].index = index
                # update the new same character to the exist list
            node.next_nodelist[ind].exist_list.append(index)
            #     update the node
            node = node.next_nodelist[ind]

    def find_string(self, string, string1_result_node):
        """
        find method,check if the string input is in the list or not, if not return None, if exist, return the
        next node of the string input.  the complexity of this function is O(len(string)) in for-loop
        :param string:
        :param string1_result_node:
        :return:  if the string input not in the list,  return None, else, return next node of the string input.
        """
        node = string1_result_node
        for i in range(len(string)):
            ind = int(ord(string[i]) - ord("A"))
            if string[i] == "$":
                ind = 4
            #     if can not find the result, return NOne
            if node.next_nodelist[ind] is None:
                return None
            node = node.next_nodelist[ind]
        return node


class OrfFinder:
    """
    the class variable for the input string
    """
    obj_string = None

    def __init__(self, string):
        """
        init method of the OrfFinder, it will process the input string to the suffix trie. the complexity of this function
        is O(N^2), N is the length of the input string, the first for-loop will loop the length of string(N), and the list
        slicing will have the N complexity, the the first for loop complexity is O(N^2), the second for-loop, will traverse
        all the number of suffix in suffix string, so O(N), and the suffix_trie_creater will take O(N) time to add node
        to the trie, so total complexity is O(N^2), O(N^2)+O(N^2) => the time complexity limited to O(N^2)

        :param string:
        """
        self.obj_string = string
        string = string + "$"
        stringlist = []
        for i in range(len(string)):
            stringlist.append(string)
            # slice the string to get suffix
            string = string[1:]
        #     create the object of suffix_trie
        self.suffix_trie_obj = suffix_trie()
        # print(stringlist)
        for j in range(len(stringlist)):
            # add the string into suffix trie
            self.suffix_trie_obj.suffix_trie_creater(stringlist[j], j)

    def find(self, start_string, end_string):
        """
        will return the list contain all the string with start_string as prefix and end_string as end string.
        the complexity will be the length of the input start_string and the length of end_string, and the number of the
        eligible output. if we can not find the result, just return []
        for the first find_string, it will do the O(len(start_string)) time,
        for the second find_string, it will do the O(len(end_string)) time.
        after this, there is a nested for-loop withe the filter while loop, the the total complexity of that part is
        O(U) U is the length of the output list,
        The overall complexity is O(len(start_string) + len(end_string) + U )
        :param start_string: prefix
        :param end_string: end of string
        :return: the result list that contain all the string with start_string as prefix and end_string as end string
        """
        node = self.suffix_trie_obj.root
        # find the node after the last node of start_string
        index_start = self.suffix_trie_obj.find_string(start_string, node)
        result = []
        # base case
        if index_start is None:
            return []
        index_start = index_start.exist_list
        # find the node after the last node of end_string
        index_end = self.suffix_trie_obj.find_string(end_string, node)
        # base case
        if index_end is None:
            return []
        index_end = index_end.exist_list

        # this part is for traversing the list and return, it meet the complexity because the while loop have filter
        # it will check if the list do not meet the requirement, just skip. so the total complexity is the U which is the
        # length of the output list.
        for start in index_start:
            count = 0
            reverse = len(index_end)-1
            # filter for the number that end smaller than start
            while count < len(index_end) and index_end[reverse] > start:
                # string output with the length of end_string place
                string = self.obj_string[start:index_end[reverse] + len(end_string)]
                # check for the overlap, if string length not smaller than start_string and end_string, append
                if len(string) >= (len(start_string)+len(end_string)):
                    result.append(string)
                count += 1
                reverse -= 1
        return result


genome1 = OrfFinder("AAAA")
print(genome1.find("A", "A"))

