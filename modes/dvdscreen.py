# from . import base
# import cv2, enum, random
# import numpy as np
# class Dirs(enum.Enum):
# 	NorthEast = enum.auto()
# 	NorthWest = enum.auto()
# 	SouthEast = enum.auto()
# 	SouthWest = enum.auto()
# def randomDir(current=None):
# 	b = None
# 	while ((b:=random.choice([Dirs.NorthEast, Dirs.NorthWest, Dirs.SouthWest, Dirs.SouthEast])) ==current): pass
# 	print(b)
# 	return b
# class dvdscreen (base.base):
# 	NAME = "dvd screensaver"
# 	boxx = 1
# 	boxy = 1
# 	currentDir = randomDir()
# 	def makeSettings(self):

# 		yield "horizontal flip", False
# 		yield "vertical flip", False

# 		yield "dvd box width", 175
# 		yield "box speed", 5
# 	def isValidMove(self, cx, cy, width, height,swidth, sheight,  dir, speed):
		
# 		if dir == Dirs.NorthEast:
# 			cx+=speed
# 			cy-=speed
# 		elif dir == Dirs.NorthWest:
# 			cx-=speed
# 			cy-=speed
# 		elif dir == Dirs.SouthEast:
# 			cx+=speed
# 			cy+=speed
# 		elif dir == Dirs.SouthWest:
# 			cx-=speed
# 			cy+=speed
# 		print(cx, cy, width, height, swidth, sheight, dir, (cx < 0, cx+width > swidth-1), (cy < 0, cy+height > sheight-1))
# 		if cx < 0 or cx+width > swidth-1:
# 			return None
# 		if cy < 0 or cy+height > sheight-1: 
# 			return None
# 		return cx, cy
# 	def onFrame(self, frame):
# 		frame = base.base.onFrame(self, frame)
# 		back = np.zeros((480,640,3), dtype=np.uint8)
# 		try:
# 			boxWidth=self.getSetting("dvd box width")
# 			heigh = int((frame.shape[0]/frame.shape[1]) *boxWidth)
# 			if heigh <= 0: heigh = 1
# 			if boxWidth <= 0: boxWidth = 1
# 			fr = cv2.resize(frame, dsize=[boxWidth, heigh])
# 			h1, w1 = fr.shape[:2]
# 			ret = self.isValidMove(self.boxx, self.boxy, w1, h1, frame.shape[1], frame.shape[0], self.currentDir, self.getSetting("box speed"))
# 			print(ret)
# 			if ret is None:
# 				self.currentDir = randomDir(self.currentDir)
# 				return self.onFrame(frame)
# 			else:
# 				self.boxx = ret[1]
# 				self.boxy = ret[0]
# 				back[self.boxx:self.boxx+h1,self.boxy:self.boxy+w1] = fr 
# 				return back
# 		except TypeError: return back


from . import base
import cv2, enum, random
import numpy as np
class dvdscreen (base.base):
	NAME = "dvd screensaver"
	boxx = 100
	boxy = 100
	tx, ty = 1, 1

	def makeSettings(self):

		yield "horizontal flip", False
		yield "vertical flip", False
		yield "randomize bounce", False

		yield "dvd box width", 175
		yield "box speed", 5
	def isValidMove(self, cx, cy, width, height,swidth, sheight,  dir, speed):
		
		if dir == Dirs.NorthEast:
			cx+=speed
			cy-=speed
		elif dir == Dirs.NorthWest:
			cx-=speed
			cy-=speed
		elif dir == Dirs.SouthEast:
			cx+=speed
			cy+=speed
		elif dir == Dirs.SouthWest:
			cx-=speed
			cy+=speed
		print(cx, cy, width, height, swidth, sheight, dir, (cx < 0, cx+width > swidth-1), (cy < 0, cy+height > sheight-1))
		if cx < 0 or cx+width > swidth-1:
			return None
		if cy < 0 or cy+height > sheight-1: 
			return None
		return cx, cy
	def __init__(self):
		base.base.__init__(self)
		self.tx, self.ty = random.choice([1, -1]), random.choice([1, -1])
	def onFrame(self, frame, dtime):
		dtime*1000
		frame = base.base.onFrame(self, frame, dtime)
		back = np.zeros((480,640,3), dtype=np.uint8)

		boxWidth=self.getSetting("dvd box width")
		heigh = int((frame.shape[0]/frame.shape[1]) *boxWidth)
		if heigh <= 0: heigh = 1
		if boxWidth <= 0: boxWidth = 1
		fr = cv2.resize(frame, dsize=(boxWidth, heigh))
		h1, w1 = fr.shape[:2]
		tempx =int( (self.boxx)+ self.tx*self.getSetting("box speed")*dtime )
		tempy =int( (self.boxy)+ self.ty*self.getSetting("box speed")*dtime )
		doset = True
		if tempx < 0 or tempx > frame.shape[0]-fr.shape[0]:
			self.tx *= -1
			if self.getSetting("randomize bounce"):
				self.ty *= random.choice([1, -1])
			doset = False
		if tempy < 0 or tempy > frame.shape[1]-fr.shape[1]:
			self.ty *= -1 
			if self.getSetting("randomize bounce"):
				self.tx *= random.choice([1, -1])
			doset = False
		if doset:
			self.boxx = tempx
			self.boxy = tempy


		back[self.boxx:self.boxx+h1,self.boxy:self.boxy+w1] = fr 
		return back
