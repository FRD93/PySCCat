# -*- coding: utf-8 -*-

####################################################################################
# THIS LIBRARY CONTAINS CLASSES FOR INTERFACING WITH SCSYNTH AUDIO SYNTHESIS SERVER.
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

import os
import time
import random
import subprocess
import numpy as np
from threading import Thread
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder



'''

- - Class SCSYNTH - -

This class connects to a running scsynth process
via OSC and allows to send and receive messages.


- Attributes:

- - ip: 
- - - ip address of the running scsynth process

- - port: 
- - - listening port of the running scsynth process


- Usage:

scsynth = SCSYNTH("127.0.0.1", 57110)
scsynth.sendMessage("/s_new", ["default", -1, 0, 0, "freq", 440, "amp", 0.5])

'''
class SCSYNTH:
	''' Connect to scsynth '''
	def __init__(self, ip="127.0.0.1", scsynthOSCPort=57110, pythonOSCPort=9999):
		self.ip = ip
		self.scsynthOSCPort = scsynthOSCPort
		self.pythonOSCPort = pythonOSCPort
		self.busyNodes = [3]
		self.connect()

	''' Start Server '''
	def startServer(self, scsynthPath):
		#print(os.popen(scsynthPath+' -u {} -c 128 -a 128 -i 2 -o 2 -z 32 -Z 32 -n 4096 -m 262144 -S 44100 -D 0'.format(self.scsynthOSCPort, )).read())
		subprocess.call(scsynthPath+' -u {} -c 128 -a 128 -i 2 -o 2 -z 32 -Z 32 -n 4096 -m 262144 -S 44100 -D 0 &'.format(self.scsynthOSCPort), shell=True)
		try:
			self.connect()
		except:
			print("scsynth already running with other client...")

	''' Create a OSC Client and a OSC Server to share data '''
	def connect(self):
		# OSC Client
		self.client = udp_client.SimpleUDPClient(self.ip, self.scsynthOSCPort)
		# OSC Dispatcher
		self.dispatcher = dispatcher.Dispatcher()
		# OSC Server
		self.server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", self.pythonOSCPort), self.dispatcher)
		self.server.serve_forever
		return self

	''' Send a OSC Message to scsynth's OSC Server '''
	def sendMessage(self, tag="/s_new", args=["default", -1, 0, 0, "freq", 1240, "amp", 1]):
		self.client.send_message(tag, args)
		return self

	''' Alloc a buffer (shortcut of sendMessage()) '''
	def allocBuffer(self, fullpath, bufnum):
		self.sendMessage("/b_allocRead", [bufnum, os.path.abspath(fullpath)])

	''' Load a synth definition file to the server '''
	def loadDefFile(self, fullpath):
		self.sendMessage("/d_load", [fullpath])
	








'''

- - Class Synth - -

This class is a convenient port of SuperCollider's Synth class.


- Attributes:

- - server: 
- - - an istance of SCSYNTH class

- - name: 
- - - name of the SynthDef to run

- - args:
- - - pairs of argument name and value

- - addAction:
- - - "head", "tail", "before" or "after"

- - targetID:
- - - addAction's target node


- Usage:

scsynth = SCSYNTH()
id = 0
while True:
	if id % 4 == 0:
		x = Synth(scsynth, "default", ["freq", 440])
	if id % 3 == 0:
		y = Synth(scsynth, "default", ["freq", 660])
	if id % 5 == 0:
		z = Synth(scsynth, "default", ["freq", 880])
	if id % 7 == 0:
		q = Synth(scsynth, "default", ["freq", 220, "amp", 1])
	id = id + 1
	time.sleep(0.125)

'''

