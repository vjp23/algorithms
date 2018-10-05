import math

def missing_num(A, st=0, ed=-1):
	"""
	Find the smallest missing number in A
	"""
	if ed == -1:
		ed = len(A) - 1
	if st == ed:
		if A[st] == st + 1:
			return st + 2
		return st + 1
	mid = math.floor((ed + st) / 2)
	if A[mid] == mid + 1:
		return missing_num(A, mid + 1, ed)
	if A[mid] > mid + 1:
		return missing_num(A, st, mid)