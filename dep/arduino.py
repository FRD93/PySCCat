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
		self.sensor_names = [b'a1\r\n', b'a2\r\n', b'a3\r\n', b'a4\r\n', b'a5\r\n', b'mn\r\n', b'br\r\n', b'ba\r\n']
		self.control_names = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Mean', 'Bar. Radius', 'Bar. Angle']
		self.pots = np.zeros(len(self.sensor_names))
		self.data = b''
		self.old_data = b''
		self.isRunning = False
		self.daemon = True
		self.lags = np.ndarray(len(self.pots), dtype=np.object)
		print('number of lags: {}'.format(len(self.pots)))
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
				for i in range(len(self.pots)):
					if self.old_data == self.sensor_names[i]:
						self.pots[i] = float(self.data[:-4]) / 1024.0
			elif self.port == None:
				self.pots = np.random.rand(len(self.pots))
				for i in range(len(self.pots)):
					self.lags[i].setNewValue(self.pots[i])
				time.sleep(0.8)
			#print(self.control_names)
			#print(self.pots)
