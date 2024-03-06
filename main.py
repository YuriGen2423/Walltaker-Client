import sys
import os
if os.path.exists("requirements.txt"):
	os.system("pip install -r requirements.txt")
	os.remove("requirements.txt")

import tkinter as tk
import requests
import utils

try:
	os.mkdir("walltaker")
except FileExistsError:
	pass

try:
	requests.get("https://walltaker.joi.how/")
except ConnectionError as e:
	win = tk.Tk()
	win.title("Error")
	label = tk.Label(win, text="Connection error")
	statusL = tk.Label(win, text=e)
	win.mainloop()
	quit(0)

win = tk.Tk()
win.title("Walltaker YClient")

interval	= 60
linkID		= 14532
if os.path.exists("sav"):
	with open("sav", "rb") as file:
		interval = int.from_bytes(file.read(4), sys.byteorder)
		linkID = int.from_bytes(file.read(4), sys.byteorder)
prevcall = 0
def new_wallpaper():
	global prevcall, currentwallpaper

	link = requests.get(f"https://walltaker.joi.how/links/{linkID}.json").json()
	post = link["post_url"]
	filename = post.split("/")[-1]

	if os.path.exists(f"walltaker/{filename}"):
		print(f"{filename} already exists")
	else:
		with open(f"walltaker/{filename}", "wb") as file:
			file.write(requests.get(post).content)

	utils.setBackground(f"{os.path.join(os.path.dirname(__file__),f'walltaker/{filename}')}")
	print(utils.getBackground())

def update(newInterval, newLinkID):
	global interval
	try:
		interval = int(newInterval)
		linkID = int(newLinkID)
		new_wallpaper()
	except ValueError:
		warningWin = tk.Tk()
		warningWin.title("Error")

		warningL	= tk.Label(warningWin, text="Invalid\nMust be integer")
		okB 		= tk.Button(warningWin, text="Ok", command=warningWin.destroy)

		warningL.pack()
		okB.pack()

		warningWin.mainloop()

intervalI	= tk.Entry(win, width=5, justify="center")
linkIDI		= tk.Entry(win, width=6, justify="center")
updateB		= tk.Button(win, text="Update", command=lambda: update(intervalI.get(), linkIDI.get()))
quitB		= tk.Button(win, text="Quit", command=win.destroy)

intervalI.insert(0, interval)
linkIDI.insert(0, linkID)

intervalI.grid(row=0, column=0)
linkIDI.grid(row=0, column=1)
updateB.grid(row=1, column=0)
quitB.grid(row=1, column=1)

win.after(1_000, new_wallpaper)
win.mainloop()

with(open("sav","wb")) as file:
	interval = bytes(int.to_bytes(interval, 4, sys.byteorder))
	linkID = bytes(int.to_bytes(linkID, 4, sys.byteorder))
	file.write(interval+linkID)

print("Exiting")
exit(0)