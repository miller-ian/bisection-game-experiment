import os

directory = 'big_interval_results/'
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
    nameEnd = f_name.find("_main")
    participant.name = f_name[:nameEnd]
    
    lastLine = lines[-1]
    lastCharacter = lastLine[-1]
    if lastCharacter in 'nN':
        participant.binary_search_familiar = False
    else:
        participant.binary_search_familiar = True
    
    participant_responses = []
    submit_timestamps = []
    for i in range(1, len(lines)):
        previous_line = lines[i-1]
        line = lines[i]
        if "DATA" in line and "Keydown: Enter" in line and "EXP" in previous_line and "text:" in previous_line: 
            equalsSign = previous_line.find("=")
            key = previous_line[equalsSign + 2:]
            participant_responses.append(key)

            decimal = line.find(".")
            time = line[:decimal + 3]
            submit_timestamps.append(time)

            
    participant.responses = participant_responses

    
    deltas = []
    for i in range(len(submit_timestamps) - 1):
        floatTimeInitial = float(submit_timestamps[i])
        floatTimeFinal = float(submit_timestamps[i+1])
        delta = round(floatTimeFinal - floatTimeInitial, 3)
        deltas.append(delta)
    participant.response_times = deltas
    
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

# # test output: getting first responses
# participant_list = get_list()
# count = 0
# for i in participant_list:
#     print(i.name)
#     print(i.responses[0])
#     count += 1
# print(count)