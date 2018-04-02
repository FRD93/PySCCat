# -*- coding: utf-8 -*-

######################################################################################
# THIS LIBRARY CONTAINS QT GRAPHIC CLASSES TO HANDLE USER INTERFACE.
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

import sys
import ast
import json
import time
import math
import pickle
import threading
import collections
import numpy as np
from .arduino import *
from .essentia import *
import pyqtgraph as pg
import configparser as cp
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .supercollider import *
from threading import Thread
from PyQt5.QtWidgets import *
import pyqtgraph.opengl as gl
from .array_processing import *
from pyqtgraph.dockarea import *
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from pyqtgraph.Qt import QtCore, QtGui
from pythonosc import osc_message_builder
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
























sndfile = "dataset"
bufnum = 6

parser = cp.ConfigParser()
parser.read("./conf/config.ini")
def ConfigSectionMap(section):
	dict1 = {}
	options = parser.options(section)
	for option in options:
		try:
			dict1[option] = parser.get(section, option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1

feature_extractor_path = ConfigSectionMap("DIRECTORIES")['feature_extractor_path']
sound_file_path        = ConfigSectionMap("DIRECTORIES")['sound_file_path']
feature_file_path      = ConfigSectionMap("DIRECTORIES")['feature_file_path']
preset_path            = ConfigSectionMap("DIRECTORIES")['preset_path']
sample_rate            = ConfigSectionMap("FEATURE_EXTRACTION")['sample_rate']
fft_frame_size         = ConfigSectionMap("FEATURE_EXTRACTION")['fft_frame_size']
fft_hop_size           = ConfigSectionMap("FEATURE_EXTRACTION")['fft_hop_size']
all_features           = np.array(ast.literal_eval(ConfigSectionMap("FEATURE_EXTRACTION")['all_features']))
features               = np.array(ast.literal_eval(ConfigSectionMap("FEATURE_SPACE")['features']))
grain_dur              = np.array(ast.literal_eval(ConfigSectionMap("SYNTHESIS_PARAMETERS")['grain_dur']))
grain_freq             = np.array(ast.literal_eval(ConfigSectionMap("SYNTHESIS_PARAMETERS")['grain_freq']))
updates_per_second     = np.array(ast.literal_eval(ConfigSectionMap("SYNTHESIS_PARAMETERS")['updates_per_second']))























'''

- - Class Image - -

A class to display an image


- Attributes:

- - image: 
- - - path to the image file

- - parent: 
- - - parent view


- Usage:

image = Image(image='/img/feature_dot_red.png', parent=None)

'''
class Image(QLabel):
	
	def __init__(self, image, parent=None):
		super().__init__(parent)
		pix = QPixmap(image)
		self.h = pix.height()
		self.w = pix.width()
		self.setPixmap(pix)

	def _set_pos(self, pos):
		self.move(pos.x() - self.w/2, pos.y() - self.h/2)
		self.x = pos.x()
		self.y = pos.y()

	def get_pos(self):
		return QPointF(self.x, self.y)

	pos = pyqtProperty(QPointF, fset=_set_pos)   














'''

- - Class AnimatedImage - -

A class to display an image and animate it's position


- Attributes:

- - parent: 
- - - parent view

- - image: 
- - - path to the image file

- - anim_time: 
- - - time to perform the animation


- Usage:


'''
class AnimatedImage(QWidget):
	
	def __init__(self, parent=None, image='', anim_time=100):

		super().__init__(parent)
		self.anim_time = anim_time
		self.parent = parent
		self.endValue = QPointF(self.parent.width() / 2, self.parent.height() / 2)
		self.initView(image)
		
		
	def initView(self, image):    
		self.image = Image(image, self)
		if self.parent is not None:
			self.image.pos = QPointF(self.parent.width() / 2, self.parent.height() / 2)
		
		self.animation_timer = QTimer(self)
		self.animation_timer.setSingleShot(False)
		self.animation_timer.timeout.connect(self.doAnim)
		self.animation_timer.start(self.anim_time)
		
		if self.parent is not None:
			self.setGeometry(0, 0, self.parent.width(), self.parent.height())
		else:
			self.setGeometry(0, 0, 300, 300)
			self.maxRand = 300
		self.show()
		
	
	def doAnim(self):
		self.anim = QPropertyAnimation(self.image, b'pos')
		self.anim.setDuration(self.anim_time)
		self.anim.setStartValue(self.image.get_pos())
		self.anim.setEndValue(self.endValue)
		self.anim.start()
		
	def setReachPoint(self, x, y):
		self.endValue = QPointF(x, y)




























'''

- - Class Label - -

A class to display some text


- Attributes:

- - text: 
- - - text to be displayed

- - parent: 
- - - parent view


- Usage:

label = Label(text='Hello World!', parent=None)

'''
class Label(QLabel):
	
	def __init__(self, text="ciao", parent=None):
		super().__init__(parent)	
		self.text = text
		self.label = QLabel(text, parent)
		self.label.setText(self.text)
		self.h = self.label.height()
		self.w = self.label.width()

	def _set_pos(self, pos):
		self.move(pos.x() - self.w/2, pos.y() - self.h/2)
		self.x = pos.x()
		self.y = pos.y()

	def set_pos(self, pos):
		self.x = pos.x()
		self.y = pos.y()
		

	def get_pos(self):
		return QPointF(self.x, self.y)

	def updateText(self, text):
		self.label.setText(text)

	pos = pyqtProperty(QPointF, fset=_set_pos)   















'''

- - Class AnimatedLabel - -

A class to display some text and animate it's position


- Attributes:

- - parent: 
- - - parent view

- - label: 
- - - text to be displayed

- - offet: 
- - - offset in pixels to center the label with it's position

- - anim_time: 
- - - time to perform the animation


- Usage:


'''
class AnimatedLabel(QWidget):
	
	def __init__(self, parent=None, label='', offset=QPointF(15, 30), anim_time=100):
		super().__init__(parent)
		self.offset = offset
		self.anim_time = anim_time
		self.parent = parent
		self.label = label
		self.endValue = QPointF(self.parent.width() / 2, self.parent.height() / 2)
		self.initView()
		
	def initView(self):    
		self.label = Label(self.label, self)
		self.label.setAlignment(Qt.AlignCenter)
		if self.parent is not None:
			self.label.pos = QPointF(self.parent.width() / 2, self.parent.height() / 2)
		self.animation_timer = QTimer(self)
		self.animation_timer.setSingleShot(False)
		self.animation_timer.timeout.connect(self.doAnim)
		self.animation_timer.start(self.anim_time)
		if self.parent is not None:
			self.setGeometry(0, 0, 300, 300)
		else:
			self.setGeometry(0, 0, 30, 30)
		self.show()
		
	def doAnim(self):
		self.anim = QPropertyAnimation(self, b'pos')
		self.anim.setDuration(self.anim_time)
		self.anim.setStartValue(self.label.get_pos())
		self.anim.setEndValue(self.endValue)
		self.anim.start()
		self.label.set_pos(self.endValue)
		
	def setReachPoint(self, x, y):
		self.endValue = QPointF(x-self.offset.x(), y-self.offset.y())

	def updateText(self, text):
		self.label.updateText(text)







































'''

- - Class RadarChart - -

Displays data as radar chart in a window.


- Attributes:

- - n_features: 
- - - number of vectors to display

- - features: 
- - - name of the vectors


- Usage:


'''
class RadarChart(QWidget):

	def __init__(self, n_features, features):
		super().__init__()
		self.n_features = n_features
		self.features = features
		self.colors = ["red", "orange", "yellow", "green", "blue"]
		''' Set window bounds '''
		self.setGeometry(0, 0, 200, 200)
		''' Calculate (x, y) pixel coordinates for every feature '''
		self.temp_angle = ( math.pi / 2 )
		self.temp_x = (math.cos(self.temp_angle) * ((self.width() / 2) - 20)) + (self.width() / 2)
		self.temp_y = -(math.sin(self.temp_angle) * ((self.height() / 2) - 20)) + (self.height() / 2)
		self.features_pos = np.array([[self.temp_x, self.temp_y]])
		for index in range(self.n_features)[1:]:
			self.temp_angle = ( 2 * math.pi * index / n_features ) + ( math.pi / 2 )
			self.temp_x = (math.cos(self.temp_angle) * ((self.width() / 2) - 20)) + (self.width() / 2)
			self.temp_y = -(math.sin(self.temp_angle) * ((self.height() / 2) - 20)) + (self.height() / 2)
			self.features_pos = np.concatenate((self.features_pos, [[self.temp_x, self.temp_y]]), axis=0)
		self.absolute_feature_pos = self.features_pos
		''' Draw an AnimatedImage and a Label for every feature '''
		self.images = np.array([])
		self.feature_values = np.array([])
		self.feature_names = np.array([])
		for index in range(self.n_features):
			self.images = np.concatenate((self.images, [AnimatedImage(self, "./img/feature_dot_"+self.colors[index % len(self.colors)]+".png")]), axis=0)
			self.feature_values = np.concatenate((self.feature_values, [AnimatedLabel(self)]), axis=0)
			self.feature_names = np.concatenate((self.feature_names, [AnimatedLabel(self, self.features[index], QPointF(7,7))]), axis=0)
			self.images[index].setReachPoint(self.features_pos[index][0], self.features_pos[index][1])
			self.feature_values[index].setReachPoint(self.features_pos[index][0], self.features_pos[index][1])
			self.feature_names[index].setReachPoint(self.features_pos[index][0], self.features_pos[index][1])	
		self.show()

	''' Recalc radius positions from feature amplitudes '''
	def calcRadius(self, amplitudes):
		self.temp_angle = ( math.pi / 2 )
		self.temp_x = (amplitudes[0] * math.cos(self.temp_angle) * ((self.width() / 2) - 20)) + (self.width() / 2)
		self.temp_y = -(amplitudes[0] * math.sin(self.temp_angle) * ((self.height() / 2) - 20)) + (self.height() / 2)
		self.features_pos = np.array([[self.temp_x, self.temp_y]])
		for index in range(self.n_features)[1:]:
			self.temp_angle = ( 2 * math.pi * index / self.n_features ) + ( math.pi / 2 )
			self.temp_x = (amplitudes[index] * math.cos(self.temp_angle) * ((self.width() / 2) - 20)) + (self.width() / 2)
			self.temp_y = -(amplitudes[index] * math.sin(self.temp_angle) * ((self.height() / 2) - 20)) + (self.height() / 2)
			self.features_pos = np.concatenate((self.features_pos, [[self.temp_x, self.temp_y]]), axis=0)
		for index in range(self.n_features):
			self.images[index].setReachPoint(self.features_pos[index][0], self.features_pos[index][1])
			self.feature_values[index].setReachPoint(self.features_pos[index][0], self.features_pos[index][1])
			self.feature_values[index].updateText(str(amplitudes[index]))   

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()

	def drawLines(self, qp):
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		for index, axes in enumerate(self.absolute_feature_pos):
			qp.drawLine(self.width() / 2, self.height() / 2, axes[0], axes[1])
			















'''

- - Class GestureSpace - -

Displays sensors data as radar chart in a window.


- Attributes:

- - arduino: 
- - - ArduinoRead instance


- Usage:

arduino = ArduinoRead(port=None)
gestureSpace = GestureSpace(arduino=arduino)

'''
class GestureSpace(QWidget):
	def __init__(self, arduino):
		super().__init__()
		self.arduino = arduino
		self.chart = RadarChart(5, ["1", "2", "3", "4", "5"])
		self.animation_timer = QTimer(self)
		self.animation_timer.setSingleShot(False)
		self.animation_timer.timeout.connect(self.doAnim)
		self.animation_timer.start(50)
		
	def doAnim(self):
		self.chart.calcRadius(self.arduino.pots)
		
















'''

- - Class GestureSpace - -

Displays multidimensional data in a 3D space in a window.


- Attributes:

- - data: 
- - - data to be displayed


- Usage:


'''
class FeatureSpace(Thread):
	def __init__(self, data=None):
		super().__init__()
		self.data = data
		self.points = np.array([])
		self.w = gl.GLViewWidget()
		self.w.resize(400, 400)
		self.w.setCameraPosition(distance=40)
		self.x = gl.GLGridItem()
		self.x.rotate(90, 0, 1, 0)
		self.x.translate(-10, 0, 0)
		self.w.addItem(self.x)
		self.y = gl.GLGridItem()
		self.y.rotate(90, 1, 0, 0)
		self.y.translate(0, -10, 0)
		self.w.addItem(self.y)
		self.z = gl.GLGridItem()
		self.z.translate(0, 0, -10)
		self.w.addItem(self.z)
		self.nd = 3
		self.mesh = gl.MeshData.sphere(rows=4, cols=8)
		self.pointerPosition = [0, 0, 0]
		self.pointer = gl.GLMeshItem(meshdata=self.mesh, smooth=False, drawFaces=False, drawEdges=True, computeNormals=False)#, edgeColor=(1,1,1,1)
		self.pointer.translate(self.pointerPosition[0], self.pointerPosition[1], self.pointerPosition[2])
		self.w.addItem(self.pointer)

	def setPointerPosition(self, position):
		try:
			if len(self.data) == 1:
				self.pointer.translate(0, -self.pointerPosition[0], -self.pointerPosition[0])
				self.pointerPosition = position
				self.pointer.translate(0, self.pointerPosition[0], self.pointerPosition[0])
			if len(self.data) == 2:
				self.pointer.translate(0, -self.pointerPosition[0], -self.pointerPosition[1])
				self.pointerPosition = position
				self.pointer.translate(0, self.pointerPosition[0], self.pointerPosition[1])
			if len(self.data) > 2:
				self.pointer.translate(-self.pointerPosition[0], -self.pointerPosition[1], -self.pointerPosition[2])
				self.pointerPosition = position
				self.pointer.translate(self.pointerPosition[0], self.pointerPosition[1], self.pointerPosition[2])
		except:
			pass
	def reloadData(self, data):
		try:
			self.w.removeItem(self.points);
		except:
			None
		self.data = data
		# Handle 1-dimensional data
		if len(data) == 1:
			self.vertexes = np.array([[[0,0,0], [0,0,0], [0,0,0]]])
			for index in range(len(self.data[0])):
				v1 = np.add(np.array([0, (self.data[0][index]*20)-10, (self.data[0][index]*20)-10]), [1,0,-1])
				v2 = np.add(np.array([0, (self.data[0][index]*20)-10, (self.data[0][index]*20)-10]), [0,1,-1])
				v3 = np.add(np.array([0, (self.data[0][index]*20)-10, (self.data[0][index]*20)-10]), [-1,0,1])
				tri = np.array([[v1, v2, v3]])
				self.vertexes = np.concatenate((self.vertexes, tri), axis=0)
			self.vertexes = self.vertexes[1:]
			self.colorData = np.array([np.full(len(self.data[0]), 0.3), self.data[0], np.full(len(self.data[0]), 0.3)]).T
			self.colors = np.array([[[0,0,0,0], [0,0,0,0], [0,0,0,0]]])
			for index in range(len(self.colorData)):
				self.colors = np.concatenate((self.colors, np.array([[np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0)]])), axis=0)
			self.colors = self.colors[1:]
			self.points = gl.GLMeshItem(vertexes=self.vertexes, vertexColors=self.colors, mooth=True, drawEdges=False)
			self.points.setGLOptions("translucent")
			self.w.addItem(self.points)
		# Handle 2-dimensional data
		if len(data) == 2:
			self.vertexes = np.array([[[0,0,0], [0,0,0], [0,0,0]]])
			for index in range(len(self.data[0])):
				v1 = np.add(np.array([0, (self.data[0][index]*20)-10, (self.data[1][index]*20)-10]), [1,0,-1])
				v2 = np.add(np.array([0, (self.data[0][index]*20)-10, (self.data[1][index]*20)-10]), [0,1,-1])
				v3 = np.add(np.array([0, (self.data[0][index]*20)-10, (self.data[1][index]*20)-10]), [-1,0,1])
				tri = np.array([[v1, v2, v3]])
				self.vertexes = np.concatenate((self.vertexes, tri), axis=0)
			self.vertexes = self.vertexes[1:]
			self.colorData = np.array([np.full(len(self.data[0]), 0.3), self.data[0], self.data[1]]).T
			self.colors = np.array([[[0,0,0,0], [0,0,0,0], [0,0,0,0]]])
			for index in range(len(self.colorData)):
				self.colors = np.concatenate((self.colors, np.array([[np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0)]])), axis=0)
			self.colors = self.colors[1:]
			self.points = gl.GLMeshItem(vertexes=self.vertexes, vertexColors=self.colors, mooth=True, drawEdges=False)
			self.points.setGLOptions("translucent")
			self.w.addItem(self.points)
		# Handle 3-dimensional data
		if len(data) == 3:
			self.vertexes = np.array([[[0,0,0], [0,0,0], [0,0,0]]])
			for index in range(len(self.data[0])):
				v1 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [1,0,-1])
				v2 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [0,1,-1])
				v3 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [-1,0,1])
				tri = np.array([[v1, v2, v3]])
				self.vertexes = np.concatenate((self.vertexes, tri), axis=0)
			self.vertexes = self.vertexes[1:]
			self.colorData = self.data.T
			self.colors = np.array([[[0,0,0,0], [0,0,0,0], [0,0,0,0]]])
			for index in range(len(self.colorData)):
				self.colors = np.concatenate((self.colors, np.array([[np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0)]])), axis=0)
			self.colors = self.colors[1:]
			self.points = gl.GLMeshItem(vertexes=self.vertexes, vertexColors=self.colors, mooth=True, drawEdges=False)
			self.points.setGLOptions("translucent")
			self.w.addItem(self.points)
		# Handle 4-dimensional data
		if len(data) == 4:
			self.vertexes = np.array([[[0,0,0], [0,0,0], [0,0,0]]])
			for index in range(len(self.data[0])):
				v1 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [1,0,-1])
				v2 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [0,1,-1])
				v3 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [-1,0,1])
				tri = np.array([[v1, v2, v3]])
				self.vertexes = np.concatenate((self.vertexes, tri), axis=0)
			self.vertexes = self.vertexes[1:]
			self.colorData = np.array([self.data[3], np.full(len(self.data[3]), 0.2), np.full(len(self.data[3]), 0.8)]).T
			self.colors = np.array([[[0,0,0,0], [0,0,0,0], [0,0,0,0]]])
			for index in range(len(self.colorData)):
				self.colors = np.concatenate((self.colors, np.array([[np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0)]])), axis=0)
			self.colors = self.colors[1:]
			self.points = gl.GLMeshItem(vertexes=self.vertexes, vertexColors=self.colors, mooth=True, drawEdges=False)
			self.points.setGLOptions("translucent")
			self.w.addItem(self.points)
		# Handle 5-dimensional data
		if len(data) == 5:
			self.vertexes = np.array([[[0,0,0], [0,0,0], [0,0,0]]])
			for index in range(len(self.data[0])):
				v1 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [1,0,-1])
				v2 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [0,1,-1])
				v3 = np.add(np.array([(self.data[0][index]*20)-10, (self.data[1][index]*20)-10, (self.data[2][index]*20)-10]), [-1,0,1])
				tri = np.array([[v1, v2, v3]])
				self.vertexes = np.concatenate((self.vertexes, tri), axis=0)
			self.vertexes = self.vertexes[1:]
			self.colorData = np.array([self.data[3], np.full(len(self.data[3]), 0.2), self.data[4]]).T
			self.colors = np.array([[[0,0,0,0], [0,0,0,0], [0,0,0,0]]])
			for index in range(len(self.colorData)):
				self.colors = np.concatenate((self.colors, np.array([[np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0), np.concatenate((self.colorData[index], [0.4]), axis=0)]])), axis=0)
			self.colors = self.colors[1:]
			self.points = gl.GLMeshItem(vertexes=self.vertexes, vertexColors=self.colors, mooth=True, drawEdges=False)
			self.points.setGLOptions("translucent")
			self.w.addItem(self.points)

	def show(self):
		self.w.show()

	def hide(self):
		self.w.hide()








