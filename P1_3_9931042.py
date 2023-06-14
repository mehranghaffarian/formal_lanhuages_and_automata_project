with open('RE_Input_3.txt', 'r') as file:
    data = file.read().splitlines()
file.close()

alphabets = data[0].split(" ")
languages_count = 0


class Language:
    def __init__(self, states, initial_states, final_state, rules):
        global languages_count
        self.language_name = 'L'+str(languages_count)
        states_dictionary = {}
        for i in range(len(states)):
            s = states[i]
            states_dictionary[s] = self.language_name + "q" + str(i)
        self.states = [states_dictionary[s] for s in states]
        self.initialStates = [states_dictionary[s] for s in initial_states]
        self.finalStates = [states_dictionary[s] for s in final_state]
        self.rules = [[states_dictionary[r[0]], r[1], states_dictionary[r[2]]] for r in rules]
        languages_count += 1


# implementing the third step to transfer RE to NFA
def find_single_word_language(word):
    global languages_count
    language_name = "L" + str(languages_count)
    states = [language_name + "q0", language_name + "q1"]
    initial_states = [language_name + "q0"]
    final_state = [language_name + "q1"]
    rules = [[language_name + "q0", word, language_name + "q1"]]

    return Language(states, initial_states, final_state, rules)


# implementing the 4.2 step to transfer RE to NFA
def find_languages_concatenation_language(first_language: Language, second_language: Language):
    states = first_language.states.copy()
    states.extend(second_language.states)
    initial_states = first_language.initialStates.copy()
    final_states = second_language.finalStates.copy()
    rules = first_language.rules.copy()
    rules.append([first_language.finalStates.copy()[-1], "λ", second_language.initialStates.copy()[0]])
    rules.extend(second_language.rules)

    return Language(states, initial_states, final_states, rules)


# implementing the 4.1 step to transfer RE to NFA
def find_languages_or_language(first_language: Language, second_language: Language):
    states = first_language.states.copy()
    states.extend(second_language.states)
    states.append("q0")
    states.append("q1")
    initial_states = ["q0"]
    final_states = ["q1"]
    rules = first_language.rules.copy()
    rules.extend(second_language.rules)

    rules.append(["q0", "λ", first_language.initialStates.copy()[0]])
    rules.append([first_language.finalStates.copy()[-1], "λ", "q1"])

    rules.append(["q0", "λ", second_language.initialStates.copy()[0]])
    rules.append([second_language.finalStates.copy()[-1], "λ", "q1"])

    return Language(states, initial_states, final_states, rules)


# implementing the 4.3 step to transfer RE to NFA, it also supports numeric powers such as 1, 2, 3, ...
def find_language_power_language(lang: Language, power):
    states = lang.states.copy()
    states.append("q0")
    states.append("q1")
    initial_states = ["q0"]
    final_states = ["q1"]
    rules = lang.rules.copy()

    rules.append(["q0", "λ", lang.initialStates.copy()[0]])
    rules.append(["q0", "λ", "q1"])
    rules.append([lang.finalStates.copy()[-1], "λ", lang.initialStates.copy()[0]])
    rules.append([lang.finalStates.copy()[-1], "λ", "q1"])

    core_lang = Language(states, initial_states, final_states, rules)
    if power == "*":
        return core_lang
    else:
        concatenated_lang = find_single_word_language("λ")

        for i in range(int(power)):
            concatenated_lang = find_languages_concatenation_language(concatenated_lang, lang)
        return concatenated_lang


# the main loop to find the NFA, it iterates over the regular expression and in each step find the equivalent language
# or finds the language in a parenthesis. the whole process is implemented recursively
# in each call the previously figured is given to find the next language, sometimes it is None when we have to
# determine the language in a parenthesis or when we have just started the process
def find_language_from_re(given_data, previous_lang=None):
    finding_parenthesis_end = False
    language_in_parenthesis = ''
    for i in range(len(given_data)):
        c = given_data[i]
        if finding_parenthesis_end:
            if c == ')':  # determining the language in the parenthesis
                parenthesis_lang = find_language_from_re(language_in_parenthesis)
                if i == len(given_data) - 1:  # checking the data length to avoid index out of bound exception
                    if previous_lang is None:
                        return parenthesis_lang
                    else:
                        return find_languages_concatenation_language(previous_lang, parenthesis_lang)
                else:
                    if given_data[i+1] == '^':  # finding the language with the power
                        powered_lang = find_language_power_language(parenthesis_lang, given_data[i + 2])
                        if len(given_data) == i+3:  # checking the data length to avoid index out of bound exception
                            if previous_lang is None:
                                return powered_lang
                            else:
                                return find_languages_concatenation_language(previous_lang, powered_lang)
                        else:
                            if previous_lang is None:
                                return find_language_from_re(given_data[i + 3:len(given_data)], powered_lang)
                            else:
                                return find_language_from_re(given_data[i + 3:len(given_data)],
                                                             find_languages_concatenation_language(previous_lang,
                                                                                                   powered_lang))
                    else:
                        if previous_lang is None:
                            return find_language_from_re(given_data[i + 1:len(given_data)], parenthesis_lang)
                        else:
                            return find_language_from_re(given_data[i + 1:len(given_data)],
                                                         find_languages_concatenation_language(previous_lang,
                                                                                               parenthesis_lang))
            else:
                language_in_parenthesis += c
        else:
            if c in alphabets:
                single_word_lang = find_single_word_language(c)
                if previous_lang is None:
                    if i == len(given_data) - 1:  # checking the data length to avoid index out of bound exception
                        return single_word_lang
                    else:
                        return find_language_from_re(given_data[i+1:len(given_data)], single_word_lang)
                else:
                    curr_lang = find_languages_concatenation_language(previous_lang, single_word_lang)
                    if i == len(given_data)-1:  # checking the data length to avoid index out of bound exception
                        return curr_lang
                    else:
                        return find_language_from_re(given_data[i+1:len(given_data)], curr_lang)
            elif c == '+':  # there must be a previous lang otherwise the regular expression is not acceptable
                return find_languages_or_language(previous_lang,
                                                  find_language_from_re(given_data[(i + 1):len(given_data)]))
            elif c == '(':
                if previous_lang is None:
                    finding_parenthesis_end = True  # starting to concatenate the string in the paranthesis
                else:
                    return find_languages_concatenation_language(previous_lang,
                                                                 find_language_from_re(
                                                                     given_data[i:len(given_data)]))
    return Language(["q-1"], ["q-1"], ["q-1"], ["L-1"])


language = find_language_from_re(data[1])


# renaming the states to see them better
def find_state_new_name(state):
    for i in range(len(language.states)):
        if language.states[i] == state:
            return "q" + str(i)
    return "Unknown"


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


with open('NFA_Output_2.txt', 'w', encoding="utf-8") as destinationFile:
    write_list(alphabets, destinationFile)
    write_list([find_state_new_name(s) for s in language.states], destinationFile)
    write_list([find_state_new_name(s) for s in language.initialStates], destinationFile)
    write_list([find_state_new_name(s) for s in language.finalStates], destinationFile)
    write_list([[find_state_new_name(r[0]), r[1], find_state_new_name(r[2])] for r in language.rules], destinationFile,
               is_rule=True)
destinationFile.close()

print("In the output the states are renamed as follow:")
for index in range(len(language.states)):
    print(language.states[index], "->", "q" + str(index))

print("Extra information are mentioned above enter anything to finish:")
junk = input()
