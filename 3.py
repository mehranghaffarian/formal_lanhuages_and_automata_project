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


def find_words_string_language(words):
    global languages_count

    curr = None
    for a in words:
        if curr is None:
            curr = find_single_word_language(a)
        else:
            curr = find_languages_concatenation_language(curr, find_single_word_language(a))

    return curr


def find_single_word_language(word):
    global languages_count
    language_name = "L" + str(languages_count)
    states = [language_name + "q0", language_name + "q1"]
    initial_states = [language_name + "q0"]
    final_state = [language_name + "q1"]
    rules = [[language_name + "q0", word, language_name + "q1"]]

    return Language(states, initial_states, final_state, rules)


def find_languages_concatenation_language(first_language: Language, second_language: Language):
    states = first_language.states.copy()
    states.extend(second_language.states)
    initial_states = first_language.initialStates.copy()
    final_states = second_language.finalStates.copy()
    rules = first_language.rules.copy()
    rules.append([rules[-1][0], "λ", second_language.initialStates.copy()[0]])
    rules.extend(second_language.rules)

    return Language(states, initial_states, final_states, rules)


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
    rules.append([first_language.finalStates.copy()[0], "λ", "q1"])

    rules.append(["q0", "λ", second_language.initialStates.copy()[0]])
    rules.append([second_language.finalStates.copy()[0], "λ", "q1"])

    return Language(states, initial_states, final_states, rules)


def find_language_power_language(first_language: Language, power):
    states = first_language.states.copy()
    states.append("q0")
    states.append("q1")
    initial_states = ["q0"]
    final_states = ["q1"]
    rules = first_language.rules.copy()

    rules.append(["q0", "λ", first_language.initialStates.copy()[0]])
    rules.append(["q0", "λ", "q1"])
    rules.append([first_language.finalStates.copy()[-1], "λ", first_language.initialStates.copy()[0]])

    return Language(states, initial_states, final_states, rules)


def find_language_from_re(given_data, curr_lang=None):
    finding_parenthesis_end = False
    language_in_parenthesis = ''
    current_alphabets_string = ''
    for i in range(len(given_data)):
        c = given_data[i]
        print(given_data, " -> ", c)
        if finding_parenthesis_end:
            if c == ')':
                if i == len(given_data) - 1:
                    return find_language_from_re(language_in_parenthesis)
                else:
                    if given_data[i+1] == '^':
                        powered_lang = find_language_power_language(find_language_from_re(language_in_parenthesis), given_data[i + 2])

                        if len(given_data) > i+3:
                            return find_language_from_re(given_data[i+3:len(given_data)], powered_lang)
                        else:
                            return powered_lang
                    else:
                        return find_languages_concatenation_language(find_language_from_re(language_in_parenthesis), given_data[i+1:len(given_data)])
            else:
                language_in_parenthesis += c
        else:
            if c in alphabets:
                current_alphabets_string += c
            elif c == '+':
                return find_languages_or_language(find_words_string_language(current_alphabets_string),
                                                  find_language_from_re(given_data[(i + 1):len(given_data)]))
            elif c == '(':
                if len(current_alphabets_string) > 0:
                    return find_languages_concatenation_language(find_words_string_language(current_alphabets_string),
                                                                 find_language_from_re(
                                                                     given_data[i:len(given_data)]))
                else:
                    finding_parenthesis_end = True
    return find_words_string_language(current_alphabets_string)


language = find_language_from_re(data[1])
print(data[1])
print(language.states)
print(language.initialStates)
print(language.finalStates)
print(language.rules)
# a b
# (a+b)^*b
# a(a+b)^*b(ab(ba)^*b)+a


# 0 1
# q0 q1 q2
# q0
# q1
# q0 λ q1
# q0 0 q1
# q1 0 q0
# q1 1 q1
# q1 0 q2
# q1 1 q2
# q2 0 q2
# q2 1 q1
