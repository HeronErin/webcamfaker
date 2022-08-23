import cv2

class base:
	SETTINGS = {}
	NAME = "Normal"
	def makeSettings(self):
		yield "horizontal flip", False
		yield "vertical flip", True
	def __init__(self):
		self.SETTINGS = {}
		for name, value in self.makeSettings():
			setting = {}
			if type(value) is type:
				setting["type"] = value.__name__
				setting["value"] = None
			else:
				setting["type"] = type(value).__name__
				setting["value"] = value
			self.SETTINGS[name] = setting
	def getSetting(self, key): 
		if self.SETTINGS.get(key) is None: return None
		return self.SETTINGS.get(key)["value"]
	def onFrame(self, frame, dtime):
		if self.getSetting("horizontal flip"):
			frame = cv2.flip(frame, 1)
		if self.getSetting("vertical flip"):
			frame = cv2.flip(frame, 0)
		return frame