class Synth:
	''' Run the Synth (as SuperCollider's "Synth.new();") '''
	def __init__(self, server, name="default", args=[], addAction="head", targetID=1000):
		self.server = server
		self.name = name
		self.args = args
		self.targetID = targetID
		# check addAction
		if addAction == "head":
			self.addAction = 0
			self.args = [self.name, -1, 0, 0] + self.args
		elif addAction == "tail":
			self.addAction = 1
			self.args = [self.name, -1, self.addAction, self.targetID] + self.args
		elif addaction == "before":
			self.addAction = 2
			self.args = [self.name, -1, self.addAction, self.targetID] + self.args
		elif addaction == "after":
			self.addAction = 3
			self.args = [self.name, -1, self.addAction, self.targetID] + self.args
		# find a free node in the server
		self.node = np.random.randint(1001, 99999)
		while self.node in self.server.busyNodes:
			self.node = np.random.randint(1001, 99999)
		# run synth in the server
		self.server.sendMessage("/s_new", self.args)

	''' Set a parameter's value of the synth (as SuperCollider's "Synth.set();") '''
	def set(self, param, value):
		self.server.sendMessage("/n_set", [self.node, param, value])
		return self

	''' Set a set of parameter's value of the synth (as SuperCollider's "Synth.setn();") '''
	def setn(self, paramValuePairs):
		self.server.sendMessage("/n_setn", paramValuePairs)
		return self

	''' Free the Synth (as SuperCollider's "Synth.free();") '''
	def free(self):
		self.server.sendMessage("/n_free", [self.node])
		return self











'''

- - Class Lag - -

This class emulates SuperCollider's Lag class.

- Attributes:

- - lagTime: 
- - - time to reach a value from another

- - power: 
- - - shape of the curves

- - numSteps:
- - - number of steps to reach the end value

- - startValue:
- - - start point of the curve

- - name:
- - - name of the lag


- Usage:

lags = np.ndarray(5, dtype=np.object)
for i in range(len(lags)):
	lags[i] = Lag(name=str(i))
	lags[i].setNewValue(np.random.randint(1.0, 30.0))

'''
class Lag():
	def __init__(self, lagTime=0.1, power=1, numSteps=100, startValue=0.0, name="lag1"):
		self.name = name
		self.lagTime = lagTime
		self.startValue = startValue
		self.currentValue = self.startValue
		self.endValue = self.startValue
		self.power = power
		self.numSteps = numSteps
		self.counter = 0
		self.break_ = False
		self.isRunning = False

	def process(self, newValue=1.0):
		self.endValue = newValue
		self.isRunning = True
		while (self.counter <= self.numSteps):
			if (self.break_ == True):
				self.break_ = False
				self.startValue = self.currentValue
				break
			self.currentValue = self.startValue + ((self.endValue - self.startValue) * np.power(self.counter / self.numSteps, self.power))
			self.counter = self.counter + 1
			time.sleep(self.lagTime / self.numSteps)
		self.startValue = self.currentValue
		self.isRunning = False
		self.counter = 0

	def setNewValue(self, newValue=1.0):
		if (self.isRunning == True):
			self.break_ = True
		self.thread = Thread(target=self.process, args=[newValue])
		self.thread.start()

	def setLagTime(self, newLagTime=0.1):
		self.lagTime = newLagTime

	def getValue(self):
		return self.currentValue













