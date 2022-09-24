    # Made by Sven Leidenbach

guesses, live_list = [], [],
testing_data = ["78796787768967678767987867677678978676"]
training_data = list("78796787768967678767987867677678978676")
tester = []
import time
for num in training_data:
    num = int(num)
    guesses.extend(str(num))
for num in testing_data:
    num = int(num)
    tester.extend(str(num))
print(guesses)
correct_guesses, incorrect_guesses, newcount = 1, 1, 0


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
                    next_guesses.append([sequence, guesses_in[end_range+1], distance_from_end,lag])
                    found_match += 1
                start_range += 1
                end_range += 1
            if found_match < 2:
                break
            sequence_length += 1
    return next_guesses


def Get_Probabilities(n, weight_length, weight_lag, weight_frequency, weight_recency):
    guesses_in = guesses[0:n]
    processed_data = GetSequences(guesses_in)
    probability_list = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    for sub_list in processed_data:
        counter = 0
        if len(sub_list) > 1:  # Generates a likelyhood predictions score for the next number
            length_multiplier = len(sub_list[0]) * weight_length
            lag = int(sub_list[-1])
            lag_weight = weight_lag / (lag+1)
            next_number = int(sub_list[1])
            frequency_bias = int(guesses_in.count(str(next_number))) * weight_frequency
            recencey_bias = -int(sub_list[-2]) * weight_recency
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
for h in range(5, len(tester) - 1):
    predicted_number = Get_Probabilities(h, -2.94, 3.9, 0.97, 2.13)
    if predicted_number is not None:  # Checks if simulation predicted the next value
        if int(predicted_number) == int(tester[h + 1]):
            simul_right += 1
        else:
            simul_wrong += 1
    correct_ratio = simul_right / (simul_wrong + simul_right)
print(correct_ratio)


def step_optimiser():
    learned_list = []  # this list stores the tested weights and their accuracy
    weight_length, weight_frequency, weight_lag, weight_recency = 0,0,0,0  # starting values of weights
    correct_ratio = 0
    last_prob = 0
    weight_number = 0
    step_size = 1
    anal_probe = 0
    swing_limit = 9
    while weight_number <= 5:
        auto_count = 0
        switch = 0
        last_prob = 0
        weight_adder = 0
        weight_list = [weight_length, weight_lag, weight_frequency, weight_recency]
        while 0 <= auto_count <= swing_limit:
            weight = weight_list[weight_number]
            if auto_count > 0 or switch == 1:
                weight_adder += step_size
            simul_right = 1
            simul_wrong = 1
            for n in range(5, len(guesses) - 1): # Compare the forecast based on guesses 0:n to the actual outcome
                if weight_number == 0:
                    predicted_number = Get_Probabilities(n, weight + weight_adder, weight_lag, weight_frequency,
                                                         weight_recency)
                if weight_number == 1:
                    predicted_number = Get_Probabilities(n, weight_length, weight + weight_adder, weight_frequency,
                                                         weight_recency)
                if weight_number == 2:
                    predicted_number = Get_Probabilities(n, weight_length, weight_lag, weight + weight_adder,
                                                         weight_recency)
                if weight_number == 3:
                    predicted_number = Get_Probabilities(n, weight_length, weight_lag, weight_frequency,
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

            if last_prob < correct_ratio:
                last_prob = float(learned_list[-1][0])
                auto_count = 0
                anal_probe = 1
            elif correct_ratio < last_prob:
                switch += 1
                step_size = -1*step_size
                auto_count = 0
                if switch > 1:
                    switch = 0
                    auto_count = -1
            else:
                auto_count += 1
            if correct_ratio > last_prob or auto_count == 2:
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
            step_size *= -1.01
            weight_number = 0


        print(correct_ratio,last_prob, weight_frequency, weight_lag, weight_length, weight_recency)

step_optimiser()