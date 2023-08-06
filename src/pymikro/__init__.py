
import os
import hid
import json

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 




class MaschineMikroMk3:
	def __init__(self):
		self.lightsState = {}

		self.loadSettings('maschine_mikro_mk3.json')

		self.vid = int(self.settings['vid'], 16)
		self.pid = int(self.settings['pid'], 16)

		self.hid = hid.Device(self.vid, self.pid)

	def loadSettings(self, fileName):
		filePath = self.getPath(fileName)
		with open(filePath) as f:
			self.settings = json.load(f)

	def getPath(self, fileName):
		return os.path.join(os.path.dirname(__file__), fileName)

	def showConnInfo(self):
		print(f'Device manufacturer: {self.hid.manufacturer}')
		print(f'Product: {self.hid.product}')
		print(f'Serial Number: {self.hid.serial}')

	def read(self):
		bufSize = 1000
		timeout = 10
		b = self.hid.read(bufSize, timeout)
		return list(b)

	def write(self, data):
		self.hid.write(bytes(data))

	# ---------------------------- maschine ouput

	# ------------ buttons

	def decodeBtns(self, rawCmd):
		def getPressedBtns(rawCmd):
			btnBytes = bytes(rawCmd[1:6])
			btnVal = int.from_bytes(btnBytes, byteorder='little')
			btnOrder = self.settings['button']['order']

			btns = []
			for btnIndex in range(len(btnOrder)):
				if (btnVal % 2) == 1:
					btns.append(btnOrder[btnIndex])
				btnVal = btnVal >> 1

			return {'btn_pressed': btns}

		def getEncoderInfo(rawCmd):
			info = {}

			encoderPos = rawCmd[7]
			encoderMove = 0
			if hasattr(self, 'lastEncoderPos'):
				diff = encoderPos - self.lastEncoderPos
				if abs(diff-16) < abs(diff):
					encoderMove = diff-16
				elif abs(diff+16) < abs(diff):
					encoderMove = diff+16
				else:
					encoderMove = diff
			self.lastEncoderPos = encoderPos

			info['encoder_pos'] = encoderPos
			info['encoder_move'] = encoderMove
			info['encoder_touched'] = (rawCmd[6] == 1)

			return info

		def getStripValue(rawCmd):
			info = {}

			info['strip_pos_1'] = rawCmd[10]
			info['strip_pos_2'] = rawCmd[12]
			#info['strip_time'] = rawCmd[9]*256 + rawCmd[8]

			return info

		if len(rawCmd) > 10 and rawCmd[0] == 1:
			ret = {'cmd': 'btn'}

			ret.update(getPressedBtns(rawCmd))
			ret.update(getEncoderInfo(rawCmd))
			ret.update(getStripValue(rawCmd))

			return ret

		return None

	# ------------ pads

	def decodePads(self, rawCmd):
		if len(rawCmd) > 4 and rawCmd[0] == 2:
			info = {'cmd': 'pad'}

			info['pad_nb'] = self.settings['pad']['order'][rawCmd[1]]

			info['pad_val'] = (rawCmd[2] & 0x0f)*256 + rawCmd[3]

			ctrl = rawCmd[2] & 0xf0
			info['touched'] = (ctrl == 0x40)
			info['pressed'] = (ctrl == 0x10)
			info['released'] = ((ctrl == 0x20) or (ctrl == 0x30))

			return info

		return None

	# ------------ read command

	def readCmd(self):
		rawCmd = self.read()
		decodeFuncs = [self.decodeBtns, self.decodePads]
		for dec in decodeFuncs:
			cmd = dec(rawCmd)
			if cmd:
				return cmd

		return None

	# ---------------------------- maschine input

	# ------------ lights

	def setLights(self, state):
		self.lightsState = state

	def getLights(self):
		return self.lightsState

	def setLight(self, elemType, elemRef, val=4, color=None):
		if elemType not in self.lightsState:
			self.lightsState[elemType] = {}

		self.lightsState[elemType][elemRef] = {'val': val, 'color': color}

	def updLights(self):
		def getElemNb(elemType, elemRef):
			if elemType in ['pad', 'button']:
				if elemRef == 'enter':
					return None
				return self.settings[elemType]['order'].index(elemRef)
			return elemRef

		def getColorByte(elemType, elem):
			byte = 0x00
			if elemType in ['pad', 'strip']:
				colorNb = self.settings['color'].index(elem['color'])
				if elem['val'] != 0:
					byte = 0x04*colorNb + elem['val']
			if elemType == 'button':
				byte = self.settings['button']['brightness'][elem['val']]
			return byte

		def setColor(buf, elemType, offset):
			if elemType not in self.lightsState.keys():
				return 

			for elemRef in self.lightsState[elemType].keys():
				elem = self.lightsState[elemType][elemRef]

				elemNb = getElemNb(elemType, elemRef)
				if elemNb != None:
					byte = getColorByte(elemType, elem)
					buf[offset+elemNb] = byte

		buf = [0x80] + [0x00]*90

		setColor(buf, 'button', 1)
		setColor(buf, 'pad', 40)
		setColor(buf, 'strip', 56)

		self.write(buf)

	# ------------ screen

	def setScreen(self, text, size=14):
		def getBitImg(text, size):
			img = Image.new('1', (128, 32))
			draw = ImageDraw.Draw(img)
			fileName = "DejaVuSans.ttf"
			fontPath = self.getPath(fileName)
			font = ImageFont.truetype(fontPath, size)
			textSp = text.split('\n')+['']
			draw.text((0, 0), textSp[0], 1, font=font)
			draw.text((0, 16), textSp[1], 1, font=font)
			return img

		def getBuffer(img):
			buf = [0xff]*512
			for i in range(128):
				for line in range(4):
					byteVal = 0x00
					for bit in range(8):
						byteVal = byteVal << 1
						pixVal = img.getpixel((i, (8*line)+(7-bit)))
						if pixVal == 0:
							byteVal += 1
					buf[128*line + i] = byteVal
			return buf

		def writeBuf(buf):
			headerHi = [0xe0, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x02, 0x00]
			headerLo = [0xe0, 0x00, 0x00, 0x02, 0x00, 0x80, 0x00, 0x02, 0x00]
			self.write(headerHi+buf[:256])
			self.write(headerLo+buf[256:])

		img = getBitImg(text, size)
		buf = getBuffer(img)
		writeBuf(buf)

