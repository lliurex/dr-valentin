import os
import os.path
import subprocess
import shutil
import multiprocessing 
import glob
import time

if os.path.exists("/srv/svn/pandora/dr-valentin-client-common/trunk/install-files/usr/share/dr-valentin/client/actions/"):
	CLIENT_ACTIONS_PATH="/srv/svn/pandora/dr-valentin-client-common/trunk/install-files/usr/share/dr-valentin/client/actions/"
else:
	CLIENT_ACTIONS_PATH="/usr/share/dr-valentin/client/actions/"


class Client:
	
	def __init__(self,core):
		
		print("[CLIENT] Initializing server diagnostics...\n")
		
		self.core=core
		self.execute_actions()
		while self.process.is_alive():
			time.sleep(2)
		
	#def init
	
	def p_execute_actions(self):
		
		if os.path.exists(CLIENT_ACTIONS_PATH):
			for item in sorted(glob.glob(CLIENT_ACTIONS_PATH+"*")):
				exe=item + " " + self.core.temp_folder
				print("[CLIENT] Executing " + exe +  " ...")
				os.system(exe)
				
		
	#def p_execute_actions
	
	def execute_actions(self):
		
		self.process=multiprocessing.Process(target=self.p_execute_actions)
		#self.process.daemon=True
		self.process.start()
		
	#def execute_actions
	
	
	
#class Server