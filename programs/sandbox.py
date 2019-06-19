from programs.gw2lib import *
import os
import json


def main():
    with open(masterItemFilePath) as masterItemFile0:
        MIL0 = json.load(masterItemFile0)
    # __MIL['45060'] = __MIL['43485']
    with open(sep.join([baseFolder, databaseFolderName, "x"+masterItemFileName])) as masterItemFile1:
        MIL1 = json.load(masterItemFile1)
    skeys0 = sorted(MIL0.keys())
    skeys1 = sorted(MIL1.keys())
    keyset0 = set(skeys0)
    keyset1 = set(skeys1)
    # print(len(skeys0), len(skeys1), len(keyset0), len(keyset1))
    for z in skeys1:
        if z in MIL0:
            x = MIL0[z]
            y = MIL1[z]
            if not (x==y):
                # print(z, MIL0[z], MIL1[z])
                pass


if __name__ == '__main__':
    main()
