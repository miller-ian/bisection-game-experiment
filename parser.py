import os

directory = 'middle_interval_results/'
listOfLogFiles = []
for f in os.listdir('middle_interval_results'):
    if f.endswith('.log'):
        listOfLogFiles.append(f)

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
class Participant:
    def __init__(self, name=None, responses=[], response_times=[], binary_search_familiar=False):
        self.name = name
        self.responses = responses
        self.response_times = response_times
        self.binary_search_familiar = binary_search_familiar


def parse(f_name):
    participant = Participant()
    f = open(directory + f_name, 'r')
    lines = f.read().splitlines()
    f.close()
    name = ""
    for line in lines:
        if "DATA" in line:
            colon = line.find(":")
            key = line[colon + 2:]
            print(line)
            if key in alphabet:
                name += key
    participant.name = name[:-1]
    print("_____")
    print(name)
    if name[-1] in 'nN':
        participant.binary_search_familiar = False
    else:
        participant.binary_search_familiar = True
    
    indicesOfResponses = []
    count = 0
    for line in lines:
        if "EXP	text:" in line and "text =" in line:
            colon = line.find(":")
            key = line[colon + 2:]
            if "null" in line:
                indicesOfResponses.append(count-1)
            count += 1
    indicesOfResponses = indicesOfResponses[2:]
    indicesOfResponsesCopy = indicesOfResponses.copy()
    count = 0
    for line in lines:
        if "EXP	text:" in line and "text =" in line:
            colon = line.find(":")
            key = line[colon + 2:]

            if len(indicesOfResponses) > 0 and count == indicesOfResponses[0]:
                indicesOfResponses.pop(0)
                equalsSign = line.find("=")
                key = line[equalsSign + 2:]
                participant.responses.append(key)

            count += 1
    indicesOfSubmit = []
    for index in indicesOfResponsesCopy:
        indicesOfSubmit.append(index + 1)
    count = 0
    responseTimes = []
    for line in lines:
        if "EXP	text:" in line and "text =" in line:
            if len(indicesOfSubmit) > 0 and count == indicesOfSubmit[0]:
                decimal = line.find(".")
                time = line[:decimal + 4]
                responseTimes.append(time)
                indicesOfSubmit.pop(0)
            count += 1

    for i in range(len(responseTimes) - 1):
        floatTimeInitial = float(responseTimes[i])
        floatTimeFinal = float(responseTimes[i+1])
        delta = round(floatTimeFinal - floatTimeInitial, 3)

        participant.response_times.append(delta)
    
    return participant

def get_list():
    returnList = []
    count = 1
    for f in listOfLogFiles:
        participant = parse(f)
        returnList.append(participant)
        count += 1
        # if count == 2:
        #     break
    return returnList