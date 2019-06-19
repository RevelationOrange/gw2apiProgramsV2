import json
from urllib import request as urlReq
import os
from os import sep
import time
import codecs


# url strings
apiBase = "https://api.guildwars2.com/v2/"
itemsSubsect = "items?"
charactersSubsect = "characters?"
commercePricesSubsect = "commerce/prices?"
acctBankSubsect = "account/bank?"
recipesSubsect = "recipes?"
achievementSubsect = "achievements?"
acctAchievementsSubsect = "account/achievements?"
recipeSearch = "recipes/search?"
searchByInput = "input="
searchByOutput = "output="
idsReq = "ids="
authPref = 'access_token='
authSuff = '&'

# folder and file strings
baseFolder = '..'
databaseFolderName = 'dbFiles'
outputFolderName = 'outputFiles'
# itemListFolder = baseFolder + databaseFolder + 'itemLists' + sep
# recipeListFolder = baseFolder + databaseFolder + 'recipeLists' + sep
searchFolderName = 'sigilrune_files'
rsPricesFolderName = 'rsPrices'
masterItemFileName = 'masterItemList.json'
masterRecipeFileName = 'masterRecipeList.json'
newItemsFileName = 'newItems.txt'
newINamesFileName = 'newINames.txt'
newRecipesFileName = 'newRecipes.txt'
newRNamesFileName = 'newRNames.txt'
runeAndSigilsFileName = 'runesAndSigils.json'
stacksByItemFileName = 'extraStacksByItem.txt'
stacksByCharacterFileName = 'extraStacksByCharacter.txt'
charCacheFileName = "characters.json"
bankCacheFileName = "bank.json"
achievementCacheFileName = "achievements.json"

# full folder/file paths
masterItemFilePath = sep.join([baseFolder, databaseFolderName, masterItemFileName])
masterRecipeFilePath = sep.join([baseFolder, databaseFolderName, masterRecipeFileName])
charactersFolderPath = sep.join([baseFolder, outputFolderName])

# converters/switches/etc.
apiSectionSwitch = {'item': itemsSubsect, 'recipe': recipesSubsect}
masterFileSwitch = {'item': masterItemFilePath, 'recipe': masterRecipeFilePath}
acctApiSectionSwitch = {'characters': charactersSubsect, 'bank': acctBankSubsect, 'achievements': acctAchievementsSubsect}
cacheFileNameSwitch = {'characters': charCacheFileName, 'bank': bankCacheFileName, 'achievements': achievementCacheFileName}
rarityKey = {'Legendary': 0, 'Ascended': 1, 'Exotic': 2, 'Rare': 3, 'Masterwork': 4, 'Fine': 5, 'Basic': 6, 'Junk': 7}

# constants
apiIDLimit = 200

# master lists
__MIL = {}
__MRL = {}

# placeholders
noItemFound = {'name': "no item found with that id"}


if os.path.exists(masterItemFilePath):
    if os.path.isfile(masterItemFilePath):
        with open(masterItemFilePath) as masterItemFile:
            __MIL = json.load(masterItemFile)
        __MIL['45060'] = __MIL['43485']
if os.path.exists(masterRecipeFilePath):
    if os.path.isfile(masterRecipeFilePath):
        with open(masterRecipeFilePath) as masterRecipeFile:
            __MRL = json.load(masterRecipeFile)


class trackedItem:
    def __init__(self, i, chName):
        self.iDict = i
        self.iDict['character'] = chName

    def __getitem__(self, item):
        return self.iDict[item]

    def __repr__(self):
        return str(self.iDict)


def __getMIL():
    # function to easily get the new master item list json
    # simply loads the master item file and returns it as a json object
    with open(masterItemFilePath) as masterItemFile:
        theList = json.load(masterItemFile)
    theList['45060'] = theList['43485']
    return theList


def __getMRL():
    # function to easily get the new master recipe list json
    # just like getMRLv2()
    with open(masterRecipeFilePath) as masterRecipeFile:
        theList = json.load(masterRecipeFile)
    return theList


def getItem(iid):
    if str(iid) in __MIL:
        return __MIL[str(iid)]
    else:
        return noItemFound

def getAllItems():
    for iid in __MIL:
        yield __MIL[iid]


def findItemByName(name):
    for id in __MIL:
        if __MIL[id]['name'].lower() == name.lower():
            return __MIL[id]


def getAccountInfo(section, auth, fromCache=True):
    fpath = sep.join([baseFolder, databaseFolderName, cacheFileNameSwitch[section]])
    if fromCache:
        if os.path.exists(fpath):
            with open(fpath) as dataFile:
                return json.load(dataFile)

    print('updating cached data ({})'.format(section))
    url = apiBase + acctApiSectionSwitch[section] + authPref + auth + authSuff
    if section == 'characters':
        charIDs = json.load(urlReq.urlopen(url))
        reqIDs = ','.join(['%20'.join(x.split()) for x in charIDs])
        url = url + idsReq + reqIDs
    data = json.load(urlReq.urlopen(url))
    with open(fpath, 'w') as cacheFile:
        json.dump(data, cacheFile)
    return data


def getAchievements(idList):
    csvIDList = []
    achList = []
    for index in range(0, len(idList), apiIDLimit):
        csvIDs = ",".join([str(x) for x in idList[index:index+apiIDLimit]])
        csvIDList.append(csvIDs)
    for ids in csvIDList:
        req = apiBase + achievementSubsect + idsReq + ids
        achs = json.load(urlReq.urlopen(req))
        achList += achs
    return achList


def updateMasterList(which):
    if which == 'item':
        try:
            masterList = __getMIL()
            make = False
        except:
            print('no file found')
            make = True
    elif which == 'recipe':
        try:
            masterList = __getMRL()
            make = False
        except:
            print('no file found')
            make = True
    else:
        print(which, "is not a valid master list to update, please enter 'item' or 'recipe'")
        return

    sectionUrl = apiBase + apiSectionSwitch[which]
    allIDs = json.load(urlReq.urlopen(sectionUrl))
    allStrIDs = [str(x) for x in allIDs]
    csvIDList = []
    if make:
        masterList = {}
        print(allStrIDs[0], allStrIDs[-1])
        print("{} ids to add".format(len(allStrIDs)))
        for index in range(0, len(allStrIDs), apiIDLimit):
            csvIDs = ','.join(allStrIDs[index:index+apiIDLimit])
            csvIDList.append(csvIDs)

    else:
        masterIDList = masterList.keys()
        newIDs = [x for x in masterIDList^allStrIDs if x in allStrIDs]
        if len(newIDs) > 0:
            print(newIDs)
            print("{} new {} ids to add".format(len(newIDs), which))
            for index in range(0, len(newIDs), apiIDLimit):
                csvIDs = ",".join(newIDs[index:index+apiIDLimit])
                csvIDList.append(csvIDs)
        else:
            print("no new {}s to add".format(which))
            return

    for ids in csvIDList:
        req = sectionUrl + idsReq + ids
        print(req)
        for i in json.load(urlReq.urlopen(req)):
            masterList[i['id']] = i
    with open(masterFileSwitch[which], 'w') as masterFile:
        json.dump(masterList, masterFile)