'''

 - - Class RecordedView - -

 Enables to play/stop recorded stream patterns

'''
class RecordedView(QWidget):
	
	def __init__(self):
		super().__init__()
		self.numButtons = 8
		self.buttons = np.array([], dtype=object)

	def initGUI(self):
		for i in range(self.numButtons):
			self.buttons[i] = QtGui.QPushButton('{}'.format(i))
		self.show()









'''

- - Class ConcatStream - -

Handles a concatenative synthesis stream


- Attributes:

- - scsynth: 
- - - SCSYNTH instance

- - arduino: 
- - - ArduinoRead instance

- - preset: 
- - - initial preset


- Usage:


'''
class ConcatStream():
	def __init__(self, scsynth, arduino, preset, outCh=20):
		print(preset)
		# Every how many milliseconds the stream updates it's parameters
		self.updateTime = 10
		# Stream output channel (SC)
		self.outCh = outCh
		# Done loading everything?
		self.doneLoading = False
		# Is playing?
		self.isPlaying = False
		# Is freeze mode just begun?
		self.firstFreezeLoop = False
		# Is freeze mode enabled?
		self.isFreezeEnabled = False
		# Do the stream have to record the update parameters?
		self.hasToRecord = False
		# Is playing in recorded mode?
		self.isPlayingRecorded = False
		# SCSYNTH instance
		self.scsynth = scsynth
		# Arduino instance
		self.arduino = arduino
		# Name of the stream
		self.name = preset
		# Name of the stream's preset
		self.presetName = preset
		# Feature space instance
		self.featureSpace = FeatureSpace(data=None)
		# Sound files list
		self.sndfiles = [f.split('.')[0] for f in os.listdir(sound_file_path) if len(f.split('.')) > 1 and f.split('.')[1] == 'wav']
		# Buffer indexes list
		self.buffers = [i for i in range(len(self.sndfiles))]
		# Preset list
		self.presets = [f.split('.')[0] for f in os.listdir(preset_path) if len(f.split('.')) > 1 and f.split('.')[1] == 'npy']
		# Load first soundfile
		self.sndfile = self.sndfiles[0]
		# Default dimensionality
		self.featureDimension = 3
		# Name of the available features
		self.featureNames = ['centroid', 'skewness', 'hfc', 'crest', 'inharmonicity']		
		# Name of the parameters
		self.paramNames = ('Parameters.Feature1', 'Parameters.Feature2', 'Parameters.Feature3', 'Parameters.Feature4', 'Parameters.Feature5', 'Parameters.Pitch', 'Parameters.GrainDur', 'Parameters.GrainFreq', 'Parameters.Amplitude', 'Parameters.Panning', 'Parameters.GrainAtk', 'Parameters.Neighbors')
		# Name of the arduino controls (plus 'None')
		self.controls = self.arduino.control_names + ['None']
		# ???
		self.reversedControl = dict(zip(self.paramNames, [False for i in range(len(self.paramNames))]))
		# Check if GUI is visible
		self.isGUIshown = False
		# Main window
		self.w = QtGui.QMainWindow()
		# Dock for parameters
		self.area = DockArea()
		self.w.setCentralWidget(self.area)
		self.w.resize(320,700)
		self.w.setWindowTitle('ConcatStream: '+self.presetName)		
		self.paramDock = Dock("Parameters")
		self.area.addDock(self.paramDock, 'top')

		self.parameters = [
			{'name': 'Parameters', 'type': 'group', 'children': [
				{'name': 'Name', 'type': 'str', 'value': self.presetName},
				{'name': 'Soundfile', 'type': 'list', 'values': self.sndfiles, 'value': self.sndfile},
				{'name': 'Preset', 'type': 'list', 'values': self.presets, 'value': self.presetName},
				{'name': 'Dimensionality', 'type': 'list', 'values': [1, 2, 3, 4, 5], 'value': self.featureDimension},
				{'name': 'Feature1', 'type': 'group', 'children': [
					{'name': 'which', 'type': 'list', 'values': ['centroid', 'crest', 'flatness', 'hfc', 'inharmonicity', 'skewness', 'spread', 'kurtosis'], 'value': self.featureNames[0]},
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[0]}
				]},
				{'name': 'Feature2', 'type': 'group', 'children': [
					{'name': 'which', 'type': 'list', 'values': ['centroid', 'crest', 'flatness', 'hfc', 'inharmonicity', 'skewness', 'spread', 'kurtosis'], 'value': self.featureNames[1]},
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[1]}
				]},
				{'name': 'Feature3', 'type': 'group', 'children': [
					{'name': 'which', 'type': 'list', 'values': ['centroid', 'crest', 'flatness', 'hfc', 'inharmonicity', 'skewness', 'spread', 'kurtosis'], 'value': self.featureNames[2]},
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[2]}
				]},
				{'name': 'Feature4', 'type': 'group', 'children': [
					{'name': 'which', 'type': 'list', 'values': ['centroid', 'crest', 'flatness', 'hfc', 'inharmonicity', 'skewness', 'spread', 'kurtosis'], 'value': self.featureNames[3]},
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[3]}
				]},
				{'name': 'Feature5', 'type': 'group', 'children': [
					{'name': 'which', 'type': 'list', 'values': ['centroid', 'crest', 'flatness', 'hfc', 'inharmonicity', 'skewness', 'spread', 'kurtosis'], 'value': self.featureNames[4]},
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[4]}
				]},
				{'name': 'Pitch', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'float', 'value': 0.8},
					{'name': 'max', 'type': 'float', 'value': 4},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					#{'name': 'round', 'type': 'float', 'value': 0.0},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[2]}
				]},
				{'name': 'GrainDur', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'float', 'value': 0.004},
					{'name': 'max', 'type': 'float', 'value': 0.4},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[3]}
				]},
				{'name': 'GrainFreq', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'float', 'value': 50},
					{'name': 'max', 'type': 'float', 'value': 400},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					#{'name': 'round', 'type': 'float', 'value': 0.0},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[4]}
				]},
				{'name': 'Amplitude', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'float', 'value': 0.5},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[2]}
				]},
				{'name': 'Panning', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[0]}
				]},
				{'name': 'GrainAtk', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'float', 'value': 0.0},
					{'name': 'max', 'type': 'float', 'value': 1.0},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[1]}
				]},
				{'name': 'Neighbors', 'type': 'group', 'children': [
					{'name': 'min', 'type': 'int', 'value': 1},
					{'name': 'max', 'type': 'int', 'value': 20},
					{'name': 'reverse', 'type': 'bool', 'value': False},
					{'name': 'hardwareConnection', 'type': 'list', 'values': self.controls, 'value': self.controls[0]}
				]},
			]}
		]
		self.p = Parameter.create(name='params', type='group', children=self.parameters)
		self.t = ParameterTree()
		self.t.setParameters(self.p, showTop=False)
		self.p.sigTreeStateChanged.connect(self.change)
		self.paramDock.addWidget(self.t)
		# save preset to file
		self.saveBtn = QtGui.QPushButton('Save')
		self.paramDock.addWidget(self.saveBtn)
		self.saveBtn.clicked.connect(self.save)
		# recall preset from file
		self.recallBtn = QtGui.QPushButton('Recall')
		self.paramDock.addWidget(self.recallBtn)
		self.recallBtn.clicked.connect(self.recall)
		self.csthread = CSThread(server=self.scsynth, bufnum=0, amp=0, outCh=self.outCh)
		self.recall()
		self.doneLoading = True
		self.initAudioNoReloadCSThread()

	def save(self):
		np.save(preset_path+self.presetName, self.p.saveState())

	def recall(self):
		data = dict(np.load(preset_path+self.presetName+'.npy').tolist())
		data['children']['Parameters']['children']['Preset']['values'] = [f.split('.')[0] for f in os.listdir(preset_path) if len(f.split('.')) > 1 and f.split('.')[1] == 'npy']
		data['children']['Parameters']['children']['Preset']['limits'] = data['children']['Parameters']['children']['Preset']['values']
		data['children']['Parameters']['children']['Preset']['value'] = self.presetName
		data['children']['Parameters']['children']['Preset']['default'] = self.presetName
		data['children']['Parameters']['children']['Name']['value'] = self.presetName
		data['children']['Parameters']['children']['Name']['default'] = self.presetName
		data['children']['Parameters']['children']['Soundfile']['values'] = [f.split('.')[0] for f in os.listdir(sound_file_path) if len(f.split('.')) > 1 and f.split('.')[1] == 'wav']
		data['children']['Parameters']['children']['Soundfile']['limits'] = data['children']['Parameters']['children']['Soundfile']['values']
		data['children']['Parameters']['children']['Soundfile']['default'] = data['children']['Parameters']['children']['Soundfile']['value']
		self.p.restoreState(data)
		np.save(preset_path+self.presetName, self.p.saveState())

	def change(self, param, changes):
		for param, change, data in changes:
			path = self.p.childPath(param)
			if path is not None:
				childName = '.'.join(path)
			else:
				childName = param.name()

			if childName == 'Parameters.Soundfile':
				if not isinstance(data, (list, collections.OrderedDict, np.ndarray)):
					self.sndfile = data
					if self.doneLoading:
						self.initAudioNoReloadCSThread()
						self.reloadFeatureSpace()

			if childName == 'Parameters.Preset':
				self.presetName = str(data)
				print("preset name", self.presetName)
				if self.doneLoading:
					self.recall()
					self.initAudioNoReloadCSThread()
					self.reloadFeatureSpace()
				
			if childName == 'Parameters.Dimensionality':
				self.featureDimension = data
				if self.doneLoading:
					self.initAudioNoReloadCSThread()
					self.reloadFeatureSpace()

			if childName == 'Parameters.Name':
				print('name : ', str(data))
				self.name = str(data)
				self.presetName = str(data)
				self.w.setWindowTitle('ConcatStream: '+self.presetName)

			if len(path) > 2 and path[2] == 'hardwareConnection':
				self.checkHardwareConnections()

			if len(path) > 2 and path[2] == 'which':
				self.featureNames[int(path[1][-1])-1] = data
				if self.doneLoading:
					self.initAudioNoReloadCSThread()
					self.reloadFeatureSpace()

			if len(path) > 2 and (path[2] == 'min' or path[2] == 'max'):
				self.calcParameterMinMaxRanges()

			if childName == 'Parameters.GrainFreq.round':
				self.csthread.setRoundGFreq(data)

			if childName == 'Parameters.Pitch.round':
				self.csthread.setRoundPitch(data)

			if path is not None and len(path) > 2:
				if path[2] == 'reverse':
					if self.reversedControl['.'.join(path[0:2])] == False:
						self.reversedControl['.'.join(path[0:2])] = True
					else:
						self.reversedControl['.'.join(path[0:2])] = False

	def playThread(self):
		if not self.isFreezeEnabled:
			if(self.arduino.port != None):
				self.pots = self.arduino.pots
			else:
				self.pots = np.zeros(len(self.arduino.pots))
				for i in range(len(self.arduino.pots)):
					self.pots[i] = self.arduino.lags[i].getValue()
			for index, param in enumerate(self.paramNames):
				if param.split(".")[1][0:7] == "Feature":
					if self.hardwareConnections[param] != (len(self.controls)-1):
						self.kdQuery[index] = ((self.pots[self.hardwareConnections[param]] if not self.reversedControl else 1.0 - self.pots[self.hardwareConnections[param]]) * (self.maxValues[param] - self.minValues[param])) + self.minValues[param]
					else:
						self.kdQuery[index] = self.minValues[param]
				else:
					if self.hardwareConnections[param] != (len(self.controls)-1):
						self.csthread.setParam(param.split(".")[1], ((self.pots[self.hardwareConnections[param]] if not self.reversedControl else 1.0 - self.pots[self.hardwareConnections[param]]) * (self.maxValues[param] - self.minValues[param])) + self.minValues[param])
					else:
						self.csthread.setParam(param.split(".")[1], self.minValues[param])
			if self.hardwareConnections['Parameters.Neighbors'] != (len(self.controls)-1):
				self.neighbours = int((self.pots[self.hardwareConnections['Parameters.Neighbors']] * (self.maxValues['Parameters.Neighbors'] - self.minValues['Parameters.Neighbors'])) + self.minValues['Parameters.Neighbors'])
			else:
				self.neighbours = int(self.minValues['Parameters.Neighbors'])
			self.featureSpace.setPointerPosition([(self.kdQuery[featurecount] * 20) - 10 for featurecount in range(len(self.kdQuery))])
			sample = queryKDTree(self.kdtree, [self.kdQuery[featurecount] for featurecount in range(self.featureDimension)], self.neighbours)
			if isinstance(sample, list):
				self.csthread.setPos(list(np.multiply(sample, int(fft_hop_size))))
			else:
				self.csthread.setPos(sample * int(fft_hop_size))
		else:
			if self.firstFreezeLoop:
				self.firstFreezeLoop = False
				if(self.arduino.port != None):
					self.pots = self.arduino.pots
				else:
					self.pots = np.zeros(len(self.arduino.pots))
					for i in range(len(self.arduino.pots)):
						self.pots[i] = self.arduino.lags[i].getValue()
				for index, param in enumerate(self.paramNames):
					if param.split(".")[1][0:7] == "Feature":
						if self.hardwareConnections[param] != (len(self.controls)-1):
							self.kdQuery[index] = ((self.pots[self.hardwareConnections[param]] if not self.reversedControl else 1.0 - self.pots[self.hardwareConnections[param]]) * (self.maxValues[param] - self.minValues[param])) + self.minValues[param]
						else:
							self.kdQuery[index] = self.minValues[param]
					else:
						if self.hardwareConnections[param] != (len(self.controls)-1):
							self.csthread.setParam(param.split(".")[1], ((self.pots[self.hardwareConnections[param]] if not self.reversedControl else 1.0 - self.pots[self.hardwareConnections[param]]) * (self.maxValues[param] - self.minValues[param])) + self.minValues[param])
						else:
							self.csthread.setParam(param.split(".")[1], self.minValues[param])
				if self.hardwareConnections['Parameters.Neighbors'] != (len(self.controls)-1):
					self.neighbours = int((self.pots[self.hardwareConnections['Parameters.Neighbors']] * (self.maxValues['Parameters.Neighbors'] - self.minValues['Parameters.Neighbors'])) + self.minValues['Parameters.Neighbors'])
				else:
					self.neighbours = int(self.minValues['Parameters.Neighbors'])
				self.featureSpace.setPointerPosition([(self.kdQuery[featurecount] * 20) - 10 for featurecount in range(len(self.kdQuery))])
				sample = queryKDTree(self.kdtree, [self.kdQuery[featurecount] for featurecount in range(self.featureDimension)], self.neighbours)
				if isinstance(sample, list):
					self.csthread.setPos(list(np.multiply(sample, int(fft_hop_size))))
				else:
					self.csthread.setPos(sample * int(fft_hop_size))
		if self.hasToRecord:
			self.recorded = np.concatenate((self.recorded, [self.csthread.getParameters()]), axis=0)
	
	def record(self):
		self.recorded = np.array([], dtype=object)
		self.hasToRecord = True

	def stopRecording(self):
		self.hasToRecord = False


	def playRecordedThread(self):
		try:
			for index, record in enumerate(self.recorded):
				for key in record.keys():
					self.csthread.setParam(key, record[key])
			self.playRecordedCounter = self.playRecordedCounter + 1
			if self.playRecordedCounter >= len(self.recorded):
				self.playRecordedCounter = 0
		except:
			None

	def playRecorded(self):
		self.playRecordedCounter = 0
		self.playRecordedTimer = QTimer()
		self.playRecordedTimer.setSingleShot(False)
		self.playRecordedTimer.timeout.connect(self.playRecordedThread)
		self.playRecordedTimer.start(self.updateTime)
		self.isPlaying = True
		self.isPlayingRecorded = True
		print("Self playRecorded started!")

	def stopRecorded(self):
		self.playRecordedTimer.stop()
		self.csthread.setAmp(0.0)
		self.isPlaying = False
		self.isPlayingRecorded = False

	def play(self):
		self.kdQuery = np.zeros(5)
		self.checkHardwareConnections()
		self.calcParameterMinMaxRanges()
		self.time = time.time()
		self.playTimer = QTimer()
		self.playTimer.setSingleShot(False)
		self.playTimer.timeout.connect(self.playThread)
		self.playTimer.start(self.updateTime)
		self.isPlaying = True

	def stop(self):
		self.playTimer.stop()
		self.csthread.setAmp(0.0)
		self.isPlaying = False
		self.isFreezeEnabled = False
		self.firstFreezeLoop = False

	def checkHardwareConnections(self):
		self.hardwareConnections = np.array([], dtype="int")
		for param in self.paramNames:
			self.hardwareConnections = np.concatenate((self.hardwareConnections, [self.controls.index(dict(dict(dict(self.p.getValues())[param.split(".")[0]][1])[param.split(".")[1]][1])['hardwareConnection'][0])]), axis=0)
		self.hardwareConnections = dict(zip(self.paramNames, self.hardwareConnections))
		
	def calcParameterMinMaxRanges(self):
		self.minValues = np.array([])
		self.maxValues = np.array([])
		for param in self.paramNames:
			self.minValues = np.concatenate((self.minValues, [float(dict(dict(dict(self.p.getValues())[param.split(".")[0]][1])[param.split(".")[1]][1])['min'][0])]), axis=0)
			self.maxValues = np.concatenate((self.maxValues, [float(dict(dict(dict(self.p.getValues())[param.split(".")[0]][1])[param.split(".")[1]][1])['max'][0])]), axis=0)
		self.minValues = dict(zip(self.paramNames, self.minValues))
		self.maxValues = dict(zip(self.paramNames, self.maxValues))
		if self.minValues['Parameters.Neighbors'] <= 0:
			self.minValues['Parameters.Neighbors'] = 1
		if self.maxValues['Parameters.Neighbors'] <= 0:
			self.maxValues['Parameters.Neighbors'] = 1
		
	def initAudio(self):
		self.featureData = readFeaturesNPY(feature_file_path+self.sndfile, self.featureNames[0:self.featureDimension], normalize=True, interp=0, power=1)
		self.kdtree = buildKDTree(features=self.featureData)
		self.csthread = CSThread(server=self.scsynth, bufnum=0, amp=0, outCh=self.outCh)
		self.csthread.setBufnum(self.sndfiles.index(self.sndfile))
		#print("soundfile index", self.sndfiles.index(self.sndfile))
		self.calcParameterMinMaxRanges()
		self.checkHardwareConnections()
		
	def initAudioNoReloadCSThread(self):
		self.featureData = readFeaturesNPY(feature_file_path+self.sndfile, self.featureNames[0:self.featureDimension], normalize=True, interp=0, power=1)
		self.csthread.setBufnum(self.sndfiles.index(self.sndfile))
		self.kdtree = buildKDTree(features=self.featureData)
		self.start_frames = computeStartFrames(features=self.featureData, hopSize=fft_hop_size)
		self.calcParameterMinMaxRanges()
		self.checkHardwareConnections()
		
	def reloadFeatureSpace(self):
		self.featureSpace.reloadData(self.featureData)
		
	def show(self):
		self.w.show()
		self.featureSpace.show()
		self.isGUIshown = True

	def hide(self):
		self.w.hide()
		self.featureSpace.hide()
		self.isGUIshown = False



			












