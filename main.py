import sys
args = sys.argv[1:]
if args.count("-h") or args.count("--help") or args.count("-?"):
	print('Just run it normally')
	print("I won't make it cli")

import os
os.chdir(os.path.dirname(__file__))

CONFIGFILE = "config.toml"
if os.path.exists("requirements.txt") and not os.path.exists(CONFIGFILE):
	os.system("pip install -r requirements.txt")

import tkinter as tk
import requests
import utils
import tomlkit as toml
import walpier

try:
	os.mkdir("walltaker")
except FileExistsError:
	pass

def window_warn(e: BaseException, title="Error", quit=False):
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

prevURL		= 0
save		= {
	"user": {
		"APIKey": "",
		"linkID": 0
	},
	"client": {
		"interval": 60
	}
}

if os.path.exists(CONFIGFILE):
	try:
		with open(CONFIGFILE, "r") as file:
			save = toml.load(file)
	except toml.exceptions.NonExistentKey:
		pass

Client = walpier.WallClient(save["user"]["APIKey"])

def new_wallpaper():
	global prevcall, prevURL
	win.after_cancel(prevcall)
	prevcall = win.after(int(save["client"]["interval"]*1000), new_wallpaper)
	try:
		link = Client.get_wallpaper(save["user"]["linkID"])
	except ConnectionError as e:
		window_warn(e)
		win.after_cancel(prevcall)
		prevcall = win.after(10_000, new_wallpaper)
		return
	
	try:
		post = link["post_url"]
	except KeyError:
		window_warn("Invalid linkID")
		win.after_cancel(prevcall)
		prevcall = win.after(10_000, new_wallpaper)

	filename = post.split("/")[-1]

	if os.path.exists(f"walltaker/{filename}"):
		print(f"{filename} already exists")
	else:
		with open(f"walltaker/{filename}", "wb") as file:
			file.write(requests.get(post).content)

	utils.setBackground(f"{os.path.join(os.path.dirname(__file__),f'walltaker/{filename}')}")
	if prevURL != link["post_url"]:
		prevURL = link["post_url"]
		utils.toast("Walltaker", f"New wallpaper by {link['set_by']}")
		
	set_byL.config(text=f"Set by:\n{link['set_by']}")
	print(utils.getBackground())

prevcall = win.after(1_000, new_wallpaper)

def update(newInterval, newLinkID, newAPIKey):
	global Client
	try:
		if float(newInterval) < 1:
			window_warn("Interval is too short.")
			return
		save['client']['interval'] = float(newInterval)
		save['user']['linkID'] = int(newLinkID)
		Client = walpier.WallClient(newAPIKey)
		new_wallpaper()
		configWin.destroy()
	except ValueError:
		window_warn("Invalid interval or linkID")
	except RuntimeError:
		window_warn("Invalid API key")

def openConfigWin():
	global configWin
	configWin = tk.Tk()
	configWin.title("Configuration")

	frameL = tk.Frame(configWin)
	frameR = tk.Frame(configWin)
	
	intervalL	= tk.Label(frameL, text="Interval: ")
	intervalI	= tk.Entry(frameR, width=5, justify="center")

	linkL		= tk.Label(frameL, text="LinkID: ")
	linkIDI		= tk.Entry(frameR, width=6, justify="center")

	APIL		= tk.Label(frameL, text="API Key: ")
	APII		= tk.Entry(frameR, width=8, justify="center")
	
	updateB		= tk.Button(frameL, text="Update", command=lambda: update(intervalI.get(), linkIDI.get(), APII.get()))


	intervalI.insert(0, save['client']['interval'])
	linkIDI.insert(0, save["user"]["linkID"])
	APII.insert(0, save["user"]["APIKey"])
	
	# frameL
	intervalL.pack(side='top')
	linkL.pack(side='top')
	APIL.pack(side='top')
	updateB.pack(side='top')
	frameL.pack(side="left")

	# frameR
	intervalI.pack(side='top')
	linkIDI.pack(side='top')
	APII.pack(side='top')
	frameR.pack(side="right")


	configWin.mainloop()

def react(reaction, reactionText):
	response = Client.react(reaction, reactionText)
	if reaction == "disgust":
		new_wallpaper()
	if "message" in response.json():
		window_warn(response.json()['message'])

def reactWin():
	reactWin = tk.Tk()
	reactWin.title("React")

	ft = tk.Frame(reactWin)
	fb = tk.Frame(reactWin)

	# ft
	reactL	= tk.Label(ft, text="Message: ")
	reactI	= tk.Entry(ft, width=10, justify="center")
	reactL.pack(side='left')
	reactI.pack(side='right')
	ft.pack(side='top')

	# fb
	def send():
		react(reactsSelected.get(), reactI.get())
		reactWin.destroy()
	sendB	= tk.Button(fb, text="Send", command=send)
	sendB.pack()
	fb.pack(side="bottom")


	reactWin.mainloop()

fl = tk.Frame(win)
fr = tk.Frame(win)

reacts = [
	"came",
	"horny",
	"disgust"
]
reactsSelected	= tk.StringVar()
reactsSelected.set(reacts[1])

# fl
reactsMenu	= tk.OptionMenu(fl, reactsSelected, *reacts)
reactB		= tk.Button(fl, text="React", command=reactWin)

reactsMenu.pack()
reactB.pack()
fl.pack(side='left')

# fr
set_byL		= tk.Label(fr, text=f"Loading...")
configB		= tk.Button(fr, text="Configure", command=openConfigWin)
quitB		= tk.Button(fr, text="Quit", command=win.destroy)

set_byL.pack()
configB.pack()
quitB.pack()
fr.pack(side='right')

win.mainloop()

print("Saving")

with(open(CONFIGFILE,"w")) as file:
	toml.dump(save, file)

print("Exiting")
exit(0)