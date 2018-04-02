# -*- coding: utf-8 -*-

######################################################################################
# THIS LIBRARY CONTAINS CLASSES FOR EXTRACTING DATA FROM ESSENTIA'S OUTPUT JSON FILES.
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
######################################################################################

import os
import time
import numpy as np
import ujson as json
from .array_processing import *
from sklearn.decomposition import PCA













'''

- - FUNCTION runEssentiaExtractor() - -

Run a specific Essentia extractor. 


- Attributes:

- - extractor_path:
- - - full path of extractor (relative if in same directory)

- - input_file_path:
- - - full path of input audio file (relative if in same directory)

- - output_file_path:
- - - full path of output file (relative if in same directory)


- Usage:

e_path = "/Users/admin/Documents/essentia-master/build/src/examples/essentia_streaming_extractor_music"
if_path = "/Users/admin/Documents/BackupGoogleDrive/Milano/CreateDataset/SoundFiles/1_1.wav"
of_path = "/Users/admin/Documents/BackupGoogleDrive/Milano/CreateDataset/JSON/1_1.txt"
runEssentiaExtractor(e_path, if_path, of_path)

'''

def runEssentiaExtractor(extractor_path, input_file_path, output_file_path, arguments):
	print(os.popen(extractor_path + " " + input_file_path + " " + output_file_path + " " + arguments).read())
	return 0






		


'''

- - FUNCTION readFeature() - -

Read a specified feature from a json file
and returns it as numpy array. Feature must
be at 0th level of json file!


- Attributes:

- - file_path:
- - - full path of json file (relative if in same directory)

- - feature:
- - - feature to be extracted from the file (string)

- - normalize:
- - - if feature has to be normalized (boolean)


- Usage:

path = "/Users/admin/Documents/BackupGoogleDrive/Milano/CreateDataset/JSON/1_1.txt"
data = readFeature(path, "energy_aw", True)
print(data)

'''
def readFeature(file_path, feature, normalize=False):
	with open(file_path) as data_file:    
		data = json.load(data_file)
	data = np.array(data[feature])
	if normalize == True:
		amax = np.amax(data)
		amin = np.amin(data)
		data = np.subtract(data, amin)
		data = data / (amax - amin)
	return data









'''

- - FUNCTION readFeatures() - -

Read a set of features from a json file
and returns it as numpy nD array. Features
must be at 0th level of json file!


- Attributes:

- - file_path:
- - - full path of json file (relative if in same directory)

- - features:
- - - features to be extracted from the file (array of strings)

- - normalize:
- - - if features have to be normalized (boolean)

- Usage:

path = "/Users/admin/Documents/BackupGoogleDrive/Milano/CreateDataset/JSON/1_1.txt"
data = readFeatures(path, ["energy_aw", "energy_bw", "entropy"], True)
print(data)

'''
def readFeatures(file_path, features, normalize=False, interp=0, power=1):
	with open(file_path) as data:
		data = data.read().replace('nan', '0')
	with open(file_path, 'w') as writefile:
		writefile.write(data)
	with open(file_path) as data_file:    
		data = json.load(data_file)
	result = np.array([data[features[0]]])
	for feature in features[1:]:
		result = np.concatenate((result, [data[feature]]), axis=0)
	if interp > 0:
		for index, feature in enumerate(features):
			result[index] = interpolate(result[index], interp)
	if normalize == True:
		for index, feature in enumerate(features):
			amax = np.amax(result[index])
			amin = np.amin(result[index])
			result[index] = np.subtract(result[index], amin)
			result[index] = result[index] / (amax - amin)
	if power > 1:
		for index, feature in enumerate(features):
			result[index] = np.power(result[index], power)
	return result



def saveFeatureDataAsNPY(file_path_no_extension, features):
	feature_vectors = readFeatures(file_path_no_extension+'.txt', features, True, 0, 1)
	np.save(file_path_no_extension, dict(zip(features, feature_vectors)))
	'''
	with open(file_path_no_extension+".txt") as data_file:    
		data = json.load(data_file)
		for key in data:
			amax = np.amax(data[key])
			amin = np.amin(data[key])
			data[key] = np.subtract(data[key], amin)
			data[key] = data[key] / (amax - amin)
		np.save(file_path_no_extension, data)
	'''



def readFeaturesNPY(file_path, features, normalize=False, interp=0, power=1):
	data = np.load(file_path+'.npy').tolist()
	if normalize == True:
		for index, feature in enumerate(data):
			print(index, feature)
			'''
			amax = np.amax(result[index])
			amin = np.amin(result[index])
			result[index] = np.subtract(result[index], amin)
			result[index] = result[index] / (amax - amin)
			'''
	return np.array([data[feature] for feature in features])












'''

- - FUNCTION computeStartFrames() - -


Create a vector containing the start frame
for each element in feature matrix.



- Attributes:

- - features:
- - - the feature matrix (computed by readFeatures() function)

- - hopSize:
- - - hop size of feature extraction

- Usage:


'''
def computeStartFrames(features, hopSize):
	frames = np.array([])
	for i, x in enumerate(features[0]):
		frames = np.concatenate((frames, [i * int(hopSize)]), axis=0)
	return frames













def autoSelectFeatures(features, feature_data):
	pca = PCA()
	pca.fit(feature_data)
	importance = pca.singular_values_
	print(importance)
	feature_importance = np.array([])
	for i in range(len(features)):
		max_id = list(importance).index(np.amax(importance))
		feature_importance = np.concatenate((feature_importance, [features[max_id]]), axis=0)
		importance[max_id] = 0.0
	print(feature_importance)
