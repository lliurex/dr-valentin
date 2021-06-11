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
import gi
try:
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk,Gdk,GObject,GLib
except:
	pass
	

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

class Core:
	
	def __init__(self,gui=False,path=None):
		
		self.gui=gui
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
		
		
		for item in self.lliurex_version:
			if "server" in item:
				#self.check_root()
				self.lliurex_type="server"
				self.clss=server.Server
				break
				
			if "client" in item:
				if self.lliurex_type==None:
					self.lliurex_type="client"
					self.clss=client.Client
					break
					
			if "desktop" in item:
				if self.lliurex_type==None:
					self.lliurex_type="desktop"
		
		self.start_gui()
			
				
			
			#self.compress_result()
		
	#def init
	
	def close_window(self,window):
		
		Gtk.main_quit()
		
	#def close_window
	
	def start_gui(self):
		
		builder=Gtk.Builder()
		builder.set_translation_domain("dr-valentin")
		builder.add_from_file(PACKAGE_PATH+"rsrc/drvalentin.glade")
		self.window=builder.get_object("window1")
		self.window.connect("destroy",self.close_window)
		self.spinner=builder.get_object("spinner")
		self.execute_button=builder.get_object("execute_button")
		#self.execute_button.set_name("PILL")
		self.execute_button.connect("clicked",self.execute_clicked)
		self.lliurex_version_label=builder.get_object("lliurex_version_label")
		self.lliurex_version_label.set_markup("<b>"+",".join(self.lliurex_version)+"</b>")
		self.folder_chooser=builder.get_object("folderchooserbutton")
		path=self.check_user_desktop()
		self.folder_chooser.set_current_folder(path)
		self.info_box=builder.get_object("info_box")
		self.info_box.set_name("info_box")
		self.msg_label=builder.get_object("msg_label")
		self.msg_label.set_name("info_box")
		self.window.set_name("Window2")
		self.window.show()
		self.set_css_info()
		#self.window.set_decorated(False)
		GObject.threads_init()
		Gtk.main()
		
	#def start_gui
	
	def execute_clicked(self,widget):
		
		self.spinner.show()
		self.execute_button.set_sensitive(False)
		self.thread=threading.Thread(target=self.m_execute)
		self.thread.daemon=True
		self.thread.start()
		
		GLib.timeout_add(1000,self.check_thread)
		
	#def execute_clicked
	
	def check_user_desktop(self):
		
		path=os.path.expanduser("~/")
		
		try:
		
			f=open(os.path.expanduser("~/.config/user-dirs.dirs"))
			lines=f.readlines()
			f.close()
			
			for item in lines:
				if "XDG_DESKTOP_DIR" in item:
					first=item.find("/")+1
					last=item.rfind('"')
					path=path + item[first:last].strip("\n")
					
					
		except Exception as e:
			print(e,"!!!")
			
			
		return path

	
	def check_thread(self):
		
		if not self.thread.is_alive():
			
			self.spinner.hide()
			self.execute_button.set_sensitive(True)
			return False
			
		return True
	
	def m_execute(self):
		
		'''
		obj=self.clss(self)
		file_name=self.compress_result()
		file_name,self.folder_chooser.get_current_folder()
		shutil.copy(file_name,self.folder_chooser.get_current_folder())
		msg=_("Diagnostic file '%s' ready!")%file_name.strip("/tmp/")
		def_msg="<b>"+msg+"</b>"
		self.msg_label.set_markup(def_msg)
		os.system("xdg-open " + self.folder_chooser.get_current_folder() )
		'''
		cmd="/usr/share/dr-valentin/core_cli.py " + self.folder_chooser.get_filename()
#		if self.lliurex_type=="server":
#			cmd="gksu " + cmd
		cmd="pkexec " + cmd
			
		os.system(cmd)
		os.system("xdg-open " + self.folder_chooser.get_filename() )
		
		
	#def m_execute
	
	def set_css_info(self):
		
		css = b"""
		#ButtonBox {
			background-image: -gtk-gradient (linear,	left top, right top, from (rgba(255,255,255,0.6)),  to (rgba(210,210,210,0)));
		}
		
		#Window2 {
			background-image: -gtk-gradient (linear,	left top, left bottom, from (#fff),  to (#e0e0e0));
		}
		
		#PILL {
			background-image: -gtk-gradient (linear,	left top, right top, color-stop(0.5,#2a48ff), color-stop(0.5,#de0000));
			color: blue;
			padding: 2px 7px;
			border-color:#000;
		}
		#PILL:hover {
			background-image: -gtk-gradient (linear,	left top, right top, color-stop(0.5,#de0000), color-stop(0.5,#2a48ff));
			color: blue;
			padding: 2px 7px;
			border-color:#000;
			transition: 1000ms ease-in-out;
		}
		
		#info_box{
			background-image: -gtk-gradient (linear,	left top, left bottom, from (#e0e0e0),  to (#fff));
			background-color: white;
			border-color:#000;
		}
		
		#Custom{
			border-radius: 50px;
		}
		
		GtkSeparator{
			border-color:black;
		}
		
		GtkFrame{
		
			
			border-color: blue;
			
		}
		
		
		GtkButton {
		
			border-radius:50px;
		}
		
		#Button{
			background-image: -gtk-gradient (linear,	left top, left bottom, from (#f5f5f5),  to (#dedede));
			
			border-radius: 0px;
			
		}
		
		.entry{
			border-radius: 50px;
		}
		
		GtkViewport{
			
			background-image: -gtk-gradient (linear,	left top, left bottom, from (rgba(255,255,255,1)),  to (rgba(210,210,210,1)));
		}


		"""
		
		self.style_provider=Gtk.CssProvider()
		self.style_provider.load_from_data(css)
		
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
				
		
	#def set_css_info
	
	def get_lliurex_version(self):
		
		try:
			p=subprocess.Popen(["lliurex-version"],stdout=subprocess.PIPE)
			output=p.communicate()[0]

			if type(output) is bytes:
				output=output.decode()
			
			output=output.strip("\n").split(", ")
			return output
			
		except:
			return None
			
	def check_root(self):
		
		try:
			f=open("/run/dr-valentin","w")
			f.close()
		except:
			print("[!] You need root privileges [!]")
			if self.gui:
				d=Gtk.Dialog("Dr Valentin", None, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
				d.set_default_size(150,100)
				hbox=Gtk.HBox()
				image=Gtk.Image()
				image.set_from_stock(Gtk.STOCK_DIALOG_WARNING,Gtk.IconSize.DIALOG)
				hbox.pack_start(image,True,True,5)
				label=Gtk.Label("")
				label.set_markup("<b>" + _("You need root privileges") + "</b>")
				hbox.pack_start(label,True,True,5)
				box=d.get_content_area()
				box.add(hbox)
				d.show_all()
				r=d.run()
			sys.exit(0)
			
	#def check_root
			
#class Core

def usage():
	
	print("USAGE:")
	print("\tdr-valentin-cli [DIAGNOSTIC-DESTINATION-FOLDER]")
	print("\t\tBy default, destination folder is /tmp/")
	print("\tdr-valentin")


if __name__=="__main__":
	try:
		if len(sys.argv)>1:
			if sys.argv[1]=="cli":
				try:
					if os.path.exists(sys.argv[2]):
						c=Core(False,sys.argv[2])
					else:
						c=Core()
				except:
					c=Core()
			elif sys.argv[1]=="gui":
				c=Core(True)
			else:
				usage()
				sys.exit(0)
				
		else:
			c=Core()
	except Exception as e:
		print(e)
		pass

