# Implementing iterative mergesort with queue
import queue

def q_mergesort(A):
	"""
	Use a queue to recursively split and sort, then merge, the input list
	"""
	# Define the queue
	Q = queue.Queue()
	# Add each element in the list as a list (for use in merge())
	for a in A:
		Q.put([a])
	# Pop two elements, merge them, and add them to the back of the queue
	while Q.qsize() > 1:
		Q.put(merge(Q.get(), Q.get()))
	# Return the last remaining element- a sorted version of input A
	return Q.get()

def merge(x, y):
	"""
	Merge two input lists recursively, sorting along the way
	"""
	# If one list is empty, then simply return the other
	if len(x) == 0: return y
	if len(y) == 0: return x
	# Sort by the first element, then recursively merge the remaining elements
	if x[0] <= y[0]:
		return([x[0]] + merge(x[1:], y))
	return([y[0]] + merge(x, y[1:]))

print(q_mergesort([1, 5, 4, 6, 2, 5, 1000, 184, 19.2, 48.10]))