import os, shutil, queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config

def checkConfigPath(path):
    if os.path.isdir(path):
        return True
    print('Директория не существует: ', path)
    return False

def executeNextTask():
    if (not taskQueue.empty()):
        path = taskQueue.get()
        print(path, '->', taskFilePath)
        shutil.copy(path, taskFilePath)
    else:
        print('Завершено')
        observer.stop()

def onFileEvent(event):
    if (event.src_path == taskFilePath):
        executeNextTask()

def createEventObserver():
    handler = FileSystemEventHandler()
    handler.on_deleted = onFileEvent
    observer = Observer()
    observer.schedule(handler, config.target)
    observer.start()
    return observer

taskFilePath = os.path.join(config.target, config.task)
taskQueue = queue.Queue()

if checkConfigPath(config.source) and checkConfigPath(config.target):
    list = os.listdir(config.source)
    for item in list:
        sourceFilePath = os.path.join(config.source, item)
        if os.path.isfile(sourceFilePath):
            taskQueue.put(sourceFilePath)
    if (not taskQueue.empty()):
        observer = createEventObserver()
        executeNextTask()
        observer.join()