'''

- - Class StreamManager - -

Handles various ConcatStream instances


- Attributes:

- - scsynth: 
- - - SCSYNTH instance

- - arduino: 
- - - ArduinoRead instance

- - preset: 
- - - initial preset


- Usage:


'''
class StreamManager(QWidget):
	def __init__(self, scsynth, arduino, spreadChannels, startChannel):
		super().__init__(None)
		self.setWindowTitle("Stream Manager")
		self.scsynth = scsynth
		self.arduino = arduino
		self.presetParser = cp.ConfigParser()
		self.presetParser.read('./conf/StreamManagerSettings.ini')
		self.numButtons = 16
		self.keyboard_keys = [QtCore.Qt.Key_4, QtCore.Qt.Key_5, QtCore.Qt.Key_6, QtCore.Qt.Key_7, QtCore.Qt.Key_E, QtCore.Qt.Key_R, QtCore.Qt.Key_T, QtCore.Qt.Key_Y, QtCore.Qt.Key_S, QtCore.Qt.Key_D, QtCore.Qt.Key_F, QtCore.Qt.Key_G, QtCore.Qt.Key_Z, QtCore.Qt.Key_X, QtCore.Qt.Key_C, QtCore.Qt.Key_V]
		# Master tempo for start of streams (in milliseconds)
		self.masterTempo = 150
		self.spreadChannels = spreadChannels
		self.startChannel = startChannel
		self.readPresets()
		self.computeGraphics()
		self.initCTRL()
		self.initMasterTempo()

	def ConfigSectionMap(self, section):
		dict1 = {}
		options = self.presetParser.options(section)
		for option in options:
			try:
				dict1[option] = self.presetParser.get(section, option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1

	def readPresets(self):
		self.presets = np.array([], dtype=str)
		for i in range(self.numButtons):
			self.presets = np.concatenate((self.presets, [self.ConfigSectionMap("PRESETS")[str(i)]]), axis=0)
		self.presets = dict(zip(range(self.numButtons), self.presets))

	def initMasterTempo(self):
		self.masterTempoTimer = QTimer(self)
		self.masterTempoTimer.setSingleShot(False)
		self.masterTempoTimer.timeout.connect(self.masterTempoFunc)
		self.masterTempoTimer.start(self.masterTempo)

	def masterTempoFunc(self):
		for i in range(self.numButtons):
			if self.needToChangeOnMasterTempo[i] == 1:
				self.controlConcatStream(i)
				self.needToChangeOnMasterTempo[i] = 0

	def initCTRL(self):
		self.btnStates = np.zeros(self.numButtons)
		self.concatStreams = np.array(np.zeros(self.numButtons), dtype=object)
		self.actionButtons = np.array(np.zeros(self.numButtons), dtype=object)
		self.buttonIcons = np.array(np.zeros(self.numButtons), dtype=object)
		self.needToChangeOnMasterTempo = np.array(np.zeros(self.numButtons), dtype=object)
		for i in range(self.numButtons):
			if self.spreadChannels:
				self.concatStreams[i] = ConcatStream(self.scsynth, self.arduino, self.presets[i], outCh=(self.startChannel+(2*i)))
			else:
				self.concatStreams[i] = ConcatStream(self.scsynth, self.arduino, self.presets[i], outCh=self.startChannel)
			self.actionButtons[i] = QtGui.QPushButton(self.presets[i])
			self.box.addWidget(self.actionButtons[i], *self.buttonPositions[i])
			self.buttonIcons[i] = QtGui.QIcon()
			self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_red.png'))
			#self.actionButtons[i].setStyleSheet("background-color: red")
			self.actionButtons[i].setIcon(self.buttonIcons[i])
			self.actionButtons[i].clicked.connect(self.makeButtonFunc(i))
			self.actionButtons[i].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.actionButtons[i].customContextMenuRequested.connect(self.makePushButtonRightClickFunc(i))
			self.actionButtons[i].show()


	def makeButtonFunc(self, i):
		def buttonFunc():
			modifiers = QtGui.QApplication.keyboardModifiers()
			if modifiers == QtCore.Qt.ControlModifier:
				if not self.concatStreams[i].isFreezeEnabled:
					self.concatStreams[i].playFreeze()
					#self.actionButtons[i].setStyleSheet("background-color: yellow")
					self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_yellow.png'))
					self.actionButtons[i].setIcon(self.buttonIcons[i])
				else:
					self.concatStreams[i].playFreeze()
					#self.actionButtons[i].setStyleSheet("background-color: red")
					self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_red.png'))
					self.actionButtons[i].setIcon(self.buttonIcons[i])
			else:
				if self.btnStates[i] == 0:
					self.concatStreams[i].play()
					self.btnStates[i] = 1
					self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_green.png'))
					self.actionButtons[i].setIcon(self.buttonIcons[i])
				else:
						self.concatStreams[i].stop()
						self.btnStates[i] = 0
						self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_red.png'))
						self.actionButtons[i].setIcon(self.buttonIcons[i])
		return buttonFunc

	def makePushButtonFunc(self, i):
		def pushButtonFunc():
			if self.btnStates[i] == 0:
				self.concatStreams[i].play()
				self.btnStates[i] = 1
				self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_green.png'))
				self.actionButtons[i].setIcon(self.buttonIcons[i])
			else:
					self.concatStreams[i].stop()
					self.btnStates[i] = 0
					self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_red.png'))
					self.actionButtons[i].setIcon(self.buttonIcons[i])
		return pushButtonFunc

	def makePushButtonRightClickFunc(self, i):
		def pushButtonRightClickFunc():
			if not self.concatStreams[i].isGUIshown:
				self.concatStreams[i].reloadFeatureSpace()
				self.concatStreams[i].show()
			else:
				self.concatStreams[i].hide()
		return pushButtonRightClickFunc

	def makeConcatStreamFreezeFunc(self, i):
		def concatStreamFreezeFunc():
			if not self.concatStreams[i].isFreezeEnabled:
				self.concatStreams[i].playFreeze()
				self.actionButtons[i].setStyleSheet("background-color: yellow")
			else:
				self.concatStreams[i].playFreeze()
				self.actionButtons[i].setStyleSheet("background-color: red")
		return concatStreamFreezeFunc


	def computeGraphics(self):
		self.setGeometry(0, 0, 200, 200)
		self.box = QtGui.QGridLayout()
		self.setLayout(self.box)
		self.buttonPositions = [(i, j) for i in range(4) for j in range(4)]
		self.show()

	def connectOSCController(self, ip='192.168.2.2', oscPort='57200'):
		self.ip = ip
		self.oscPort = oscPort
		# OSC Dispatcher
		self.dispatcher = dispatcher.Dispatcher()
		# OSC Server
		self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.oscPort), self.dispatcher)
		self.server.serve_forever
		for i in range(self.numButtons):
			self.dispatcher.map('/OSCController/button'+i, self.makePushButtonFunc(i))

	def keyPressEvent(self, event):
		for i in range(self.numButtons):
			if event.key() == self.keyboard_keys[i]:
				self.needToChangeOnMasterTempo[i] = 1
		
	def controlConcatStream(self, i):
		modifiers = QtGui.QApplication.keyboardModifiers()
		# No modifier: start/stop stream
		if modifiers == QtCore.Qt.NoModifier:
			if self.btnStates[i] == 0:
				self.concatStreams[i].play()
				self.btnStates[i] = 1
				self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_green.png'))
				self.actionButtons[i].setIcon(self.buttonIcons[i])
			else:
				self.concatStreams[i].stop()
				self.btnStates[i] = 0
				self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_red.png'))
				self.actionButtons[i].setIcon(self.buttonIcons[i])
		# Cmd modifier: enter/leave freeze mode
		elif modifiers == QtCore.Qt.ControlModifier:
			if self.btnStates[i] == 1:
				if not self.concatStreams[i].isFreezeEnabled:
					self.concatStreams[i].isFreezeEnabled = True
					self.concatStreams[i].firstFreezeLoop = True
					self.btnStates[i] = 1
					self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_yellow.png'))
					self.actionButtons[i].setIcon(self.buttonIcons[i])
				else:
					self.concatStreams[i].isFreezeEnabled = False
					if self.btnStates[i] == 0:
						self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_red.png'))
					else:
						self.buttonIcons[i].addPixmap(QtGui.QPixmap('./img/feature_dot_green.png'))
					self.actionButtons[i].setIcon(self.buttonIcons[i])
		# Alt modifier: record/stop recording
		elif modifiers == QtCore.Qt.AltModifier:
			print("Alt modifier pressed!")
			if self.btnStates[i] == 1:
				if self.concatStreams[i].hasToRecord:
					print("Stop recording")
					self.concatStreams[i].stopRecording()
				else:
					print("Start recording")
					self.concatStreams[i].record()
		# Ctrl modifier: play/stop recording
		if modifiers == QtCore.Qt.MetaModifier:
			print("Ctrl modifier pressed!")
			if self.btnStates[i] == 0:
				if self.concatStreams[i].isPlayingRecorded:
					print("Stop recorded")
					self.concatStreams[i].stopRecorded()
				else:
					print("Play recorded")
					self.concatStreams[i].playRecorded()
				








