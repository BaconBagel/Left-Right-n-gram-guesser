    # Made by Sven Leidenbach
import random
import time
from threading import Thread
guesses = []
test_guesses = list("623456234297543792573485723858579347895787389297734857837845789478239784795780422679710781782")
for num in test_guesses:
    num = int(num) + 1
    guesses.extend(str(num))
print(guesses)
correct_guesses = 0
incorrect_guesses = 0
newcount = 0
live_list = []


def GetSequences(guesses_in): # This function fetches all guesses, the last x guesses are then matched and the next item is added to an index in a new list
    list_length = len(guesses_in)
    next_guesses = []
    time_lag = range(0, 7) #modify this to be a function input later
    for lag in time_lag:
        sequence_length = 0
        while list_length > lag:
            found_match = 0
            start_range = 0
            end_range = sequence_length  # note that sequence length will increase 1 at the end of each loop
            if sequence_length > 0:
                sequence = guesses_in[(list_length-sequence_length-lag-1):list_length-lag]
            else:
                sequence = [guesses_in[-1-lag]]
            for x in range(list_length-sequence_length):
                if guesses_in[start_range:end_range+1] == sequence and len(guesses_in) > end_range + 1 + lag:  # we go over the list of the guesses and look for matches, then add any matches to a new list
                    distance_from_end = list_length - end_range
                    next_guesses.append([sequence,guesses_in[end_range+1+lag],distance_from_end,lag])
                    found_match += 1
                start_range += 1
                end_range += 1
            if found_match < 2:
                break
            sequence_length += 1
    return next_guesses


def Get_Probabilities(input_list, weight_length, weight_recency, weight_frequency, weight_lag):
    guesses_in = input_list
    processed_data = GetSequences(input_list)
    probability_list = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    for sub_list in processed_data:
        counter = 0
        if len(sub_list) > 1:  # Generates a likelyhood predictions score for the next number
            length_multiplier = (len(sub_list[0]) / len(probability_list)) * weight_length
            lag = int(sub_list[-1])
            lag_weight = (1/(lag+1))*weight_lag
            next_number = int(sub_list[-3])
            frequency_bias = (int(guesses_in.count(str(next_number))) / int(len(guesses_in))) * weight_frequency
            recencey_bias = ((len(guesses_in)+1) / int(sub_list[-2])) * weight_recency
            result_matches = (frequency_bias) * (recencey_bias) * (lag_weight) * (length_multiplier)
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


def step_optimiser():
    weight_length = 0
    weight_frequency = 0
    weight_lag = 0
    weight_recency = 0
    correct_ratio = 0
    last_prob = 0
    weight_number = 0
    step_size = 1
    learned_list = []
    anal_probe = 0
    while weight_number <= 5:
        auto_count = 0
        last_prob = 0
        weight_adder = 0
        weight_list = [weight_length, weight_lag, weight_frequency, weight_recency]
        while 0 <= auto_count <= 20:
            weight = weight_list[weight_number]
            if auto_count > 0:
                weight_adder += step_size
            simul_right = 1
            simul_wrong = 1
            for n in range(5, len(guesses) - 1): # Compare the forecast based on guesses 0:X to the actual outcome
                if weight_number == 0:
                    predicted_number = Get_Probabilities(guesses[0:n], weight + weight_adder, weight_lag, weight_frequency,
                                                         weight_recency)
                if weight_number == 1:
                    predicted_number = Get_Probabilities(guesses[0:n], weight_length, weight + weight_adder, weight_frequency,
                                                         weight_recency)
                if weight_number == 2:
                    predicted_number = Get_Probabilities(guesses[0:n], weight_length, weight_lag, weight + weight_adder,
                                                         weight_recency)
                if weight_number == 3:
                    predicted_number = Get_Probabilities(guesses[0:n], weight_length, weight_lag, weight_frequency,
                                                         weight + weight_adder)
                if predicted_number is not None:  # Checks if simulation predicted the next value
                    if int(predicted_number) == int(guesses[n + 1]):
                        simul_right += 1
                    else:
                        simul_wrong += 1
                correct_ratio = simul_right / (simul_wrong + simul_right)
                if auto_count == 0:
                    last_prob = correct_ratio
            learned_list.append([correct_ratio, weight])

            if last_prob < float(learned_list[-1][0]):
                last_prob = float(learned_list[-1][0])
                auto_count = 0
                anal_probe = 1
            elif learned_list[-1][0] < last_prob:
                auto_count = -1
                anal_probe = 1
            else:
                auto_count += 1
            if anal_probe == 1 or auto_count == 10:
                if weight_number == 0:
                    weight_length = weight + weight_adder
                if weight_number == 1:
                    weight_lag = weight + weight_adder
                if weight_number == 2:
                    weight_frequency = weight + weight_adder
                if weight_number == 3:
                    weight_recency = weight + weight_adder
                weight_list = [weight_length, weight_lag, weight_frequency, weight_recency]
            # print(learned_list[-1], last_prob, weight_numberweight)

            #  find a cleaner solution to the below
        weight_number += 1
        if weight_number > 3:
            weight_number = 0
            step_size = -1*step_size

        print(correct_ratio,last_prob, weight_frequency, weight_lag, weight_length, weight_recency)



step_optimiser()
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



