# import os
# import time
# import win32print
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic


#----------------------------------------------------------------------
# def print_job_checker():
#     """
#     Prints out all jobs in the print queue every 1 seconds
# 	https://pythonq.com/so/python/1857010 참조
#     """
#     jobs = [1]
#     while jobs:				#프린트 스풀링 중에 반복문 작동
#         jobs = []
#         for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None, 1):
#             flags, desc, name, comment = p

#             phandle = win32print.OpenPrinter(name)
#             print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
#             if print_jobs:
#                 jobs.extend(list(print_jobs))
#             win32print.ClosePrinter(phandle)

#         time.sleep(1)

#     print( "프린트 작업 목록 비어있음")

# def set_defaultPrinter():
# 	printer_name = win32print.GetDefaultPrinter()
# 	printTuple=win32print.EnumPrinterDrivers()
# 	printList=list()

# 	n=1
# 	print("기본 프린트를 선택 하세요")
# 	for i in printTuple:
# 		printList.append([n,i['Name']])
# 		print(n," : ",i['Name'])
# # 		n=n+1
# #----------------------------------------------------------------------


# #----------------------------------------------------------------------


# set_defaultPrinter()

# print ("*******폴더 간편 출력 프로그램******** \n")
# print("출력물 위치 : 1.바탕화면 2.그외 ")
# menu=input()
# folder_name=" "


# if menu =='1':
# 	print("--바탕화면의 폴더명을 입력하시오\n")
# 	strin=input()
# 	folder_name="C:/Users/KT/Desktop/"+strin
# else:
# 	print("--출력할 폴더 디렉토리를 입력하시오\n")
# 	print("예시)C:/Users/KT/Desktop/RFP \n")
# 	folder_name=input()

# i=1
# try:
# 	file_list=os.listdir(folder_name)

# 	if len(file_list)>0 :

# 		for file_name in file_list:
# 			print(i,"/",len(file_list),file_name+"를 출력합니다.\n")
# 			os.startfile(folder_name + "\\"+ file_name, "print")
# 			print_job_checker()

# 			time.sleep(int(10))

# 	else : print("폴더가 비어있습니다.")

# except :
#  	print("경로가 정확하지 않습니다.")

# exe 만들기 :
# pip install pyinstaller 하고
# 커멘드에서 py위치 있는곳으로 이동하고
# pyinstaller --onefile xxxx.py 입력


#___________________________________________________________________________



import sys
import os
import time
#import win32print

#pip install pyqt5 이후 사용
from PyQt5.QtCore import QTranslator,Qt,QEvent,QLocale,QEventLoop
from PyQt5.QtWidgets import QWidget,QApplication,QLabel, QComboBox,QBoxLayout,QPushButton, QTextBrowser,QFileDialog
from PyQt5 import QtTest
import tkinter
from tkinter import filedialog




class printer:
	default_printer_name='디폴트'
	printerlist=['']
	filelist=['']
	dirPath='./'
	
	def printing(filename):
		
			# for file_name in filelist:
			# 	#print(i,"/",len(filelist),file_name+"를 출력합니다.\n")
			# 	os.startfile(folder_name + "\\"+ file_name, "print")
			# 	print_job_checker()	#비어있을때까지 대기
			# 	time.sleep(int(10))	#10초 대기
		
		print(filename+'을 출력합니다.')

	
	def getPath(self,path):
		self.filelist = os.listdir(path)
		
	def getPrinterList(self):
		#프린터 리스트 받아오기
		self.printerlist=['1','2','3','4']

		#맥북이여서 뺌
		#default_printer_name = win32print.GetDefaultPrinter()
		#printerlist=win32print.EnumPrinterDrivers()
		

	def print_job_checker():
		"""
		Prints out all jobs in the print queue every 1 seconds
		https://pythonq.com/so/python/1857010 참조
		"""
		jobs = [1]
		while jobs:				#프린트 스풀링 중에 반복문 작동
			jobs = []
			for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None, 1):
				flags, desc, name, comment = p

				phandle = win32print.OpenPrinter(name)
				print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
				if print_jobs:
					jobs.extend(list(print_jobs))
				win32print.ClosePrinter(phandle)

			QtTest.QTest.qWait(1000)


		print( "프린트 작업 목록 비어있음")


class Form(QWidget,printer):
	
	def __init__(self):
		QWidget.__init__(self, flags=Qt.Window)

		
		self.setMinimumWidth(500)
		self.setMinimumHeight(500)
		self.setWindowTitle("프린터 간편 출력 프로그램")
		self.lb = QLabel("폴더 내 파일을 순차적으로 출력합니다.",self)
		self.lb2 = QLabel("출력 프린터 선택",self)
		self.lb3 = QLabel("파일 목록",self)

		#푸쉬버튼 초기 세팅
		self.pb1=QPushButton("출력",self)
		self.pb2=QPushButton("정지",self)
		self.pb3=QPushButton("디렉터리찾기",self)
		self.pb1.clicked.connect(self.pb1_printing)
		self.pb2.clicked.connect(self.pb2_stop)
		self.pb3.clicked.connect(self.pb3_getdir)
		
		#텍스트 박스 초기 셋팅
		self.tb=QTextBrowser(self)

		#콤보박스 초기 셋팅
		self.qb = QComboBox(self)
		printer.getPrinterList(printer)
		self.qb.addItems(i for i in printer.printerlist) #콤보박스 내용 삽입
		self.qb.currentIndexChanged.connect(self.change_printer)  # 콤보박스의 선택된 내용이 바뀌면 시그널
		
		QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
		
		#위치 세팅
		self.init_widget()
	
	def pb1_printing(self):
		#프린트 시작
		for index in range(0,len(printer.filelist)):
			#파일 하나씩 출력 명령 후 텍스트박스 업데이트
			printer.printing(printer.filelist[index])
			printer.filelist[index]='출력완료'
			self.setfileList()
			QtTest.QTest.qWait(2000)


	def pb2_stop(self):
		########코드 짜야함
		print("정지")

	def pb3_getdir(self):
		#파일 위치 수집
		#fname = QFileDialog.getOpenFileNames(self)#파일들 선택
		fname= QFileDialog.getExistingDirectory(self) #폴더 선택
		printer.getPath(printer,fname)
		self.setfileList()

	def change_printer(self):
		#디폴트 프린터 변경
		printer.default_printer_name=self.qb.currentText()
		print(self.qb.currentText())


	def setfileList(self):
		#파일 리스트 박스에 출력
		#text box에 파일 리스트 출력
		self.tb.setPlainText('')
		
		for i in range(0,len(printer.filelist)):
			self.tb.append(str(i)+'.     '+printer.filelist[i])
			

	def init_widget(self):
		#setGeometry (x,y,너비,높이)
		self.lb.setGeometry(200,30,300,20)
		self.lb2.setGeometry(55,60,300,20)
		self.lb3.setGeometry(55,130,300,20)
		self.pb1.setGeometry(600,30,100,50)
		self.pb2.setGeometry(600,90,100,50)
		self.pb3.setGeometry(600,150,100,50)
		self.qb.setGeometry(45,20,500,150)
		self.tb.setGeometry(50,155,500,500)
		self.tb.setPlainText('  폴더를 선택해주세요.')
	

if __name__ == "__main__":

	app = QApplication(sys.argv)
	form = Form()
	form.show()

	exit(app.exec_())