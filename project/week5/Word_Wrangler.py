def remove_duplicates(list1):
	"""
	Eliminate duplicates in a sorted list.

	Returns a new sorted list with the same elements in list1, but
	with no duplicates.

	This function can be iterative.
	"""
	if len(list1) == 0:
		return list1
	results = [list1[0]]
	for item in list1:
		if item != results[-1]:
			results.append(item)
	return results

def intersect(list1, list2):
	"""
	intersect should return a new sorted list that contains only 
	the elements that are in both input lists, list1 and list2.
	"""
	index1 = 0
	index2 = 0
	interlist = []
	while index1 != len(list1) and index2 != len(list2):
		if list1[index1] == list2[index2]:
			interlist.append(list1[index1])
			index1 += 1
			index2 += 1
		elif list1[index1] < list2[index2]:
			index1 += 1
		elif list2[index2] < list1[index1]:
			index2 += 1
	return interlist

def merge(list1, list2):
	"""
	merge should return a new sorted list that 
	contains all of the elements in either list1 and list2.
	"""
	merged_list = []
	index1 = 0
	index2 = 0
	list_tmp1 = list1[:]
	list_tmp2 = list2[:]
	list_tmp1.append(float("inf"))
	list_tmp2.append(float("inf"))
	while index1 != len(list_tmp1) - 1 or index2 != len(list_tmp2) - 1:
		if list_tmp1[index1] <= list_tmp2[index2]:
			merged_list.append(list_tmp1[index1])
			index1 += 1
		else:
			merged_list.append(list_tmp2[index2])
			index2 += 1
	return merged_list

def merge_sort(list1):
	"""
	merge_sort should return a new sorted list that 
	contains all of the elements in list1 sorted in ascending order.
	"""
	if len(list1) <= 1:
		return list1
	else:
		return merge(merge_sort(list1[0:len(list1)/2]), merge_sort(list1[len(list1)/2:]))

def gen_all_strings(word):
	"""
	return all possible strings that 
	can be constructed from the letters in the input word.
	"""
	if len(word) == 0:
		return [""]
	first = word[0]
	rest = word[1:]
	rest_strings = gen_all_strings(rest)
	new_strings = []
	for rest_string in rest_strings:
		for index in range(len(rest_string) + 1):
			new_string = rest_string[:index] + first + rest_string[index:]
			new_strings.append(new_string)
	new_strings += rest_strings
	return new_strings

