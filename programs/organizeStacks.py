import sys
from programs.gw2lib import *


stacksByItemFilePath = sep.join([baseFolder, outputFolderName, stacksByItemFileName])
stacksByCharacterFilePath = sep.join([baseFolder, outputFolderName, stacksByCharacterFileName])
maxStack = 250
ignoreIDList = [54604]


def bagAccount(bag, accountDict, chName):
    for item in bag:
        if item is not None:
            if item['count'] != maxStack:
                if 'charges' not in item:
                    if 'bound_to' not in item:
                        if item['id'] not in ignoreIDList:
                            m = getItem(item['id'])
                            if 'details' not in m or 'type' not in m['details'] or (m['details']['type'] not in ['Logging', 'Foraging', 'Mining']):
                                loc = item.copy()
                                loc['loc'] = chName
                                if item['id'] in accountDict:
                                    accountDict[item['id']].append(loc.copy())
                                else:
                                    accountDict[item['id']] = [loc.copy()]


def main():
    if len(sys.argv) < 2 and 0:
        print("No api key provided. Please provide your api key as the first argument. If you need to create one, "
              "you can do so at https://account.arena.net/applications")
        print("Be sure to include the 'character' and 'inventories' permissions for this program to work.")
        return
    # apiKey = sys.argv[1]

    chars = getAccountInfo('characters', DELETE_THIS)
    bank = getAccountInfo('bank', DELETE_THIS)

    locByCharDict = {}
    locByItemDict = {}
    locByCharText = []
    locByItemText = []
    for ch in chars:
        # print(ch['name'])
        for bag in ch['bags']:
            if bag is not None:
                bagAccount(bag['inventory'], locByItemDict, ch['name'])
        # print()
    bagAccount(bank, locByItemDict, "Bank")

    for k in locByItemDict:
        if len(locByItemDict[k]) > 1:
            locByItemText.append("{} - found in: {}".format(getItem(k)['name'], ", ".join(
                ["{} ({})".format(x['loc'], x['count']) for x in locByItemDict[k]])))
            for item in locByItemDict[k]:
                if item['loc'] in locByCharDict:
                    locByCharDict[item['loc']].append(item.copy())
                else:
                    locByCharDict[item['loc']] = [item.copy()]
    locByCharText.append("Bank")
    for item in locByCharDict['Bank']:
        thisSectionStr = "{} ({}): "
        others = []
        for i in locByItemDict[item['id']]:
            if i['loc'] == "Bank":
                thisSectionStr = thisSectionStr.format(getItem(i['id'])['name'], i['count'])
            else:
                others.append("{} ({})".format(i['loc'], i['count']))
        outpStr = thisSectionStr + ", ".join(others)
        locByCharText.append(outpStr)
    locByCharText.append("")
    for section in locByCharDict:
        if section != "Bank":
            locByCharText.append(section)
            for item in locByCharDict[section]:
                # print(i, locByCharDict[i])
                thisSectionStr = "{} ({}): "
                others = []
                for i in locByItemDict[item['id']]:
                    if i['loc'] == section:
                        thisSectionStr = thisSectionStr.format(getItem(i['id'])['name'], i['count'])
                    else:
                        others.append("{} ({})".format(i['loc'], i['count']))
                outpStr = thisSectionStr + ", ".join(others)
                locByCharText.append(outpStr)
            locByCharText.append("")
    del locByCharText[-1]
    with open(stacksByCharacterFilePath, 'w') as byCharFile:
        for line in locByCharText:
            byCharFile.write(line + "\n")

    with open(stacksByItemFilePath, 'w') as byItemFile:
        for line in locByItemText:
            byItemFile.write(line + "\n")


if __name__ == '__main__':
    main()
    # test()
