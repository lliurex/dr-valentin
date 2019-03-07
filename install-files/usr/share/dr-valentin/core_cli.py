#!/usr/bin/env python2
import os

import os.path
import subprocess
import shutil
import sys
import tempfile
import tarfile
import time
import signal
import threading
import gettext
	

signal.signal(signal.SIGINT, signal.SIG_DFL)
_=gettext.gettext
gettext.textdomain('dr-valentin')

if os.path.exists("/srv/svn/pandora/dr-valentin/trunk/install-files/usr/share/dr-valentin/"):
	PACKAGE_PATH="/srv/svn/pandora/dr-valentin/trunk/install-files/usr/share/dr-valentin/"
else:
	PACKAGE_PATH="/usr/share/dr-valentin/"

import server
import client
import common

class Core_cli:
	
	def __init__(self,path=None):
		
		if path==None:
			self.path="/tmp/"
		else:
			self.path=path
			if self.path[len(self.path)-1]!="/":
				self.path=self.path+"/"
		
		self.lliurex_version=self.get_lliurex_version()

		
		if self.lliurex_version==None:
			print("Lliurex-version not found.")
			if gui:
				pass
			sys.exit(0)
			#self.lliurex_version=["client","13.02545"]

		
		self.temp_folder=tempfile.mkdtemp() + "/"
		self.lliurex_type=None
		
		
		if "server" in self.lliurex_version:
			self.check_root()
			self.lliurex_type="server"
			srv=server.Server(self)
			
		if "client" in self.lliurex_version:
			if self.lliurex_type==None:
				self.lliurex_type="client"
				cln=client.Client(self)
				
		if "desktop" in self.lliurex_version:
			if self.lliurex_type==None:
				self.lliurex_type="desktop"
		
		common.Common(self)
		
		self.compress_result()
			
	#def init
	
	def compress_result(self):
		
		file_name="drvalentin-"+self.lliurex_type+"_"+time.strftime("%d%m%Y",time.gmtime())+".tar.gz"
		
		print("\n[CORE] Creating tar.gz file...")
		
		tar=tarfile.open(self.path+file_name,"w:gz")
		
		os.chdir(self.temp_folder)
		
		for item in os.listdir("."):
			path=item
			#if os.path.isdir(path):
			print("\t* Adding " + path + " ...")
			tar.add(path)
				
		tar.close()
		print("\n[CORE] Diagnostic file " + self.path +file_name + " ready.\n")
		
		try:
			shutil.rmtree(self.temp_folder)
		except:
			pass
		
		return self.path + file_name
		
	#def compress_result
	
	def get_lliurex_version(self):
		
		try:
			p=subprocess.Popen(["lliurex-version"],stdout=subprocess.PIPE)
			output=p.communicate()[0]
			
			output=output.strip("\n").split(", ")
			return output
			
		except:
			return None

dr=Core_cli()
