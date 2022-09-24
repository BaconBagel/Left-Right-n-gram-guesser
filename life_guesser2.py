# Made by Sven Leidenbach - A basic number predictor using simple arithmetic and supervised learning
import random

guesses, live_list = [], [],
probability_list = []
testing_data = ["68686868868688686886868668668686868868686888686886868686686868686868868686868686886"]
training_data = ["68686868868688686886868668668686868868686888686886868686686868686868868686868686886"]
tester = []
import time
for num in training_data:
    num = int(num)
    guesses.extend(str(num))
for num in testing_data:
    num = int(num)
    tester.extend(str(num))
print(guesses)
correct_guesses, incorrect_guesses, newcount = 0, 0, 0


def GetSequences(guesses_in): # This function fetches all guesses, the last x guesses are then matched and the next item is added to an index in a new list
    list_length = len(guesses_in)
    next_guesses = []
    time_lag = range(0, 10) #modify this to be a function input later
    for lag in time_lag:
        sequence_length = 0
        while list_length > lag:
            found_match, start_range = 0, 0
            end_range = sequence_length  # note that sequence length will increase 1 at the end of each loop
            if sequence_length > 0:
                sequence = guesses_in[(list_length-sequence_length-lag-1):list_length-lag]
            else:
                sequence = [guesses_in[-1-lag]]
            for x in range(list_length-sequence_length):
                if guesses_in[start_range:end_range+1] == sequence and len(guesses_in) > end_range + 1 + lag:  # we go over the list of the guesses and look for matches, then add any matches to a new list
                    distance_from_end = list_length - end_range
                    next_guesses.append([sequence, guesses_in[end_range+1+lag], distance_from_end, lag])
                    found_match += 1
                start_range += 1
                end_range += 1
            if found_match < 2:
                break
            sequence_length += 1
    return next_guesses


def division_by_zero(n, d):
    return n / d if d else 0


def Get_Probabilities(input_list, weight_length, weight_lag, weight_frequency, weight_recency):
    guesses_in = input_list
    probability_list = []
    processed_data = GetSequences(guesses_in)
    setz = sorted(set(guesses_in))
    setz = list(setz)
    for z in setz:
        probability_list.append([z])
    probability_list = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    for sub_list in processed_data:
        counter = 0
        if len(sub_list) > 1:  # Generates a likelyhood predictions score for the next number
            length_multiplier = len(sub_list[0]) * weight_length
            lag = int(sub_list[-1])
            lag_weight = weight_lag * (lag+1)
            next_number = int(sub_list[-3])
            frequency_bias = int(guesses_in.count(str(next_number))) * weight_frequency
            recencey_bias = int(sub_list[-2]) * weight_recency
            result_matches = (frequency_bias) + (recencey_bias) + (lag_weight) + (length_multiplier)
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


simul_right = 1
simul_wrong = 1
"""for h in range(1, len(tester) - 1):
    predicted_number = Get_Probabilities(tester[0:h],0, 22.16293647955239, 25.281980629461664, 0)
    if predicted_number is not None:  # Checks if simulation predicted the next value
        if int(predicted_number) == int(tester[h]):
            simul_right += 1
        else:
            simul_wrong += 1
    correct_ratio = simul_right / (simul_wrong + simul_right)
print("Result on testing data: ", correct_ratio)"""


def learn():
    learned_list = []  # this list stores the tested weights and their accuracy
    weight_length, weight_frequency, weight_lag, weight_recency = 1, 1, 1, 1  # starting values of weights
    correct_ratio = 0
    weight_number = 0
    step_size = 0.1
    swing_limit = 10
    total_count = 0
    while total_count < 30:
        auto_count = 0
        switch = 0
        last_prob = 0
        weight_adder = 0
        weight_list = [weight_length, weight_lag, weight_frequency, weight_recency]
        while 0 <= auto_count <= swing_limit:
            odds_improved = 0
            weight = weight_list[weight_number]
            if auto_count > 0 or switch == 1:
                weight_adder += step_size
            simul_right = 1
            simul_wrong = 1
            for n in range(5, len(guesses)): # Compare the forecast based on guesses 0:n to the actual outcome
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
                    if int(predicted_number) == int(guesses[n]):
                        simul_right += 1
                    else:
                        simul_wrong += 1
                correct_ratio = simul_right / (simul_wrong + simul_right)

            learned_list.append([correct_ratio, weight])

            if last_prob < correct_ratio:
                last_prob = correct_ratio
                auto_count = 1
                odds_improved *= 0.5
            elif correct_ratio < last_prob:
                switch += 1
                step_size = -1*step_size
                if switch > 1:
                    switch = 0
                    auto_count = -1
            else:
                auto_count += 1
            if odds_improved == 1 or auto_count == 9:
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
        if auto_count > swing_limit:
            swing_limit += -1
            step_size = step_size * 1.1
        if weight_number > 3:
            weight_number = 0

        total_count += 1
        outcome_list = [correct_ratio, last_prob, weight_frequency, weight_lag, weight_length, weight_recency]
    return outcome_list


final_correct = 0
final_incorrect = 0
counter = 0
while 1==1:
    for k in testing_data:
        print(len(guesses))
        if len(guesses) > 5:
            model_outcome = learn()
            final_guess = Get_Probabilities(testing_data[0:counter], model_outcome[-4] ,model_outcome[-3], model_outcome[-2], model_outcome[-1])
        else:
            final_guess = random.randint(1, 9)
        text_from_user = testing_data[counter+1]
        if text_from_user.isnumeric():
            if 1 <= int(text_from_user) <= 9:
                guesses.append(text_from_user)
                if int(guesses[-1]) == int(final_guess):
                    print("Hooray, I guessed correctly, you are the robot, not me!")
                    final_correct += 1
                else:
                    print("You have eluded me this time, but I will only grow stronger with each defeat!")
                    final_incorrect += 1
                if final_correct > 0 and final_incorrect > 0:
                    print("I have have guessed ", str(100* (final_correct/(final_incorrect + final_correct)))), "of your guesses so far."



