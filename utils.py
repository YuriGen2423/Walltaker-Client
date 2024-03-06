import os
if os.name == "nt":
	import ctypes

def setBackground(path: str):
	if os.name == "nt":
		print("Untested on Windows")
		ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
	else:
		if os.getenv("DESKTOP_SESSION") != "cinnamon":
			print("Not supported on this desktop environment.\nMe too lazy...")
			raise NotImplementedError
		os.system(f"gsettings set org.cinnamon.desktop.background picture-uri 'file://{path}'")
		#os.system(f"gsettings set org.cinnamon.desktop.background picture-uri 'file://{path.removeprefix('/')}'")

def getBackground():
	if os.name == "nt":
		print("Not supported on Windows")
		raise NotImplementedError
	else:
		return os.popen(f"gsettings get org.cinnamon.desktop.background picture-uri").read().split("'")[1]