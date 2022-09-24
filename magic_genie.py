    # Made by Sven Leidenbach
import random
import time
from threading import Thread
guesses = []
test_guesses = list("111111111111111111111111111113789578978938795879487987978956789497887987987957899789789785786978")
for num in test_guesses:
    num = int(num)
    guesses.extend(str(num))
print(guesses)
correct_guesses = 0
incorrect_guesses = 0
newcount = 0
live_list = []

def waitinput():
    wait_input_str = input("Please enter a number from one to ten")
    live_list.append(str(wait_input_str))


def start_countdown():
    thd = Thread(target=waitinput)
    thd.daemon = True
    thd.start()
    for i in reversed(range(1, 11)):
        if not thd.is_alive():
            # Execute 2
            break
        print("\r countdown: {} seconds ".format(i), end="Please enter a number from one to ten")
        time.sleep(1)

    if thd.is_alive():
        # Execute 1
        print("\nCountdown has ended")


def GetSequences(guesses_in): # This function fetches all guesses, the last x guesses are then matched and the next item is added to an index in a new list
    list_length = len(guesses_in)
    sequence_length = 0
    next_guesses = []
    new_list = []
    found_match = 1
    for k in range(list_length):
        if found_match > 0:
            found_match = 0
            start_range = 0
            sequence_counter = 0
            end_range = sequence_length  # note that sequence length will increase 1 at the end of each loop
            if sequence_length > 0:
                sequence = guesses_in[(list_length-sequence_length):list_length]
            else:
                sequence = [guesses_in[-1]]

            for x in range(list_length-sequence_length):
                if guesses_in[start_range:end_range+1] == sequence and len(guesses_in) > end_range + 1:  # we go over the list of the guesses and look for matches, then add any matches to a new list
                    sequence_counter += 1
                    next_index = guesses_in[end_range]
                    distance_from_end = list_length - end_range
                    next_guesses.append([sequence,guesses_in[end_range+1],distance_from_end])
                    found_match = 1
                start_range += 1
                end_range += 1
            sequence_length += 1
            sequence_counter = 0

    return next_guesses


def Get_Probabilities(input_list, weight_length, weight_recency, weight_frequency):
    guesses_in = input_list
    processed_data = GetSequences(input_list)
    result_matches = 1
    result_notmatches = 1
    length_multiplier = 1
    probability_list = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    for sub_list in processed_data:
      #  print (processed_data)
        counter = 0
        length_multiplier = (len(sub_list[0])) * weight_length
        if len(sub_list) > 1:
            next_number = int(sub_list[-2])
            if len(probability_list[next_number]) > 1:
                last_add = probability_list[next_number][-1]
            else:
                last_add = 0
            frequency_bias = (int(guesses_in.count(str(next_number))) / int(len(guesses_in))) * weight_frequency
            recencey_bias = ((len(guesses_in)+1) / int(sub_list[-1])) * weight_recency
            result_matches = frequency_bias * recencey_bias
            probability_list[next_number-1].append(result_matches)
            counter += 1

    prob_outcomes = []
    countr = 0
    if len(guesses_in) > 0 and len(processed_data) > 0:
        for h in probability_list:
            if len(h) > 1:
                prob_outcomes.append([countr+1,sum(h[1:])])
            countr += 1
        idx, max_value = max(prob_outcomes, key=lambda item: item[-1])
        return int(idx)



def learn():
    learned_list = []
    weight_length = 1
    weight_recency = 0
    weight_frequency = 1
    correct_ratio = 0
    while weight_recency < 1:
        weight_recency += 0.1
        weight_length -= 0.1
        weight_frequency -= 0.1
        simul_right = 1
        simul_wrong = 1
        for n in range(0, len(guesses)-1):
            predicted_number = Get_Probabilities(guesses[0:n], weight_length, weight_recency, weight_frequency)
            if predicted_number is not None:
                if int(predicted_number) == int(guesses[n+1]):
                    simul_right += 1
                else:
                    simul_wrong += 1
            correct_ratio = simul_right / (simul_wrong+simul_right)
        learned_list.append([correct_ratio, weight_frequency, weight_recency])
        print(learned_list)





learn()
time.sleep(100)
while True:
    if newcount > 0:
        prediction = Get_Probabilities()
    else:
       # print("Guessing randomly due to lack of info")
        prediction = random.randint(0,10)
    if str(prediction) == "None":
       # print("Guessing randomly due to lack of info")
        prediction = random.randint(0, 10)

    number_guessed = input("Guess a number between 1 and 10")
 #   number_guessed = random.randint(1,10) # this makes the input random for testing, comment the line above if you uncomment this one
    if number_guessed is not None:
        if number_guessed.isnumeric() == True:
            number_guessed = int(number_guessed)
            if 1 <= int(number_guessed) <= 11:
                guesses.append(number_guessed)
                error_message = 0
            else:
                print("Your input did not match the requirements")
                error_message = 1
            if error_message == 0:
                if number_guessed == prediction:
                    correct_guesses += 1
                    print("I predicted correctly, I guessed " + str((
                        correct_guesses/(correct_guesses+incorrect_guesses)*100)) + "% of your predictions so far")
                else:
                    incorrect_guesses += 1
                    print("I predicted incorrectly, my guess was " + str(prediction) + " I guessed " + str((
                        correct_guesses / (correct_guesses + incorrect_guesses))*100) + "% of your predictions so far")
    else:
        print("You did not guess in time, or your input wasn't a number, try again")
    newcount += 1



