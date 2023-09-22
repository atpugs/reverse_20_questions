#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 15:25:33 2021

@author: anishagupta

import random
from copy import deepcopy
from akinator.async_aki import Akinator
import akinator
import asyncio

aki = Akinator()
guess = "sheep"
choices = ["yes", "no", "idk", "probably", "probably not"]
choice_prob = [0.35, 0.35, 0.1, 0.1, 0.1]

async def main():
    q = await aki.start_game()

    while aki.progression <= 80:
        a = random.choices(choices, weights=choice_prob, k=1)[0]
        print("Question: ", aki.question)
        print("Answer: ", a)
        q = await aki.answer(a)
        prev_aki = deepcopy(aki)
        prev_aki.win()
        print(prev_aki.guesses)
    await aki.win()
    
    print("I guess", aki.first_guess['name'])
    if guess in aki.first_guess['name']:
        print("Yay\n")
    else:
        print("Oof\n")
    await aki.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
"""

import random
from copy import deepcopy
import akinator

aki = akinator.Akinator()
guess = "Ariel"
choices = ["yes", "no", "idk", "probably", "probably not"]
choice_prob = [0.425, 0.425, 0.05, 0.05, 0.05]

q = aki.start_game()
prob_guess = 0
feature_count = 1

while aki.progression <= 80:
    a = random.choices(choices, weights=choice_prob, k=1)[0]
    #a = input(q + "\n\t")
    print("Question: ", aki.question)
    print("Answer: ", a)
    q = aki.answer(a)
    prev_aki = deepcopy(aki)
    prev_aki.win()
    print(prev_aki.guesses)
    for g in prev_aki.guesses:
        if g['name'] == guess:
            prob_guess += float(g['proba'])
            feature_count += 1
            break
aki.win()

print("Avg probability: ", prob_guess/feature_count)
print("I guess", aki.first_guess['name'])
if guess in aki.first_guess['name']:
    print("Yay\n")
else:
    print("Oof\n")