import os
if os.name == "nt":
	import ctypes

def setBackground(path: str):
	if os.name == "nt":
		print("Untested on Windows")
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
		print("Not supported on Windows")
		raise NotImplementedError
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