'''

- - Class CSThread - -

This class executes a concatenative synthesis thread with real time control.


- Attributes:

- - server: 
- - - an istance of SCSYNTH class

- - name: 
- - - name of the SynthDef to run

- - args:
- - - pairs of argument name and value

- - addAction:
- - - "head", "tail", "before" or "after"

- - targetID:
- - - target node 


- Usage:

scsynth = SCSYNTH()
id = 0
while True:
	if id % 4 == 0:
		x = Synth(scsynth, "default", ["freq", 440])
	if id % 3 == 0:
		y = Synth(scsynth, "default", ["freq", 660])
	if id % 5 == 0:
		z = Synth(scsynth, "default", ["freq", 880])
	if id % 7 == 0:
		q = Synth(scsynth, "default", ["freq", 220, "amp", 1])
	id = id + 1
	time.sleep(0.125)

'''
class CSThread(Thread):
	def __init__(self, server, bufnum=0, grainFreq=100, grainDur=0.1, pos=0, amp=0.5, pan=0.5, rate=1, atk=0.5, outCh=20):
		Thread.__init__(self)
		self.verbose = False
		self.scsynth = server
		self.bufnum = bufnum
		self.grainFreq = grainFreq
		self.roundGFreq = 0.0
		self.grainDur = grainDur
		self.pos = pos
		self.amp = amp
		self.pan = pan
		self.rate = rate
		self.roundPitch = 0.0
		self.atk = atk
		self.outCh = outCh
		self.neighborMode = 'Random'
		self.isRunning = False
		self.grainCounter = 0
		self.daemon = True
		self.start()

	def _round(self, number, thresh):
		if thresh != 0:
			result = round(float(number) / thresh) * thresh
			if result != 0:
				return result
			else:
				return thresh
		else:
			return number



	def run(self):
		self.isRunning = True
		self.grainCounter = 0
		while self.isRunning:
			if self.verbose:
				print('buf: {} dur: {} pos: {} amp: {} pan: {} rate: {} atk: {}'.format(type(self.bufnum), type(self.grainDur), type(self.pos), type(self.amp), type(self.pan), type(self.rate), type(self.atk)))

			if self.isRunning == False:
				break
			# RUN SYNTH ONLY IF AMPLITUDE > 0.0
			if self.amp > 0.0:
				print(self.bufnum, self.outCh)
				if isinstance(self.pos, (list, np.ndarray, tuple)):
					if self.neighborMode == 'Circular':
						self.pos = np.concatenate((self.pos, self.pos[::-1]), axis=0)
					if self.neighborMode == 'Random':
						random.shuffle(self.pos)
						self.chosenPos = int(self.pos[self.grainCounter % len(self.pos)])
					Synth(self.scsynth, "SCGrain", ["buf", self.bufnum, "dur", self.grainDur, "pos", self.chosenPos, "amp", self.amp, "pan", self.pan, "rate", self._round(self.rate, self.roundPitch), "atk", self.atk, "outCh", self.outCh])
					#print("neighbors:", self.pos, "index:", self.grainCounter % len(self.pos), "pos:", int(self.pos[self.grainCounter % len(self.pos)]))
				else:
					self.chosenPos = self.pos
					Synth(self.scsynth, "SCGrain", ["buf", self.bufnum, "dur", self.grainDur, "pos", int(self.pos), "amp", self.amp, "pan", self.pan, "rate", self.rate, "atk", self.atk, "outCh", self.outCh])
			'''
			if isinstance(self.grainFreq, (list, np.ndarray, tuple)):
				time.sleep(1.0 / self.grainFreq[self.grainCounter % (len(self.grainFreq)-1)])
			else:
			'''
			time.sleep(self._round(1.0 / self.grainFreq, self.roundGFreq))
			self.grainCounter = self.grainCounter + 1

	def stop(self):
		self.isRunning = False
		self.grainCounter = 0

	def setGrainFreq(self, newGrainFreq):
		self.grainFreq = float(newGrainFreq)

	def setGrainDur(self, newGrainDur):
		self.grainDur = float(newGrainDur)

	def setBufnum(self, newBufnum):
		self.bufnum = int(newBufnum)

	def setPos(self, newPos):
		self.pos = newPos

	def setAmp(self, newAmp):
		self.amp = float(newAmp)

	def setPan(self, newPan):
		self.pan = float(newPan)

	def setRate(self, newRate):
		self.rate = float(newRate)

	def setAtk(self, newAtk):
		self.atk = float(newAtk)

	def setOutCh(self, newOutCh):
		self.outCh = int(newOutCh)

	def setRoundGFreq(self, newRoundGFreq):
		self.roundGFreq = float(newRoundGFreq)

	def setRoundPitch(self, newRoundPitch):
		self.roundPitch = float(newRoundPitch)

	def setParam(self, param, value):
		if param == "Pos":
			self.setPos(value)
		if param == "GrainFreq":
			self.setGrainFreq(value)
		if param == "RoundGFreq":
			self.setRoundGFreq(value)
		if param == "GrainDur":
			self.setGrainDur(value)
		if param == "Amplitude":
			self.setAmp(value)
		if param == "Panning":
			self.setPan(value)
		if param == "GrainAtk":
			self.setAtk(value)
		if param == "Pitch":
			self.setRate(value)
		if param == "RoundPitch":
			self.setRoundPitch(value)

	def getParameters(self):
		self.params = {'Pos': self.pos, 'GrainFreq': self.grainFreq, 'GrainDur': self.grainDur, 'Amplitude': self.amp, 'Panning': self.pan, 'GrainAtk': self.atk, 'Pitch': self.rate, 'RoundGFreq': self.roundGFreq, 'RoundPitch': self.roundPitch}
		return self.params








