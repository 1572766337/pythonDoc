#coding=utf8

import os
import sys
import pydoc
import tkFileDialog
import tkMessageBox
from Tkinter import *
from tkinter import ttk

class Application(Frame):

	def __init__(self, master):	# master=None
		Frame.__init__(self, master, bd=3)
		self.pack(fill='both', expand='yes')
		self.lstLib = []
		self.lstMethod = []
		# 初始化配置文件
		fini = open(os.path.dirname(sys.argv[0])+os.sep+'Py2LibPath.ini','a+')
		self.path = fini.read()
		if not self.path:
			self.path = tkFileDialog.askdirectory(title='请选择 Python Lib 文件夹')
			fini.write(self.path)
		fini.close()
		# 创建界面组件
		self.createWidgets()
		
	def createWidgets(self):
		# 左边布局
		self.labf_lib = LabelFrame(self, text='库')
		self.labf_lib.pack(side=LEFT, fill='both', expand='yes')

		frmLib = LabelFrame(self.labf_lib)
		frmLib0 = Frame(frmLib)
		frmLib00 = Frame(frmLib0)
		self.treeLib = ttk.Treeview(frmLib00)
		ysb = ttk.Scrollbar(frmLib, orient='vertical', command=self.treeLib.yview)
		xsb = ttk.Scrollbar(frmLib0, orient='horizontal', command=self.treeLib.xview)
		self.treeLib.configure(yscroll=ysb.set, xscroll=xsb.set)
		self.treeLib.heading('#0', text='Library', anchor='w')
		self.treeLib.bind("<<TreeviewSelect>>",self.importLibMethod) #事件(选中)绑定
		self.txtLibEntry = Entry(frmLib00, bd =2)
		self.txtLibEntry.bind('<Return>', self.filterLib)
		self.txtLibEntry.bind('<FocusIn>', self.filterLibClear)
		
		# 初始化左侧树
		self.getLibs()
		# 构建一个pack
		self.treeLib.pack(side=TOP, fill='both', expand='yes')
		ysb.pack(side=RIGHT, fill='y', expand='no')
		self.txtLibEntry.pack(side=BOTTOM, fill='x', expand='no')
		xsb.pack(side=BOTTOM, fill='x', expand='no')
		frmLib00.pack(fill='both', expand='yes')
		frmLib0.pack(fill='both', expand='yes')
		frmLib.pack(fill='both', expand='yes')
		
		
		# 中间布局
		self.labf_method = LabelFrame(self, text='函数')
		self.labf_method.pack(side=LEFT, fill='both', expand='yes')

		frmMethod = LabelFrame(self.labf_method)
		frmMethod0 = Frame(frmMethod)
		frmMethod00 = Frame(frmMethod0)
		self.treeMethod = ttk.Treeview(frmMethod00)
		ysb = ttk.Scrollbar(frmMethod, orient='vertical', command=self.treeMethod.yview)
		xsb = ttk.Scrollbar(frmMethod0, orient='horizontal', command=self.treeMethod.xview)
		self.treeMethod.configure(yscroll=ysb.set, xscroll=xsb.set)
		self.treeMethod.heading('#0', text='Method', anchor='w')
		self.treeMethod.bind("<<TreeviewSelect>>",self.showMethodInfo) #事件(选中)绑定
		self.txtMethodEntry = Entry(frmMethod00, bd =2)
		self.txtMethodEntry.bind('<Return>', self.filterMethod)
		self.txtMethodEntry.bind('<FocusIn>', self.filterMethodClear)
		
		# self.root_method = self.treeMethod.insert('', 'end', text=abspath, open=True)
		# self.getMethods(self.root_method, abspath)
		# 构建一个pack
		self.treeMethod.pack(side=TOP, fill='both', expand='yes')
		ysb.pack(side=RIGHT, fill='y', expand='no')
		self.txtMethodEntry.pack(side=BOTTOM, fill='x', expand='no')
		xsb.pack(side=BOTTOM, fill='x', expand='no')
		frmMethod00.pack(fill='both', expand='yes')
		frmMethod0.pack(fill='both', expand='yes')
		frmMethod.pack(fill='both', expand='yes')

		
		# 右边布局
		self.labf_content = LabelFrame(self, text='帮助')
		self.labf_content.pack(side = LEFT, fill='both', expand='yes')

		scrollbar = Scrollbar(self.labf_content)
		scrollbar.pack( side = RIGHT, fill=Y )
		
		self.text = Text(self.labf_content, yscrollcommand=scrollbar.set)
		self.text.pack(fill='both', expand='yes')
		scrollbar.config(command = self.text.yview )

	def initLibs(self):
		self.lstLib = ['__builtins__']
		for root,dirs,files in os.walk(self.path):
			for file in files:
				abspath = root + os.sep + file
				if 'test' in abspath.lower():
					continue
				if not file.endswith('.py'):
					continue
				abspath = abspath.replace('.py','')
				if os.path.dirname(abspath) == self.path:
					text = os.path.relpath(abspath, self.path)
					self.lstLib.append(text)
					# self.treeLib.insert(parent, 'end', text=text, open=False)
				elif 'lib-tk' in abspath:
					text = os.path.relpath(abspath, self.path).replace('lib-tk\\','')
					self.lstLib.append(text)
				# elif 'site-packages' in abspath:
				elif file.endswith('__init__.py'):
					text = os.path.relpath(abspath, self.path).replace('\\__init__','').replace('site-packages\\','').replace('\\','.')
					self.lstLib.append(text)
					# self.treeLib.insert(parent, 'end', text=text, open=False)
				
					
	def getLibs(self):
		if len(self.lstLib) == 0:
			self.initLibs()
		for item in self.treeLib.get_children():
			self.treeLib.delete(item)
		self.root_lib = self.treeLib.insert('', 'end', text=self.path, open=True)
		filterLib = self.txtLibEntry.get()
		if filterLib != '':
			for lib in self.lstLib:
				if filterLib.lower() in lib.lower():
					self.treeLib.insert(self.root_lib, 'end', text=lib, open=False)
		else:
			for lib in self.lstLib:
				self.treeLib.insert(self.root_lib, 'end', text=lib, open=False)
		
	def showMethodInfo(self,event):
		self.select=event.widget.selection() #获取所选的项(可能是多项，所以要for循环)  
		for idx in self.select:
			# print self.treeMethod.item(idx)
			method = ''
			try:
				lib = self.treeMethod.item(idx)["values"][0]
				method = lib + '.' +self.treeMethod.item(idx)["text"]
			except:
				method = self.treeMethod.item(idx)["text"]
			if method.startswith('__builtins__'):
				method = method[13::]
			try:
				# 必须编码，不然是unicode编码，只能显示unicode类
				exec 'methodInfo = pydoc.render_doc("%s")'%method
				methodInfo = re.sub('\x08.','',methodInfo)
				self.text.delete(0.0,END)
				self.text.insert(1.0,methodInfo)
			except ImportError:
				self.text.delete(0.0,END)
				self.text.insert(1.0,'no Python documentation found for %s'%method)
	
	def filterLib(self, event):
		self.getLibs()
		
	def filterLibClear(self, event):
		self.txtLibEntry.delete(0, END)
	
	def filterMethod(self, event):
		self.createMethodTree(self.mn)
		
	def filterMethodClear(self, event):
		self.txtMethodEntry.delete(0, END)
	
	def createMethodTree(self, mn):
		if len(self.lstMethod) == 0:
			return
		for item in self.treeMethod.get_children():
			self.treeMethod.delete(item)
		parent = self.treeMethod.insert('', 'end', text=self.mn, open=True)
		filterMethodTxt = self.txtMethodEntry.get()
		if filterMethodTxt != '':
			for method in self.lstMethod:
				if filterMethodTxt.lower() in method.lower():
					self.treeMethod.insert(parent, 'end', text=method, value=(mn), open=False)
		else:
			for method in self.lstMethod:
				self.treeMethod.insert(parent, 'end', text=method, value=(mn), open=False)
				
	def importLibMethod(self,event):  
		self.select=event.widget.selection() #获取所选的项(可能是多项，所以要for循环)  
		for idx  in self.select:
			try:
				self.mn = self.treeLib.item(idx)["text"]
				if '.' in self.mn:
					exec 'from %s import *'%self.mn
					methods = dir()
				elif '__builtins__' == self.mn:
					methods = dir(__builtins__)
				else:
					exec 'import %s'%self.mn
					exec 'methods = dir(%s)'%self.mn
				
				# 初始变量
				self.lstMethod = []
				for method in methods:
					self.lstMethod.append(method)
				self.createMethodTree(self.mn)
			except ImportError:
				self.text.delete(0.0,END)
				self.text.insert(1.0,'No module named %s'%self.mn)
				
	

root = Tk()
root.title('PythonDoc2.7 By:星晨之域 QQ:1572766337')
root.geometry('1100x600+100+50')
app = Application(master=root)
app.mainloop()
# root.destroy()
