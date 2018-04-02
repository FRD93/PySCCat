# -*- coding: utf-8 -*-

####################################################################################
# THIS LIBRARY CONTAINS CLASSES FOR INTERFACING WITH ARDUINO MICROCONTROLLER.
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
####################################################################################

import time
import serial
from .supercollider import *
import numpy as np
from threading import Thread











'''

- - Class ArduinoRead - -

This class serves to read the sensor data sent from the Arduino™ board via serial.

- Attributes:

- - port: 
- - - the port name to which the Arduino™ is connected

- - baudRate: 
- - - baud rate of the serial transmission


- Usage:

arduino = ArduinoRead(port=None)

'''
class ArduinoRead(Thread):
	def __init__(self, port='/dev/cu.usbmodem1411', baudRate=9600):
		Thread.__init__(self)
		self.port = port
		self.baudRate = baudRate
		if self.port != None:
			self.ser = serial.Serial(self.port, self.baudRate)
		self.pots = np.zeros(5)
		self.data = b''
		self.old_data = b''
		self.isRunning = False
		self.daemon = True
		self.lags = np.ndarray(len(self.pots), dtype=np.object)
		for i in range(len(self.pots)):
			self.lags[i] = Lag(lagTime=3, name=str(i))
		self.start()

	def run(self):
		self.isRunning = True
		while True:
			if self.port != None:
				if self.isRunning == False:
					break
				self.old_data = self.data
				self.data = self.ser.readline()
				if self.old_data == b'a1\r\n':
					self.pots[0] = float(self.data[:-4]) / 1024.0
				if self.old_data == b'a2\r\n':
					self.pots[1] = float(self.data[:-4]) / 1024.0
				if self.old_data == b'a3\r\n':
					self.pots[2] = float(self.data[:-4]) / 1024.0
				if self.old_data == b'a4\r\n':
					self.pots[3] = float(self.data[:-4]) / 1024.0
				if self.old_data == b'a5\r\n':
					self.pots[4] = float(self.data[:-4]) / 1024.0
			elif self.port == None:
				self.pots = np.random.rand(len(self.pots))
				for i in range(len(self.pots)):
					self.lags[i].setNewValue(self.pots[i])
				time.sleep(0.8)
