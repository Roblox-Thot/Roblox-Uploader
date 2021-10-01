import requests
import scruber

def uploadFile(fileLocation, cookie):
    """ Returns game as a JSON 
    return {
        "link": gameLink
        "gameId": gameId,
        "userId": userId
    }
    """
    def mapStuff():
        #region Map file
        mapData = open(fileLocation, 'rb').read()
        if fileLocation.endswith(".rbxlx"): # Clean if RBXLX 
            mapData = scruber.replace_referents(mapData)
            finalData = scruber.replace_script_guids(mapData)
        #endregion
        return finalData

    def getXsrf():
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

    return {
        "link": f'https://roblox.com/games/{str(gameId)}/',
        "gameId": gameId,
        "userId": userId
    }