class ConfigManager():
	def __init__(self):
		self.w = QtGui.QMainWindow()
		self.area = DockArea()
		self.w.setCentralWidget(self.area)
		self.w.resize(320,700)
		self.w.setWindowTitle('System Configuration')		
		self.paramDock = Dock("Parameters")
		self.area.addDock(self.paramDock, 'top')

		self.parameters = {
			'SCSYNTH.IP address': '127.0.0.1',
			'SCSYNTH.OSC port': 57110,
			'SCSYNTH.Start channel': 20,
			'SCSYNTH.Spread channels': True,
			'HARDWARE.Type': 'Serial',
			'HARDWARE.Serial Port': '/dev/cu.usbmodem1411',
			'HARDWARE.Number of sensors': 5
		}

		#np.save('./conf/ConfigManager', self.parameters)

		self.parameters = np.load('./conf/ConfigManager.npy').item()

		self.scsynthParameters = [
			{'name': 'SCSYNTH', 'type': 'group', 'children': [
				{'name': 'IP address', 'type': 'str', 'value': self.parameters['SCSYNTH.IP address']},
				{'name': 'OSC port', 'type': 'int', 'value': self.parameters['SCSYNTH.OSC port']},
				{'name': 'Start channel', 'type': 'int', 'value': self.parameters['SCSYNTH.Start channel']},
				{'name': 'Spread channels', 'type': 'bool', 'value': self.parameters['SCSYNTH.Spread channels']}
			]}
		]

		self.hardwareParameters = [
			{'name': 'HARDWARE', 'type': 'group', 'children': [
				{'name': 'Type', 'type': 'list', 'values': ['Serial', 'OSC'], 'value': self.parameters['HARDWARE.Type']},
				{'name': 'Serial Port', 'type': 'str', 'value': self.parameters['HARDWARE.Serial Port']},
				{'name': 'Number of sensors', 'type': 'int', 'value': self.parameters['HARDWARE.Number of sensors']},
			]}
		]




		self.p1 = Parameter.create(name='params', type='group', children=self.scsynthParameters)
		self.t1 = ParameterTree()
		self.t1.setParameters(self.p1, showTop=False)
		self.p1.sigTreeStateChanged.connect(self.change1)
		self.paramDock.addWidget(self.t1)

		self.p2 = Parameter.create(name='params', type='group', children=self.hardwareParameters)
		self.t2 = ParameterTree()
		self.t2.setParameters(self.p2, showTop=False)
		self.p2.sigTreeStateChanged.connect(self.change2)
		self.paramDock.addWidget(self.t2)

		self.analyzeBtn = QtGui.QPushButton('Analyze Datasets')
		self.paramDock.addWidget(self.analyzeBtn)
		self.analyzeBtn.clicked.connect(self.analyze)

		self.w.show()

	def change1(self, param, changes):
		for param, change, data in changes:
			print(param, change, data)
			path = self.p1.childPath(param)
			if path is not None:
				childName = '.'.join(path)
			else:
				childName = param.name()
			self.parameters[childName] = data
			np.save('./conf/ConfigManager', self.parameters)

	def change2(self, param, changes):
		for param, change, data in changes:
			print(param, change, data)
			path = self.p2.childPath(param)
			if path is not None:
				childName = '.'.join(path)
			else:
				childName = param.name()
			self.parameters[childName] = data
			np.save('./conf/ConfigManager', self.parameters)

	def analyze(self):
		for _file in os.listdir(sound_file_path):
			if len(_file.split('.')) > 1:
				if _file.split('.')[1] == 'wav':
					runEssentiaExtractor(feature_extractor_path, sound_file_path+_file, feature_file_path+_file.split('.')[0]+'.txt', str(sample_rate)+" "+str(fft_frame_size)+" "+str(fft_hop_size))
					saveFeatureDataAsNPY(feature_file_path+_file.split('.')[0], all_features)
					os.remove(feature_file_path+_file.split('.')[0]+'.txt')

			



'''
Emmerson / Landy
Laura Zattra - Studiare computer music
Fabian Lévy
Marta Grabòoz
Carratelli
H. Schenker
A. Lomax
Diana Doich - The psicology of music
Balaban - artificial intelligence (1992)
Bent Drabkin - Analisi musicale
Roads (1978) - Composing Grammars
O. Laske
Holtzman - Computer Grammars / CAC
Tae Hong Park - Easy Squema - Perceptual Feature Extraction


congnitivismo
emozione
Hindemit -> simbologia
Nastiez -> semiologia musicale
A. Forte -> teoria degli insiemi
K. Stockhausen -> Formel
W. Berry -> grammatica come performance
Lerdahl
Jackendoff
Schwanauer Levitt - Machine Models of Music
Roads - Computer Music Tutorial - capitolo modelli di composizione computazionale
Xenakis - Formalized Music


Delalande Fremiot -> Unites semiotiques temporelles
Le condotte d'ascolto

Roger Reynolds - The angel of death
'''


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	#if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
	#	QtGui.QApplication.instance().exec_()



