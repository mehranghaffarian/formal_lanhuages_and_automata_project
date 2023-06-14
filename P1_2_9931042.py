# change the Î» with any thing that λ would look like in a python list in your system
with open('NFA_Input_2.txt', 'r') as file:
    data = file.read().splitlines()
file.close()

alphabets = data[0].split(" ")
states = data[1].split(" ")
initialStates = data[2].split(" ")
finalStates = data[3].split(" ")
rules = []

for i in range(4, len(data)):
    rules.append(data[i].split(" "))

statesLambdaClosure = {}

# finding the states lambda closures
for i in range(len(states)):
    currentState = states[i]

    for j in range(len(rules)):
        currentRule = rules[j]

        if currentState == currentRule[0] and (currentRule[1] == "Î»" or currentRule[
            1] == "λ"):  # in my laptop λ is loaded as Î» so i have to check both
            if currentState not in statesLambdaClosure:
                statesLambdaClosure[currentState] = [currentRule[2]]
            else:
                statesLambdaClosure[currentState].append(currentRule[2])

            count = 0

            while count < len(statesLambdaClosure[currentState]):
                newCurrentState = statesLambdaClosure[currentState][count]

                # checking for the new reachable states
                for k in range(len(rules)):
                    newCurrentRule = rules[k]

                    if newCurrentState == newCurrentRule[0] and (
                            newCurrentRule[1] == "Î»" or newCurrentRule[1] == "λ") and newCurrentRule[2] not in \
                            statesLambdaClosure[currentState]:  # in my laptop λ is loaded as Î» so i have to check both
                        statesLambdaClosure[currentState].append(newCurrentRule[2])

                count += 1

initialStates.sort()
newInitialStates = []
newStates = []

for s in initialStates:
    newInitialStates.append([s])
    newStates.append([s])

newRules = []
# initial for to find the new states
for currentNewState in newStates:
    for currentLetter in alphabets:
        currentReachableStates = []
        for currentNewSingleState in currentNewState:
            for currentRule in rules:
                if currentRule[1] == currentLetter and (currentRule[0] == currentNewSingleState or (
                        currentNewSingleState in statesLambdaClosure and currentRule[0] in statesLambdaClosure[
                    currentNewSingleState])):
                    if currentRule[2] not in currentReachableStates:
                        currentReachableStates.append(currentRule[2])

                    if currentRule[2] in statesLambdaClosure:
                        for s in statesLambdaClosure[currentRule[2]]:
                            if s not in currentReachableStates:
                                currentReachableStates.append(s)

            currentReachableStates.sort()
            stateNotCurrentlyAdded = True
            for s in newStates:
                if s == currentReachableStates:
                    stateNotCurrentlyAdded = False

            if stateNotCurrentlyAdded:
                newStates.append(currentReachableStates)
            if len(currentReachableStates) != 0:
                newRule = [currentNewState, currentLetter, currentReachableStates]
                if len(newRules) == 0 or newRule != newRules[-1]:  # checking if the newRule is not currently added
                    newRules.append(newRule)

newFinalStates = []
for currentState in newStates:
    for currentSingleState in currentState:
        isStateAdded = False

        if isStateAdded:
            break
        for finalState in finalStates:
            if finalState == currentSingleState or (
                    currentSingleState in statesLambdaClosure and finalState in statesLambdaClosure[
                currentSingleState]):
                isStateAdded = True

                if len(newFinalStates) == 0:
                    newFinalStates.append(currentState)
                else:
                    newFinalStates[-1].sort()

                    if newFinalStates[-1] != currentState:
                        newFinalStates.append(currentState)
                break


# helper function to write the language properties in the file better
def write_list(given_list, file_descriptor, is_rule=False):
    final_string = ""
    for t in given_list:
        if isinstance(t, list):
            if is_rule:
                write_list(t, file_descriptor)
            else:
                final_string += "["
                final_string += ", ".join(t)
                final_string += "]"
        else:
            final_string += t
        final_string += " "
    file_descriptor.write(final_string + "\n")


# renaming the states to see them better
def find_state_new_name(state):
    for a in range(len(newStates)):
        if newStates[a] == state:
            return "q" + str(a)
    return "Unknown"


with open('NFA_Output_2.txt', 'w') as destinationFile:
    write_list(alphabets, destinationFile)

    newStatesToWrite = []
    for s in newStates:
        newStatesToWrite.append(find_state_new_name(s))
    write_list(newStatesToWrite, destinationFile)

    newInitialStatesToWrite = []
    for s in newInitialStates:
        newInitialStatesToWrite.append(find_state_new_name(s))
    write_list(newInitialStatesToWrite, destinationFile)

    newFinalStatesToWrite = []
    for s in newFinalStates:
        newFinalStatesToWrite.append(find_state_new_name(s))
    write_list(newFinalStatesToWrite, destinationFile)

    newRulesToWrite = []
    for r in newRules:
        newRulesToWrite.append([find_state_new_name(r[0]), r[1], find_state_new_name(r[2])])
    write_list(newRulesToWrite, destinationFile, is_rule=True)

destinationFile.close()

print("In the output the states are renamed as follow:")
for index in range(len(newStates)):
    print(newStates[index], "->", "q" + str(index))

print("Extra information are mentioned above enter anything to finish:")
junk = input()
