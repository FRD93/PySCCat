# -*- coding: utf-8 -*-

#################################################################################
# THIS LIBRARY CONTAINS CLASSES FOR ARRAY PROCESSING.
# 
# Copyright (C) 2017  Francesco Roberto Dani
# Mail of the author: f.r.d@hotmail.it
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#################################################################################

import math
import numpy as np
import sklearn.utils
from scipy import spatial
from scipy import signal










'''
- - FUNCTION normalize() - -

A function to normalize a numpy array.

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(normalize([0.1, 0.5, 0.9, 0.3]))

'''
def normalize(array):
	amax = np.amax(array)
	amin = np.amin(array)
	array = np.subtract(array, amin)
	if (amax - amin) != 0:
		return array / (amax - amin)
	else:
		return array











'''
- - FUNCTION interpolate() - -

A function to calculate the covariance
of 2 numpy arrays.
https://it.wikipedia.org/wiki/Covarianza_(probabilità)
http://ncalculators.com/statistics/covariance-calculator.htm

- Attributes:

- - array:
- - - a 1-dimensional numpy array

- - factor:
- - - integer, defining interpolation factor


- Usage:

print(interpolate(np.array([1, 2, 3, 4, 5,4 ,3, 2, 1]), 1))

'''
def interpolate(array, factor=1):
	indexes = np.array([0])
	interp_array = np.array([])
	for index in range(factor):
		indexes = np.concatenate((indexes, [index+1]), axis=0)
		indexes = np.concatenate((indexes, [-(index+1)]), axis=0)
	len_indexes = len(indexes)
	for index, number in enumerate(array):
		interp_array = np.concatenate((interp_array, [np.sum(array[np.clip(np.add(indexes, index), 0, len(array)-1)]) / len_indexes]), axis=0)
	return interp_array
















'''
- - FUNCTION mmap() - -

Map a number from a range
to another.

- Attributes:

- - number:
- - - a 1-dimensional numpy array

- - range1:
- - - tuple, (min, max)

- - range2:
- - - tuple, (min, max)

- - reverse:
- - - boolean, if True reverse mapping

- Usage:

print(mmap(0.56, (0, 1), (0.2, 0.3)))

'''
def mmap(number, range1, range2, reverse=False):
	return (((number - range1[0]) / (range1[1] - range1[0])) * (range2[1] - range2[0])) + range2[0]















'''
- - FUNCTION expand() - -

Expand array length.

- Attributes:

- - array:
- - - a 1-dimensional numpy array

- - length:
- - - integer, final array length

- Usage:

print(expand([0, 2, 45, 29], 20))

'''
def expand(array, length):
	maxDim = 0
	for i in range(len(array)):
		if isinstance(array[i], list) or isinstance(array[i], np.ndarray):
			maxDim = len(array[i])
	if maxDim == 0:
		result = np.array([])
		step = math.ceil(length / float(len(array[:-1])))
		for index, item in enumerate(array[:-1]):
			index1 = np.clip(index+1, 0, len(array)-1)
			item1 = array[index1]
			for i2 in range(step):
				result = np.concatenate((result, [item + ((item1 - item) * i2 / step)]), axis=0)
		if(len(result) < length):
			result = np.concatenate((result, np.zeros(length-len(result))), axis=0)
		if(len(result) > length):
			result = result[:length]
			result[-1] = array[-1]
	else:
		len_ = len(array)
		diff = length - len_
		step = int(len_ / diff)
		if step == 0:
			print("Too large to expand... breaking")
			return [0]
		first = np.zeros(len(array[0]))
		result = np.array([first])
		add_counter = 0
		for i in range(len_):
			result = np.concatenate((result, [array[i]]), axis=0)
			if ((i) % step == 0) and (add_counter < diff):
				result = np.concatenate((result, [np.add(array[i], array[np.clip(i+1, 0, len(array)-1)]) / 2]), axis=0)
				add_counter = add_counter + 1
		result = result[1:]
	return result


















'''
- - FUNCTION reduce() - -

Reduce array length.

- Attributes:

- - array:
- - - a 1-dimensional numpy array

- - length:
- - - integer, final array length

- Usage:

print(reduce([0, 2, 45, 29], 20))

'''
def reduce_(array, length):
	maxDim = 0
	for i in range(len(array)):
		if isinstance(array[i], list) or isinstance(array[i], np.ndarray):
			maxDim = len(array[i])
	if maxDim == 0:
		len_ = len(array)
		diff = len_ - length
		print(diff)
		step = int(len_ / length)
	else:
		len_ = len(array)
		diff = len_ - length
		step = int(len_ / diff)
		first = np.zeros(len(array[0]))
		result = np.array([first])
		add_counter = 0
		for i in range(len_):
			if ((i) % step == 0):
				result = np.concatenate((result, [array[i]]), axis=0)
		result = result[1:]
	return array[::step]
















'''
- - FUNCTION resample() - -

Resample array.

- Attributes:

- - array:
- - - a 1-dimensional numpy array

- - length:
- - - integer, final array length

- Usage:

print(resample([0, 2, 45, 29], 20))


'''
def resample(array, length):
	len_ = len(array)
	if len_ > length:
		result = reduce_(array, length)
	elif len_ < length:
		result = expand(array, length)
	else:
		result = array
	return result
















'''
- - FUNCTION stddev() - -

A function to calculate the standard
deviation of a numpy array.

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(stddev([1, 1, 1, 1000]))

'''
def stddev(array):
	mean = np.sum(array) / len(array)
	std = 0
	for j in range(len(array)):
		std = std + np.power((array[j] - mean), 2)
	std = np.sqrt((std / len(array)))
	return std













