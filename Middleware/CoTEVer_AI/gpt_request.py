from statistics import mean
import os
import json
import re
import random
from Sogong_AI.utils import *


def split_question(gpt_response):
    match = re.split(r'\n',gpt_response)
    match = [context.split(":")[-1] for context in match]
    return match

class Decoder():
    def __init__(self):
        print_now()

    def decode(self, input, max_length=256, key="None",model="gpt3-code",):
        # demo = create_demo_text("./prompt/demo.txt") # create example for prompt
        # prompt = demo + input # add input to example
        prompt = input
        response = decoder_for_gpt3(prompt, max_length, key ,model,) # get response from gpt3
        print(response)
        final_output = split_question(response) # split response into questions,evidence, and answer
        return final_output




