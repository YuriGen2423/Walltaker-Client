import os
os.chdir(os.path.dirname(__file__))

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

def window_warn(e, title="Error", quit=False):
	win = tk.Tk()
	win.title(title)

	label = tk.Label(win, text="Error:")
	statusL = tk.Label(win, text=e)
	okB = tk.Button(win, text="Ok", command=win.destroy)

	label.pack()
	statusL.pack()
	okB.pack()
	
	win.mainloop()
	if quit:
		quit(0)

win = tk.Tk()
win.title("Walltaker YClient")

interval	= 60
linkID		= 0
APIKey		= ""

if os.path.exists(CONFIGFILE):
	try:
		with open(CONFIGFILE, "r") as file:
			save = toml.load(file)
			interval = save["client"]["interval"]
			linkID = save["user"]["linkID"]
			APIKey = save["user"]["APIKey"]
	except toml.exceptions.NonExistentKey:
		pass

def new_wallpaper():
	global prevcall
	win.after_cancel(prevcall)
	prevcall = win.after(interval*1000, new_wallpaper)
	try:
		link = requests.get(f"https://walltaker.joi.how/links/{linkID}.json",
						headers={"User-Agent": "Yuri-client"},
						timeout=10)
	except requests.exceptions.ConnectionError as e:
		window_warn(e)
		win.after_cancel(prevcall)
		prevcall = win.after(10_000, new_wallpaper)
		return
		
	link = link.json()
	
	try:
		post = link["post_url"]
	except KeyError:
		window_warn("Invalid linkID")
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
	set_byL.config(text=f"Set by:\n{link['set_by']}")
	print(utils.getBackground())

prevcall = win.after(1_000, new_wallpaper)

def update(newInterval, newLinkID, newAPIKey):
	global interval, linkID, APIKey
	try:
		interval = int(newInterval)
		linkID = int(newLinkID)
		APIKey = newAPIKey
		new_wallpaper()
		configWin.destroy()
	except ValueError:
		window_warn("Invalid interval or linkID")

def oconfigWin():
	global configWin
	configWin = tk.Tk()
	configWin.title("Configuration")
	
	intervalL	= tk.Label(configWin, text="Interval: ")
	intervalI	= tk.Entry(configWin, width=5, justify="center")

	linkL		= tk.Label(configWin, text="LinkID: ")
	linkIDI		= tk.Entry(configWin, width=6, justify="center")

	APIL		= tk.Label(configWin, text="API Key: ")
	APII		= tk.Entry(configWin, width=8, justify="center")
	
	updateB		= tk.Button(configWin, text="Update", command=lambda: update(intervalI.get(), linkIDI.get(), APII.get()))


	intervalI.insert(0, interval)
	linkIDI.insert(0, linkID)
	APII.insert(0, APIKey)
	
	intervalL.grid(row=0, column=0)
	intervalI.grid(row=0, column=1)

	linkL.grid(row=1, column=0)
	linkIDI.grid(row=1, column=1)

	APIL.grid(row=2, column=0)
	APII.grid(row=2, column=1)
	
	updateB.grid(row=3, column=0)

	configWin.mainloop()

def react(reaction, reactionText):
	response = requests.post(f"https://walltaker.joi.how/api/links/{linkID}/response.json", {
		"api_key": APIKey,
		"type": reaction,
		"text": reactionText
	})
	if reaction == "disgust":
		new_wallpaper()
	if "message" in response.json():
		window_warn(response.json()['message'])

def reactWin():
	reactWin = tk.Tk()
	reactWin.title("React")

	reactL	= tk.Label(reactWin, text="Reaction: ")
	reactI	= tk.Entry(reactWin, width=10, justify="center")

	def send():
		react(reactsSelected.get(), reactI.get())
		reactWin.destroy()
	sendB	= tk.Button(reactWin, text="Send", command=send)

	reactL.grid(row=0, column=0)
	reactI.grid(row=0, column=1)
	sendB.grid(row=1, column=0)

	reactWin.mainloop()

reacts = [
	"came",
	"horny",
	"disgust"
]
reactsSelected	= tk.StringVar()
reactsSelected.set(reacts[1])
reactsD			= tk.OptionMenu(win, reactsSelected, *reacts)

set_byL		= tk.Label(win, text=f"Loading...")

configB		= tk.Button(win, text="Configure", command=oconfigWin)
reactB		= tk.Button(win, text="React", command=reactWin)
quitB		= tk.Button(win, text="Quit", command=win.destroy)

reactsD.grid(row=0, column=0)
set_byL.grid(row=0, column=1)
reactB.grid(row=1, column=0)
configB.grid(row=1, column=1)
quitB.grid(row=1, column=2)

win.mainloop()

print("Saving")

with(open(CONFIGFILE,"w")) as file:
	save = {
		"client": {
			"interval": interval
		},
		"user": {
			"linkID": linkID,
			"APIKey": APIKey
		}
	}
	toml.dump(save, file)

print("Exiting")
exit(0)