import os
if os.name == "nt":
	import ctypes
	import winreg
	import win10toast

def setBackground(path: str):
	if os.name == "nt":
		path = path.replace("/","\\")
		print("setting to", path)
		ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
	else:
		match os.getenv("DESKTOP_SESSION"):
			case "cinnamon":
				# Mon cher cinnamon
				os.system(f"gsettings set org.cinnamon.desktop.background picture-uri 'file://{path}'")
			case "gnome":
				print("Untested on Gnome")
				os.system(f"gsettings set org.gnome.desktop.background picture-uri 'file://{path}'")
			case _:
				print("Not supported on this desktop environment.")
				raise NotImplementedError

def getBackground():
	if os.name == "nt":
		# Open the registry key
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
		# Query for the Wallpaper value
		wallpaper_path, _ = winreg.QueryValueEx(key, "WallPaper")
		return wallpaper_path
	else:
		match os.getenv("DESKTOP_SESSION"):
			case "cinnamon":
				return os.popen(f"gsettings get org.cinnamon.desktop.background picture-uri").read().split("'")[1]
			case "gnome":
				print("Untested on Gnome")
				return os.popen(f"gsettings get org.gnome.desktop.background picture-uri").read().split("'")[1]
			case _:
				print("Not supported on this desktop environment.")
				raise NotImplementedError
			
def toast(title: str, message: str, icon = None, duration = 5, threaded = True):
		if os.name == "nt":
			toaster = win10toast.ToastNotifier()
			toaster.show_toast(title,message,icon,duration,threaded)
		else:
			if threaded == False:
				print("Not suported on linux yet")
			os.system(f"notify-send -u 'normal' 'Walltaker' 'New wallpaper by {link['set_by']}'")