import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import youtube_subs
import urllib
import subprocess
import pafy
from threading import Thread
import time
from cStringIO import StringIO
import sys
import os
import datetime
import random

class GUI():
	def __init__(self,url_list,show_old):
		self.app = QApplication(sys.argv)
		self.widget = QWidget()
		self.widget.resize(650,800)
		self.widget.setWindowTitle("Selection")
		self.widget.show()
		
		layout = QVBoxLayout()
		self.widget.cb = QListWidget()
		self.widget.cb.setStyleSheet("QListWidget::item:focus{border:none;outline:none;}")
		self.widget.cb.setStyleSheet("QListWidget::item {border-style:outset;border-width: 2px;border-color: grey;}")
		
		
		self.myWidgetList = []
		
		for i in range(len(url_list)):
			print(i)
			try:
				video = pafy.new(url_list[i])
				month_out = int(video.published[5:7])
				now = datetime.datetime.now()
				if(show_old or now.month - month_out <= 2):
					myQWidget = WidgetVideo(url_list[i],video.length)
					self.myWidgetList.append(myQWidget)
					myQListWidgetItem = QListWidgetItem(self.widget.cb)
					myQListWidgetItem.setSizeHint(myQWidget.sizeHint())
					self.widget.cb.addItem(myQListWidgetItem)
					self.widget.cb.setItemWidget(myQListWidgetItem, myQWidget)
			except:
				print("Il y a eu une erreur, la video n'existe pas")
		layout.addWidget(self.widget.cb)
		
		Hlayout = QHBoxLayout()
		okButton = QPushButton("OK")
		cancelButton = QPushButton("CANCEL")
		selectAllButton = QPushButton("SELECT ALL")
		deselectAllButton = QPushButton("DESELECT ALL")
		Hlayout.addWidget(okButton)
		Hlayout.addWidget(cancelButton)
		Hlayout.addWidget(selectAllButton)
		Hlayout.addWidget(deselectAllButton)
		layout.addLayout(Hlayout)
		
		self.widget.setLayout(layout)
		
		okButton.clicked.connect(self.ok)
		cancelButton.clicked.connect(self.cancel)
		selectAllButton.clicked.connect(self.select_all)
		deselectAllButton.clicked.connect(self.deselect_all)
		
		self.widget.cb.sortItems()
		
		sys.exit(self.app.exec_())
		
	def select_all(self):
		for i in range(len(self.myWidgetList)):
			self.myWidgetList[i].check.setChecked(True)
	
	def deselect_all(self):
		for i in range(len(self.myWidgetList)):
			self.myWidgetList[i].check.setChecked(False)
	
	def cancel(self):
		sys.exit()
		
	def clearLayout(self,layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				self.clearLayout(child.layout())

	def ok(self):
		newfont = QFont("Times",22,QFont.Bold)
		to_dl_list = []
		ost = sys.stdout
		for i in range(len(self.myWidgetList)):
			if self.myWidgetList[i].check.isChecked():
				to_dl_list.append(self.myWidgetList[i].url)
		print(to_dl_list)
		for i in reversed(range(self.widget.layout().count())): 
			self.clearLayout(self.widget.layout())
		self.progress_single = QProgressBar()
		self.progress_group = QProgressBar()
		self.progress_single.setValue(100)
		self.progress_group.setValue(100)
		

		self.quitButton = QPushButton("Quit")
		self.quitButton.clicked.connect(self.exit_app)
		self.quitButton.setEnabled(False)
		
		self.name_label = QLabel("")
		self.name_label.setFont(newfont)
		self.video_total_label = QLabel("")
		self.video_total_label.setFont(newfont)
		self.temps_restant_label = QLabel("")
		self.temps_restant_label.setFont(newfont)
		self.length_label = QLabel("")
		self.length_label.setFont(newfont)
		
		self.widget.layout().addWidget(self.name_label)
		self.widget.layout().addWidget(self.length_label)
		self.widget.layout().addWidget(self.progress_single)
		self.widget.layout().addWidget(self.temps_restant_label)
		self.widget.layout().addWidget(self.progress_group)
		self.widget.layout().addWidget(self.video_total_label)
		self.widget.layout().addWidget(self.quitButton)
		
		self.thread_dl = Downloader(to_dl_list)
		self.thread_dl.start()
		
		
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_percent)#self.thread_dl.join()
		self.timer.start(500)
		
	def exit_app(self):
		sys.exit()

	def update_percent(self):
		try:
			self.name_label.setText(self.thread_dl.name)
			self.length_label.setText(str(datetime.timedelta(seconds=self.thread_dl.length)))
			percent_now = int((os.path.getsize("Dled/"+str(self.thread_dl.name)+".mp4.temp")/float(self.thread_dl.size))*100)
			time_spent = round(time.time()-self.thread_dl.begin_time,0)
			percent_left = 100-percent_now
			time_left_estimated = time_spent/percent_now
			time_left_estimated = int(time_left_estimated*percent_left)

			self.video_total_label.setText("Video "+str(self.thread_dl.url_nbr+1)+"/"+str(self.thread_dl.video_total))
			self.temps_restant_label.setText("Temps restant: Environ "+str(time_left_estimated)+" s")
			self.progress_single.setValue(percent_now)
			
			self.progress_group.setValue((self.thread_dl.url_nbr)/float(self.thread_dl.video_total)*100)
		except:
			self.progress_single.setValue(100)
			if(self.thread_dl.done):
				self.progress_group.setValue(100)
				self.quitButton.setEnabled(True)

		if(self.thread_dl.done):
			self.timer.stop()
			self.clean_filename()
			print()
			print("Telechargement termine")
	
	def clean_filename(self):
		file_list = os.listdir("/home/nemael/Desktop/Programmes/YoutubeDownloader/Dled/")
		safe_char_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','-','(',')','[',']','+',' ','.','1','2','3','4','5','6','7','8','9','0']
		for fil in range(len(file_list)):
			name = file_list[fil]
			i = 0
			while i < len(name):
				if name[i] in safe_char_list:
					i += 1
				else:
					name = name[:i] + name[i+1:]
			if name == ".mp4":
				name = str(random.randint(1,10000))
				name += ".mp4"
			os.rename("/home/nemael/Desktop/Programmes/YoutubeDownloader/Dled/"+file_list[fil],"/home/nemael/Desktop/Programmes/YoutubeDownloader/Dled/"+name)
				

