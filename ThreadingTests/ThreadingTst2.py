
from threading import Thread
import time
import RPi.GPIO as gpio

global MyGlobalVariable
MyGlobalVariable = 0
counter = 0


class MyTimedThread:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global MyGlobalVariable
		MyTempVariable = 0
		while self._running:
			for i in range(50):
				MyTempVariable += gpio.input(13)
			MyGlobalVariable = MyTempVariable / 50
			time.sleep(0.5) #Wait for half a second between executions

NewThread = MyTimedThread()
NewThread = Thread(target=NewThread.run)
NewThread.start()

Exit = False
while Exit==False:
	print("Average Imput Value: ")
	print(MyGlobalVariable)
	time.sleep(1.27)
	if (counter > 100):
		Exit = True
	else:
		counter += 1

TwoSecond.terminate()
NewThread.terminate()

print("bai")
