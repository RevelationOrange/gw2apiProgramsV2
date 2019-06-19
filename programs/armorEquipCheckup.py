from programs.gw2lib import *


def findEquips(bag):
    pass


def main():
    ignoredSlots = ['Sickle', 'Axe', 'Pick']
    slotList = ['HelmAquatic', 'Back', 'Coat', 'Boots', 'Gloves', 'Helm', 'Leggings',
                'Shoulders', 'Accessory', 'Ring', 'Amulet']
    typeList = ['Armor', 'Back', 'Trinket']

    chars = getAccountInfo('characters', None)
    equipDictByChar = {}
    equipsFromInvy = {}
    for ch in chars:
        equips = {}
        for item in ch['equipment']:
            if item['slot'] not in ignoredSlots:
                slot = item['slot']
                while slot[-1] in '12AB':
                    slot = slot[:-1]
                i = getItem(item['id'])
                # print(ch['name'], slot, i['name'], item['id'])
                if slot in equips:
                    if rarityKey[i['rarity']] > rarityKey[equips[slot]['rarity']]:
                        equips[slot] = i
                    elif rarityKey[i['rarity']] == rarityKey[equips[slot]['rarity']]:
                        if i['level'] < equips[slot]['level']:
                            equips[slot] = i
                else:
                    equips[slot] = i
        equipDictByChar[ch['name']] = equips
        invyEquips = []
        for bag in ch['bags']:
            if bag is not None:
                # invyEquips += findEquips(bag)
                pass
        for i in invyEquips:
            if i['type'] in typeList:
                print(i)
    print()
    for x in equipDictByChar:
        print("{}".format(x, equipDictByChar[x]))
        for k in equipDictByChar[x]:
            # print("({}, {})".format(k, equipDictByChar[x][k]))
            # print(equipDictByChar[x][k]['type'])
            pass
        print()


if __name__ == '__main__':
    main()
