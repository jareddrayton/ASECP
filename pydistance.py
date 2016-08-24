""" This module is an implementation of distance measures after those contained
in the math.NET project http://numerics.mathdotnet.com/Distance.html """

import math

def SAD(x, y):
	""" Sum of the Absolute Difference
	:input x: a one dimensional list containing integers or floats.
	:input y: a one dimensional list containing integers or floats. 

	:returns: the sum of the absolute differences of each element
	"""

	total = []

	for i in range(len(x)):
		total.append(x[i] - y[i])

	total = map(abs, total)

	return sum(total)


def SSD(x,y):
	""" Sum of the Squared Difference
	:input x: a one dimensional list.
	:input y: a one dimensional list. 

	:returns: the sum of the absolute differences of each element
	"""

	total = []

	for i in range(len(x)):
		total.append((x[i] - y[i]) ** 2)

	return sum(total)


def MAE(x,y):
	""" Mean-Absolute Error
	:input x: a one dimensional list containing integers or floats.
	:input y: a one dimensional list containing integers or floats. 

	:returns: the sum of the absolute differences of each element
	"""

	total = []

	for i in range(len(x)):
		total.append(x[i] - y[i])

	total = map(abs, total)

	return sum(total) // len(x)


def MSE(x,y):
	""" Mean-Squared Error Distance
	:input x: a one dimensional list.
	:input y: a one dimensional list. 

	:returns: the sum of the absolute differences of each element
	"""

	total = []

	for i in range(len(x)):
		total.append((x[i] - y[i]) ** 2)

	return sum(total) // len(x)


def EUC(x,y):
	""" Euclidean distance

	:returns: the sum of the absolute differences of each element
	"""

	total = []

	for i in range(len(x)):
		total.append((x[i] - y[i]) ** 2)

	return math.sqrt(sum(total))

def CAN(x,y):
	""" Canberra Distance

	:
	"""

	total = []

	for i in range(len(x)):
		total.append(abs(x[i]-y[i]) / (abs(x[i]) + abs(y[i])))

	return sum(total)

# y = [495.0, 1627.0, 2267.0]
# x = [319.0, 1944.0, 2700.0]
# y = [10000, 10000, 10000]

# print CAN(x,y)
# print SSD(x,y)

