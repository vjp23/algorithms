# Implementation of a recursive divide-and-conquer algorithm for finding the median of an array in O(n) time

import math

def select_item(A, k=-1):
	"""
	Returns the kth element of array A in O(n) time. When k = -1,
	which is its default value, the median element is returned,
	where the median is defined as ceiling(|A|/2)th smallest element
	"""
	# Determine whether k is the median item
	if k == -1:
		# Use floor due to 0-indexing
		k = math.floor(len(A) / 2)
	# Begin by breaking A into ceil(|A|/5) groups
	groups = []
	for i in range(0, len(A), 5):
		groups.append([A[i:i + 5]])
	# Next, build a set S of the medians of each group in G.
	# Since each group is just 5 elements, this is done in linear time
	S = [group_median(g) for g in groups]
	# Now, recursively get the medians of subgroups
	p = select_item(S, len(A) / 10)
	# Define three bins for breaking the input list
	A_l, A_p, A_r = [], [], []
	# Break the input into bins
	for a in A:
		if a < p:
			A_l.append(a)
		elif a == p:
			A_p.append(a)
		else:
			A_r.append(a)
	# Now, find the bin containing k and recurse on it
	if k <= len(A_l):
		return(select_item(A_l, k))
	elif k > len(A_l) + len(A_p):
		return(select_item(A_r, k - len(A_l) - len(A_p)))
	else:
		return(p)

def group_median(group):
	"""
	Returns the median of input list group, where |group| <= 5
	"""
	# First, sort the list
	group.sort()
	# Now determine whether the group has 5 elements or some even or odd smaller integer
	if len(group) % 2 != 0:
		# Odd length groups (most of them)
		return group[math.floor(len(group) / 2)]
	# Deal with even-length groups
	return group[len(group) / 2 - 1]

print(select_item([1, 2, 3]))