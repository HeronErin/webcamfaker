import eel, cv2, numpy, base64, os, importlib, sys, json, threading, pyfakewebcam, time
from functools import partial

modes = []
maindir = os.path.abspath(os.path.dirname(__file__))
for m in os.listdir(os.path.join(maindir, "modes")):
	if os.path.isfile(os.path.join(maindir, "modes", m)):
		md = importlib.import_module("modes."+m.replace(".py", ""))
		modes.append( md.__dict__[m.replace(".py", "")]() )
class main:
	desiredFrameRate = 20

	currentMode = modes[0]
	running =True
	frameAccess = threading.Condition()
	frameControll = threading.Condition()
	frame = None
	lastdelta=0
	newframe = None
	def run(self):
		if os.path.exists("settings.json"):
			for m in json.load(open("settings.json", "r")):
				for md in modes:
					if md.NAME == m[0]:
						md.SETTINGS = m[1]

		eel.init("webui")
		self.vcam = pyfakewebcam.FakeWebcam('/dev/video2', 640, 480)
		self.vid = cv2.VideoCapture(0)
		self.replay = None
		self.output = None
		ret, frame = self.vid.read()
		threading.Thread(target=self.frameThread).start()
		threading.Thread(target=self.mainTicker).start()
		
		@eel.expose
		def getimg():
			# self.frameAccess.acquire()
			frame = self.frame.copy()
			# self.frameAccess.release()
			return base64.b64encode(cv2.imencode('.jpg', frame)[1].tobytes()).decode("utf-8")
		@eel.expose
		def getsettings():

			return json.dumps([ [k, list(v.values())]  for k, v in list(self.currentMode.SETTINGS.items())])
		@eel.expose
		def getmodes():
			return json.dumps([m.NAME for m in modes])
		@eel.expose
		def setmode(s):
			for m in modes:
				if m.NAME == s:
					self.currentMode = m
			print(s)
		@eel.expose
		def setsetting(s, v):
			if self.currentMode.SETTINGS[s]["type"] == type(v).__name__:
				self.currentMode.SETTINGS[s]["value"] = v
				json.dump([[m.NAME, m.SETTINGS] for m in modes], open("settings.json", "w"))
		@eel.expose
		def startrecording():
			if self.replay is None:
				self.frameControll.acquire()
				if not self.output is None:
					self.output = None
					
				else:
					
					width, height = self.frame.shape[1], self.frame.shape[0]
					self.output = cv2.VideoWriter("record.avi", cv2.VideoWriter_fourcc(*'MPEG'), self.desiredFrameRate, (width, height))
				self.frameControll.release()
		@eel.expose
		def replayrecording():
			self.frameControll.acquire()
			if self.replay is None:
				self.replay =  cv2.VideoCapture("record.avi")
				self.vid.release()
			else:
				self.replay = None
				self.vid = cv2.VideoCapture(0)
			self.frameControll.release()

		try:
			print("http://localhost:8000/main.html")
			eel.start("main.html")
			
		finally:
			self.running = False
	def frameThread(self):
		while self.running:

			self.frameControll.acquire()
			ot = time.time()
			sp = (1/self.desiredFrameRate)-self.lastdelta
			time.sleep(sp if sp > 0 else 0)
			
			frame = None
			
			if self.replay is None:
				frame = self.vid.read()[1]
				if not self.output is None:
					self.output.write(frame)
			else:

				frame = self.replay.read()[1]
				if frame is None:
					self.replay.release()
					self.replay =  cv2.VideoCapture("record.avi")
					frame = self.replay.read()[1]
			dt = time.time()-ot
			self.frameControll.release()
			# self.frameAccess.acquire()

			self.newframe = frame
	def mainTicker(self):
		while self.running:

			# self.frameControll.acquire()
			ot = time.time()
			sp = (1/self.desiredFrameRate)-self.lastdelta
			time.sleep(sp if sp > 0 else 0)
			if self.newframe is None: 
				continue

			dt = time.time()-ot
			# self.frameAccess.acquire()
			self.frame = self.currentMode.onFrame(self.newframe.copy(), dt)
			# self.frameAccess.release()
			self.lastdelta = dt
			if self.frame is not None:
				self.vcam.schedule_frame(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
			
			
if "__main__" == __name__:
	main().run()
