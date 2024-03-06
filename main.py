import sys
import os

CONFIGFILE = "config.toml"
if os.path.exists("requirements.txt") and not os.path.exists(CONFIGFILE):
	os.system("pip install -r requirements.txt")

import tkinter as tk
import requests
import utils
import tomlkit as toml

try:
	os.mkdir("walltaker")
except FileExistsError:
	pass

def disconnected(e, quit=False):
	win = tk.Tk()
	win.title("Error")
	label = tk.Label(win, text="Connection error")
	statusL = tk.Label(win, text=e)
	label.pack()
	statusL.pack()
	win.mainloop()
	if quit:
		quit(0)

win = tk.Tk()
win.title("Walltaker YClient")

interval	= 60
linkID		= 0

if os.path.exists(CONFIGFILE):
	with open(CONFIGFILE, "r") as file:
		save = toml.load(file)
		interval = save["client"]["interval"]
		linkID = save["user"]["linkID"]

def new_wallpaper():
	global prevcall
	win.after_cancel(prevcall)
	prevcall = win.after(interval*1000, new_wallpaper)
	try:
		link = requests.get(f"https://walltaker.joi.how/links/{linkID}.json",
						headers={"User-Agent": "Yuri-client"},
						timeout=10)
	except requests.exceptions.ConnectionError as e:
		disconnected(e)
		win.after_cancel(prevcall)
		prevcall = win.after(10_000, new_wallpaper)
		return
		
	link = link.json()
	
	try:
		post = link["post_url"]
	except KeyError:
		disconnected("Invalid linkID")
		win.after_cancel(prevcall)
		prevcall = win.after(10_000, new_wallpaper)
		#return

	filename = post.split("/")[-1]

	if os.path.exists(f"walltaker/{filename}"):
		print(f"{filename} already exists")
	else:
		with open(f"walltaker/{filename}", "wb") as file:
			file.write(requests.get(post).content)

	utils.setBackground(f"{os.path.join(os.path.dirname(__file__),f'walltaker/{filename}')}")
	print(utils.getBackground())

def update(newInterval, newLinkID):
	global interval, linkID
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

prevcall = win.after(1_000, new_wallpaper)
win.mainloop()

with(open(CONFIGFILE,"w")) as file:
	save = {
		"client": {
			"interval": interval
		},
		"user": {
			"linkID": linkID
		}
	}
	toml.dump(save, file)

print("Exiting")
exit(0)