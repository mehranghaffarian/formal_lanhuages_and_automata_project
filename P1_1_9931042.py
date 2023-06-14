with open('DFA_Input_1.txt', 'r') as file:
    data = file.read().splitlines()
file.close()

alphabets = data[0].split(" ")
stats = data[1].split(" ")
initialStates = data[2].split(" ")
finalStates = data[3].split(" ")
rules = []

for i in range(4, len(data)):
    rules.append(data[i].split(" "))

print("Please write the input string and press enter:")
givenString = input()
currentPossibleStates = initialStates.copy()
isCurrentLetterAcceptable = False
newPossibleStates = []

for i in range(len(givenString)):
    currentLetter = givenString[i]
    isCurrentLetterAcceptable = False
    newPossibleStates.clear()

    for j in range(len(currentPossibleStates)):
        currentPossibleState = currentPossibleStates[j]

        for k in range(len(rules)):
            rule = rules[k]
            if rule[0] == currentPossibleState and currentLetter == rule[1]:
                isCurrentLetterAcceptable = True
                newPossibleStates.append(rule[2])
                break  # because  in DFA there should be no other rule to make it nondeterministic

    if not isCurrentLetterAcceptable:
        break
    currentPossibleStates = newPossibleStates.copy()

for i in range(len(newPossibleStates)):
    if not(newPossibleStates[i] in finalStates):
        newPossibleStates.remove(newPossibleStates[i])

if len(newPossibleStates) == 0:
    print("The given string is not acceptable")
else:
    print("The given string is accepted and the possible final states are: ", newPossibleStates)