class WidgetVideo(QWidget):
	def __init__(self, video_id, length, parent=None):
		QWidget.__init__(self, parent=parent)
		
		res_list = youtube_subs.get_videos_infos(video_id)
		print(res_list[0],res_list[3])
		Hlay = QHBoxLayout(self)
		self.url = "https://www.youtube.com/watch?v="+video_id
		self.check = QCheckBox()
		self.check.setStyleSheet("QCheckBox::indicator { width: 70; height: 110;}")
		Hlay.addWidget(self.check)
		
		Vlay = QVBoxLayout()
		name = res_list[0]
		if len(name) > 65:
			name = name[:65] +"..."
		Vlay.addWidget(QLabel(name))
		Vlay.addWidget(QLabel(res_list[3]))
		Vlay.addWidget(QLabel(str(datetime.timedelta(seconds=length))))
		
		
		HlayIntern = QHBoxLayout()
		data = urllib.urlopen(res_list[1]).read()
		image = QImage()
		image.loadFromData(data)
		lbl = QLabel(self)
		lbl.setPixmap(QPixmap(image))
		HlayIntern.addWidget(lbl)
		
		date = res_list[2]
		date = date[:10]+"\n"+date[11:19]
		HlayIntern.addWidget(QLabel(date))
		Vlay.addLayout(HlayIntern)
		
		Hlay.addLayout(Vlay)
		horizontalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
		Hlay.addItem(horizontalSpacer)
		

class Downloader(Thread):
	def __init__(self,url_list):
		Thread.__init__(self)
		
		self.url_list = url_list
		self.video_total = len(url_list)
		self.url_nbr = 0
		self.url = url_list[0]
		self.size = 0
		self.name = ""
		self.begin_time = 0
		self.length = 0
		self.done = False
		
		
		
	def run(self):
		
		for i in range(len(self.url_list)):
			try:				
				self.url_nbr = i
				video = pafy.new(self.url_list[i])
				best = video.getbest(preftype="mp4")
				self.length = video.length
				self.size = best.get_filesize()
				self.name = video.title
				self.begin_time = time.time()
				
				best.download(filepath = "Dled/",quiet=False)
			except UnicodeEncodeError:
				print("Erreur d'encodage sur la video",i)
				video = pafy.new(self.url_list[i])
				try:
					print(video.title)
				except:
					print("Ne peut meme pas print le nom de la video")
				best = video.getbest(preftype="mp4")
				best.download(filepath = "Dled/",quiet=False)
		self.done = True