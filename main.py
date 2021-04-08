import json
import sys
import os
import random

#cmd template:
#python3 main.py -input="name" -expect_out=true

def parseArgs(args):
    result = {}
    for el in args[1:]:
        temp = el.replace('-', '')
        temp = temp.split('=')
        result[temp[0]] = temp[1]
    return result

def readFile(args):
    try:
        input_file = open("./input/{}".format(args["input"]), "r")
        return input_file
    except IOError:
        print("File couldn't be open")
        return -1

def parseJsonInfo(json):
    # If points or declared weren't specified in given template
    if not (json["points"] and json["declarations"]):
        print("Input file is invalid")
        return - 1
    points = {}
    tasks = {}
    priorities = {}

    # Make a dict of points of every student
    for index in json["points"]:
        points[index] = int(json["points"][index])

    # Make a dict of tasks and list of students declaring that task
    for index in json["declarations"]:
        for task in json["declarations"][index]:
            if not task in tasks:
                tasks[task] = [index]
            else:
                tasks[task].append(index)
    
    # Make a dict of tasks and list of students who have priority over this task
    for index in json["priority"]:
        if not json["priority"][index] in priorities:
            priorities[json["priority"][index]] = [index]
        else:
            priorities[json["priority"][index]].append(index)

    return points, tasks, priorities
        
def makeQueue(points, tasks, priorities, declarations):
    queue = {}
    # How many tasks has given student done so far
    done = {}
    for task in tasks:
        # print("Current task: ", task)
        min_points = 999
        min_declared = 999
        min_done = 999
        min_index = ""
        same_indexes = [] # Pick random index from this list in case of same priority over current task
        prio_index = ""

        for index in tasks[task]:
            # Populate done dict with: index: 0
            if not index in done:
                done[index] = 0
            # If given student has less points than others, less declared tasks than others and done less tasks today, he has priority in the queue
            # Also if one or more students have declared priority, we also check below conditions
            # print(declarations[index])
            if (len(declarations[index]) == min_declared and done[index] == min_done and points[index] == min_points): same_indexes.append(index)
            if (len(declarations[index]) < min_declared or done[index] < min_done or points[index] < min_points):
                # If someone has already been assigned this task with priority, skip if current student isn't prioritized
                if prio_index and task in priorities and index not in priorities[task]: continue
                if task in priorities and index in priorities[task]: prio_index = index
                same_indexes = []
                # print(points[index], len(declarations[index]), done[index])
                min_index = index
                min_points = points[index]
                min_declared = len(declarations[index])
                min_done = done[index]
                same_indexes.append(index)
        
        if len(same_indexes) > 1: min_index = same_indexes[random.randrange(len(same_indexes))]
        if prio_index: min_index = prio_index
        queue[task] = min_index
        points[min_index] += 1
        done[min_index] += 1

    return sorted(queue.items())

def prettifyQueue(queue):
    result = []
    for task, index in queue:
        result.append("Zadanie {zad}:".format(zad=task).ljust(13, ' ') + "@{index}\n".format(index=index))
    return result

def output(queue, points, args):
    try:
        print("Attempting to create an output file . . .")
        output_file = open("./output/{}_out".format(args["input"][:-5]), "w+")
        output_file.writelines(prettifyQueue(queue))
        print("Output file created at: ./output/{}_out".format(args["input"][:-5]))

        expect_input = -1
        if "expect_out" in args and (args["expect_out"] == "true"):
            print("Attempting to create expected input . . .")
            expect_input = open("./input/{}_expected.json".format(args["input"][:-5]), "w+")
            expect_dict = {
                "points": points,
                "declarations": {},
                "priority": {},
            }
            json.dump(expect_dict, expect_input)
            print("Expected next input file created at: ./input/{}_expected".format(args["input"][:-5]))

    except IOError:
        print("File couldn't be written")
        return -1
    
    return 1
        


def main():
    os.makedirs("./output", exist_ok=True)
    os.makedirs("./input", exist_ok=True)

    print("Parsing cmd arguments . . .")
    if len(sys.argv) == 1:
        print("No command arugments were specified in commandline")
        return
    args = parseArgs(sys.argv)
    print("Success")

    print("Reading input file . . .")
    input_file = readFile(args)
    if input_file == -1: return
    print("Success")

    print("Loading to json . . .")
    input_json = json.loads(input_file.read())
    input_file.close()

    print("Parsing json to dicts . . .")
    points, tasks, priorities = parseJsonInfo(input_json)
    print("Making queue . . .")
    queue = makeQueue(points, tasks, priorities, input_json["declarations"])
    print("Queue created: ", queue)
    return output(queue, points, args)
    

if __name__ == "__main__":
    main()
