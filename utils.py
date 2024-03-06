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
				os.system(f"gsettings set org.cinnamon.desktop.background picture-uri 'file://{path}'")
			case "gnome":
				# untested
				os.system(f"gsettings set org.gnome.desktop.background picture-uri 'file://{path}'")
			case _:
				print("Not supported on this desktop environment.\nMe too lazy...")
				raise NotImplementedError
		#os.system(f"gsettings set org.cinnamon.desktop.background picture-uri 'file://{path.removeprefix('/')}'")

def getBackground():
	if os.name == "nt":
		print("Not supported on Windows")
		raise NotImplementedError
	else:
		return os.popen(f"gsettings get org.cinnamon.desktop.background picture-uri").read().split("'")[1]