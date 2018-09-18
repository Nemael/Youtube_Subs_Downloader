import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import youtube_subs
import urllib



def start(url_list):
	app = QApplication(sys.argv)
	widget = QWidget()
	widget.resize(650,800)
	widget.setWindowTitle("Selection")
	widget.show()
	
	layout = QVBoxLayout()
	widget.cb = QListWidget()
	#widget.cb.setFocusPolicy(Qt.NoFocus)
	#widget.cb.setStyleSheet("QListWidget {border-style:outset;border-width:10px;border-color:black;}")
	widget.cb.setStyleSheet("QListWidget::item:focus{border:none;outline:none;}")
	widget.cb.setStyleSheet("QListWidget::item {border-style:outset;border-width: 2px;border-color: grey;}")
	
	
	myWidgetList = []
	
	for i in range(len(url_list)):
		myQWidget = WidgetVideo(url_list[i])
		myWidgetList.append(myQWidget)
		myQListWidgetItem = QListWidgetItem(widget.cb)
		myQListWidgetItem.setSizeHint(myQWidget.sizeHint())
		widget.cb.addItem(myQListWidgetItem)
		widget.cb.setItemWidget(myQListWidgetItem, myQWidget)
	
	
	layout.addWidget(widget.cb)
	
	Hlayout = QHBoxLayout()
	okButton = QPushButton("OK")
	cancelButton = QPushButton("CANCEL")
	Hlayout.addWidget(okButton)
	Hlayout.addWidget(cancelButton)
	layout.addLayout(Hlayout)
	
	widget.setLayout(layout)
	
	okButton.clicked.connect(lambda: ok(myWidgetList))
	cancelButton.clicked.connect(cancel)
	
	sys.exit(app.exec_())
	

def cancel():
	sys.exit()

def ok(myWidgetList):
	to_dl_list = []
	for i in range(len(myWidgetList)):
		if myWidgetList[i].check.isChecked():
			to_dl_list.append(myWidgetList[i].url)
	print(to_dl_list)

	

class WidgetVideo(QWidget):
	def __init__(self, video_id, parent=None):
		QWidget.__init__(self, parent=parent)
		
		res_list = youtube_subs.get_videos_infos(video_id)
		print(res_list)
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
		Vlay.addWidget(QLabel(res_list[3]))
		
		Hlay.addLayout(Vlay)
		horizontalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
		Hlay.addItem(horizontalSpacer)