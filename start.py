import os, shutil, time

import config

def checkConfigPath(path):
    if os.path.isdir(path):
        return True
    print('Директория не существует: ', path)
    return False

targetFilePath = os.path.join(config.target, config.file)

if checkConfigPath(config.source) and checkConfigPath(config.target):
    list = os.listdir(config.source)
    for item in list:
        sourceFilePath = os.path.join(config.source, item)
        if os.path.isfile(sourceFilePath):
            shutil.copy(sourceFilePath, targetFilePath)
            time.sleep(config.interval)