'''
- - FUNCTION variance() - -

A function to calculate the variance
of a numpy array.
https://it.wikipedia.org/wiki/Covarianza_(probabilità)

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(variance([1, 1, 20, 1, 1, 1, 1, 1]))

'''
def variance(array):
	mean = np.mean(array)
	var_ = 0
	for i, x in enumerate(array):
		var_ = var_ + np.power(x - mean, 2)
	return var_















'''
- - FUNCTION covariance() - -

A function to calculate the covariance
of 2 numpy arrays.
https://it.wikipedia.org/wiki/Covarianza_(probabilità)
http://ncalculators.com/statistics/covariance-calculator.htm

- Attributes:

- - array1:
- - - a 1-dimensional numpy array

- - array2:
- - - a 1-dimensional numpy array


- Usage:

print(covariance([65.21, 64.75, 65.26, 65.76, 65.96], [67.25, 66.39, 66.12, 65.70, 66.64]))

'''
def covariance(array1, array2):
	if len(array1) != len(array2):
		print("Size of the two arrays differ! Breaking...")
		pass
	size = len(array1) - 1
	mean1 = np.mean(array1)
	mean2 = np.mean(array2)
	covar = 0
	for i, x in enumerate(array1):
		covar = covar + ( (x - mean1) * (array2[i] - mean2) )
	return covar / size

















'''
- - FUNCTION correlation() - -

A function to calculate the correlation
of 2 numpy arrays.
http://www.math.uah.edu/stat/expect/Covariance.html

- Attributes:

- - array1:
- - - a 1-dimensional numpy array

- - array2:
- - - a 1-dimensional numpy array


- Usage:

print(correlation([65.21, 64.75, 65.26, 65.76, 65.96], [67.25, 66.39, 66.12, 65.70, 66.64])) # returns 0.058
print(correlation(np.random.random(100000) * 100, np.random.random(100000) * 100)) # returns -0.00185575395109

'''
def correlation(array1, array2):
	#return covariance(array1, array2) / ( stddev(array1) * stddev(array2) )
	return covariance(array1, array2) / np.sqrt( variance(array1) * variance(array2) )















'''
- - FUNCTION flatness() - -

A function to calculate the flatness
of a numpy array.
https://en.wikipedia.org/wiki/Spectral_flatness

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(flatness([1, 1, 1, 10, 10, 10, 500, 1]))

'''
def flatness(array):
	sum_ = np.sum(array)
	ln_sum = 0
	for i, num in enumerate(array):
		ln_sum = ln_sum + math.log(array[i])
	ln_sum = ln_sum / len(array)
	return math.exp(ln_sum) / (sum_ / len(array))














'''
- - FUNCTION rms() - -

A function to calculate rms value
of a numpy array.
https://it.wikipedia.org/wiki/Valore_efficace

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(rms([1, 1, 5, 0, 0, 0]))

'''
def rms(array):
	return np.sqrt(np.sum(np.power(array, 2)) / np.sum(array))












'''
- - FUNCTION crest() - -

A function to calculate the crest value
of a numpy array.
https://en.wikipedia.org/wiki/Crest_factor

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(crest([10000, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

'''
def crest(array):
	return np.amax(np.abs(array)) / rms(array)















'''
- - FUNCTION hfc() - -

A function to calculate the high 
frequency content of a numpy array.
https://en.wikipedia.org/wiki/High_frequency_content_measure

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(hfc([0, 0, 0, 1, 1, 1, 1, 1, 1, 100]))

'''
def hfc(array):
	hfc_ = 0
	for i, x in enumerate(array):
		hfc_ = hfc_ + (i * abs(x))
	return hfc_












'''
- - FUNCTION centroid() - -

A function to calculate the centroid
of a numpy array.

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(centroid([1, 1, 1, 10, 10, 10, 500, 1]))

'''
def centroid(array):
	sum_ = np.sum(array)
	weighted_sum = 0
	for i, x in enumerate(array):
		weighted_sum = weighted_sum + ( (i / len(array)) * x )
	return weighted_sum / sum_
















'''
- - FUNCTION spread() - -

A function to calculate the spread
of a numpy array.

- Attributes:

- - array:
- - - a 1-dimensional numpy array


- Usage:

print(spread([1, 1, 1, 10, 10, 10, 500, 1]))

'''
def spread(array):
	mu = np.mean(array)
	rho = array / np.sum(array)
	print(rho)
	spread = 0
	for i, x in enumerate(array):
		spread = spread + ( np.power(( x - mu ), 2) * rho[i] )
	return spread
















'''
- - FUNCTION buildKDTree() - -

A function to build a k-nearest neighbour tree
from given features data.


- Attributes:

- - features:
- - - an n-dimensional vector in which is stored feature data


- Usage:

features = np.array([[1, 2, 3], [2, 2, 9], [5, 2, 1], [4, 2, 0], [9, 8, 1]])
tree = buildKDTree(features)
print(tree)

'''
def buildKDTree(features):
	return spatial.KDTree(features.T)












'''
- - FUNCTION queryKDTree() - -

A function to query from a k-nearest neighbour tree
a definite number of neighbours by a given point in the space.


- Attributes:

- - kdtree:
- - - a k-nearest neighbour tree

- - point:
- - - a list of the same size as the kdtree's dimensions defining a point in that space

- - neighbours:
- - - an integer defining how many neighbours to return


- Usage:

features = np.array([[1, 2, 3], [2, 2, 9], [5, 2, 1], [4, 2, 0], [9, 8, 1]])
tree = buildKDTree(features)
indexes = queryKDTree(tree, (1, 3, 2, 4, 0), 3)
print(indexes)

'''
def queryKDTree(kdtree, point, neighbours):
	return kdtree.query(point, neighbours)[1]

