try:
    import re, secrets, uuid
    unblacklist = True
except ImportError:
    print("[!] You need to install the following modules: re, secrets, uuid if you want to unblacklist")
    unblacklist = False

import requests


cookie = input("Account cookie: ")
fileLocation = input("Location to the map file: ").replace("\"", "")

#region unblacklist
def replace_referents(data):
    cache = {}
    def _replace_ref(match):
        ref = match.group(1)
        if not ref in cache:
            cache[ref] = ("RBX" + secrets.token_hex(16).upper()).encode()
        return cache[ref]
    data = re.sub(
        b"(RBX[A-Z0-9]{32})",
        _replace_ref,
        data
    )
    return data

def replace_script_guids(data):
    cache = {}
    def _replace_guid(match):
        guid = match.group(1)
        if not guid in cache:
            cache[guid] = ("{" + str(uuid.uuid4()).upper() + "}").encode()
        return cache[guid]
    data = re.sub(
        b"(\{[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}\})",
        _replace_guid,
        data
    )
    return data
#endregion

def mapStuff():
	#region Map file
    mapData = open(fileLocation, 'rb').read()
    if fileLocation.endswith(".rbxlx") and unblacklist: # Clean if RBXLX 
        #not sure if doing this would work but i dont know why it wouldnt
       mapData = replace_referents(mapData)
       mapData = replace_script_guids(mapData)
    #endregion
    return mapData

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
