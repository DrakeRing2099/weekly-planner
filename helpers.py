import pickle
# This function retrieves data from the binary file
def retrieveData():
    try:
        with open("data.bin", "rb") as file:
            retreivedData = pickle.load(file)
    except EOFError:
        retreivedData = []
    return retreivedData

def pushData(retreivedData, newData):
    retreivedData.append(newData)
    with open("data.bin", "wb") as file:
        retreivedData = pickle.dump(retreivedData, file)

def checkTasks(taskList):
    retrievedData = retrieveData()
    for i in retrievedData:
        if i["taskname"] in taskList:
            retrievedData.remove(i)
    with open("data.bin", "wb") as file:
        retrievedData = pickle.dump(retrievedData, file)

