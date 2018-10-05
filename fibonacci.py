import time

def fib_rec(n):
	# Recursive Fibonacci sequence - exponential time!
	if n == 0:
		return 0
	if n == 1:
		return 1
	return fib_rec(n - 1) + fib_rec(n - 2)


def fib_array(n):
	# Array-based Fibonacci sequence - polynomial time
	if n == 0:
		return 0
	if n == 1:
		return 1
	a = list(range(n + 1))
	for i in range(2, n + 1):
		a[i] = a[i - 1] + a[i - 2]
	return a[-1]


def fib_direct(n):
	# Directly compute the nth Fibonacci number
	rt_five = 5 ** (0.5)
	left = (1 / rt_five) * ((1 + rt_five) / 2) ** n
	right = (1 / rt_five) * ((1 - rt_five) / 2) ** n
	return left - right


rec_start = time.time()
fib_rec(30)
rec_time = time.time() - rec_start

print('Calculating the 30th Fibonacci number took {0:.1f}ms with the recursive method.'.format(1000 * rec_time))

arr_start = time.time()
fib_array(30000)
arr_time = time.time() - arr_start

print('Calculating the 30,000th Fibonacci number took {0:.1f}ms with the array method.'.format(1000 * arr_time))

dir_start = time.time()
fib_direct(300)
dir_time = time.time() - dir_start

print('Calculating the 30,000th Fibonacci number took {0:.5f}ms with the direct method.'.format(1000 * dir_time))

if fib_rec(10) == fib_array(10) and fib_array(10) == fib_direct(10):
	print('All methods produced the same output.')