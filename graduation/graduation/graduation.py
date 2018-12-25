from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import requests
import sys, cv2, numpy, time
import os
import threading
from multiprocessing import Process

class Example(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = uic.loadUi("./G_form.ui",self) #경로 바꿀것
		#"/home/pi/PyQt/G_form.ui"
		self.setWindowTitle("Exam")
		self.initUi()

	def initUi(self):
		self.cpt = cv2.VideoCapture(0) #라즈베리파이는 -1
		self.fps = 24
	
		self.cnt = 0
		
		self.ui.camera.setScaledContents(True)
		self.ui.Picture_1.setScaledContents(True)

		self.ui.btn_on.clicked.connect(self.start)
		self.ui.btn_off.clicked.connect(self.stop)
		self.ui.btn_capture.clicked.connect(self.capture)
		self.ui.btn_send.clicked.connect(self.send)
		self.ui.btn_delete.clicked.connect(self.delete)
		self.ui.btn_close.clicked.connect(self.close)

		self.ui.show()

	def capture(self):
		_, cam = self.cpt.read()
		cv2.imwrite('img'+str(self.cnt)+'.jpg',cam)
		cam = cv2.cvtColor(cam,cv2.COLOR_BGR2RGB)
		img = QImage(cam,cam.shape[1],cam.shape[0],QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)

		self.ui.Picture_1.setPixmap(pix)
	
	def delete(self):
		self.ui.Picture_1.setText("bin")

	def close(self):
		sys.exit(0)

	def send(self):
		try:
			#proc = Process(target=self.sendimg,args=())
			#proc.start()
			#proc.join()
			my_t = threading.Thread(target=self.sendimg,args=())
			my_t.start()
		except Exception as e:
			print('Error :',e)

	def sendimg(self):
		try:
			requests.post("http://xn--c79as89achap9v.xn--3e0b707e:5000/sendimg",files={'img1':open(r'C:/Users/err20/Desktop/img0.jpg','rb')},timeout=50) # 50sec wait
			#r'C:/Users/err20/source/repos/graduation/graduation/img0.jpg','rb')
		except:
			QMessageBox.question(self,'Message',"error : Server down, Failed",QMessageBox.Yes)
		finally:
			self.ui.Picture_1.setText("bin")

	def start(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.start(1000. / self.fps)

	def nextFrameSlot(self):
		_, cam = self.cpt.read()
		cam = cv2.cvtColor(cam,cv2.COLOR_BGR2RGB)
		img = QImage(cam,cam.shape[1],cam.shape[0],QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.ui.camera.setPixmap(pix)

	def stop(self):
		self.ui.camera.setPixmap(QPixmap.fromImage(QImage()))
		self.timer.stop()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
