import requests

cookie = input("Account cookie: ")
fileLocation = "Location to the rbxlx file"

def mapStuff():
	#region Map file
    mapData = open(fileLocation, 'rb').read()
    if fileLocation.endswith(".rbxlx"): # Clean if RBXLX 
        import scruber #not sure if doing this would work but i dont know why it wouldnt
        mapData = scruber.replace_referents(mapData)
        finalData = scruber.replace_script_guids(mapData)
    #endregion
    return finalData

def getXsrf(): #Get the Xsrf token bc roblox is a cunt
    xsrHeader = requests.post("https://auth.roblox.com/v2/login", headers={
        "X-CSRF-TOKEN": ""
    }, cookies={
        '.ROBLOSECURITY': cookie
    }).headers['x-csrf-token']
    return xsrHeader

xsrf = getXsrf()
userId = requests.get("https://users.roblox.com/v1/users/authenticated", headers={
        'x-csrf-token': xsrf,
        'User-Agent': 'Roblox/WinINet'
    }, cookies={
        '.ROBLOSECURITY': cookie
    }).json()["id"]

gameId = requests.get("https://inventory.roblox.com/v2/users/" + str(userId) + "/inventory/9?limit=10&sortOrder=Asc", headers={
        'x-csrf-token': xsrf,
        'User-Agent': 'Roblox/WinINet'
    }, cookies={
        '.ROBLOSECURITY': cookie
    }).json()["data"][0]["assetId"]

uploadRequest = requests.post("https://data.roblox.com/Data/Upload.ashx?assetid=" + str(gameId) + "&type=Place&name=ese&description=Sup&genreTypeId=1&ispublic=False",
   headers={
     'Content-Type': 'application/xml',
     'x-csrf-token': xsrf,
     'User-Agent': 'Roblox/WinINet'
   }, 
   cookies={
       '.ROBLOSECURITY': cookie
   }, data = mapStuff())

print(f'uploaded to https://roblox.com/games/{str(gameId)}/')
input('')
