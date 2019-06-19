from programs.gw2lib import *


def getAllItems(chars, bank):
    for ch in chars:
        chName = ch['name']
        for bag in ch['bags']:
            if bag is not None:
                for i in bag['inventory']:
                    if i is not None:
                        i = getItem(i['id'])
                        ti = trackedItem(i, chName)
                        yield ti


def byPartialNameMatch(itemGen, name):
    return [x for x in itemGen if name.lower() in x['name'].lower()]

def main():
    chars = getAccountInfo('characters', DELETE_THIS)
    bank = getAccountInfo('bank', DELETE_THIS)

    n = "salvage"

    # search by partial name match
    allItems = getAllItems(chars, bank)
    found = byPartialNameMatch(allItems, n)
    for x in found:
        print(x['character'], x)


if __name__ == '__main__':
    main()
