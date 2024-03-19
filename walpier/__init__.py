import requests

# User example:
# client = WallClient("API__KEY")
class WallClient:
	def __init__(self, APIKey="", userAgent = "Yuri-Client", timeout = 10):
		self.APIKey = APIKey
		self.userAgent = userAgent
		self.timeout = timeout
		if len(self.APIKey)>0 and (self.APIKey.__len__()<8 or self.APIKey.__len__()>8):
			raise RuntimeError("Invalid API key\nKeys are explicitly 8 characters long")

	def get_wallpaper(self, linkID):
		return requests.get(f"https://walltaker.joi.how/links/{linkID}.json",
					  		headers={ "User-Agent": self.userAgent },
							timeout=self.timeout).json()

	def react(self, reaction, reactionText):
		return requests.post(f"https://walltaker.joi.how/api/links/{self.linkID}/response.json", {
			"api_key": self.APIKey,
			"reaction": reaction,
			"text": reactionText
		}, headers={ "User-Agent": self.userAgent }, timeout=self.timeout).json()
	
if __name__ == "__main__":
	import tomlkit as toml
	with open("config.toml", "r") as file:
		save = toml.load(file)
	Client = WallClient(save["user"]["APIKey"])
	print(Client.get_wallpaper(save["user"]["linkID"]))