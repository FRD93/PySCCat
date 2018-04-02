# -*- coding: utf-8 -*-

#################################################################################
# CONCATENATIVE SYNTHESIZER
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



'''
TODO:

1) Implementare neighbor modes nei parametri
2) Correggere reboot necessario dopo aggiunta preset/file audio
3) Implementare record/analisi in rt di suoni da microfono
7) Implementare segmentazione/analisi per onset
'''



import time
from dep.graphics import *
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder



''' Load configuration file /conf/config.ini '''
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
scsynth_path = ConfigSectionMap("SCSYNTH")['scsynth_path']
scsynth_def_path = ConfigSectionMap("SCSYNTH")['scsynth_def_path']
scsynth_reverb_inCh = ConfigSectionMap("SCSYNTH")['reverb_in_ch']
#scsynth_spread_Stream_Channels = ConfigSectionMap("SCSYNTH")['scsynth_spread_Stream_Channels']
sound_file_path        = ConfigSectionMap("DIRECTORIES")['sound_file_path']



''' GUI '''
app = QtGui.QApplication([])

''' Config Manager '''
configManager = ConfigManager()
''' Setup scsynth '''
scsynth = SCSYNTH(ip=configManager.parameters['SCSYNTH.IP address'], scsynthOSCPort=configManager.parameters['SCSYNTH.OSC port'], pythonOSCPort=9999)
for path in os.listdir(scsynth_def_path):
	if len(path.split(".")) > 1:
		if path.split(".")[1] == 'scsyndef':
			scsynth.loadDefFile(scsynth_def_path+path)
soundfiles = np.array([])
for path in os.listdir(sound_file_path):
	if len(path.split(".")) > 1:
		if path.split(".")[1] == 'wav':
			soundfiles = np.concatenate((soundfiles, [sound_file_path+path]), axis=0)
for buf_id, path in enumerate(soundfiles):
		scsynth.allocBuffer(path, buf_id)
		print(buf_id, path)
''' Connect to Arduino™ '''
try:
	arduino = ArduinoRead(port=configManager.parameters['HARDWARE.Serial Port'])
except:
	arduino = ArduinoRead(port=None)
''' Start stream manager '''
streamManager = StreamManager(scsynth=scsynth, arduino=arduino, spreadChannels=configManager.parameters['SCSYNTH.Spread channels'], startChannel=configManager.parameters['SCSYNTH.Start channel'])
''' Start gesture space '''
gestureSpace = GestureSpace(arduino)


r = RecordedView()



if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()


