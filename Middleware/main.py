import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from CoTEver_Search import search_yul
from Sogong_AI import gpt_request, speedup
import math
import asyncio
import os


class Input(BaseModel):
    question: str


app = FastAPI()
my_decoder = gpt_request.Decoder()
my_summarizer = speedup.SpeedyPipeline()
demo = """
[Example 1]
Question: Do hamsters provide food for any animals?
Output:
Sub Question #0 : What type of animals are hamsters?
Sub Answer #0 : Hamsters are prey animals.
Sub Question #1 : Can prey animals be food for other animals?
Sub Answer #1 : Prey are food for predators.
Sub Question #2 : Do hamsters provide food for any animals?
Sub Answer #2 : Since hamsters are prey animals, and prey are food for predetors, hamsters provide food for some animals.
So the answer is yes.

[Example 2]
Question: Could Brooke Shields succeed at University of Pennsylvania?
Output:
Sub question #0 : What university did Brooke Shields went to?
Sub answer #0 : Brooke Shields went to Princeton University.
Sub question #1 : Did Brooke Shields succeed at Princeton University?
Sub answer #1 : At Princeton University, she got all As and Bs while pursing her bachelor's degree in French literature, meaning she had a successful school life.
Sub question #2 : How rigorous is Princeton University compared to University of Pennsylvania?
Sub answer #2 : Princeton University is about as academically rigorous as the University of Pennsylvania because they have a similar ranking according to U.S. News Rankings.
Sub question #3 : Could Brooke Shields succeed at University of Pennsylvania?
Sub answer #3 : Since University of Pennsylvania and University of Princeton are in similar circumstances, Brooke Shields has been successful in University of Princeton, Brooke Shields could also succeed at the University of Pennsylvania.
So the answer is yes.

[Example 3]
Question: Hydrogen\u2019s atomic number squared exceeds number of Spice Girls?
Output:
Sub question #0 : What is the atomic number of Hydrogen?
Sub answer #0 : Hydrogen has an atomic number of 1.
Sub question #1 : What is 1 squared?
Sub answer #1 : 1 squared is 1.
Sub question #2 : How much Spice Girls are there?
Sub answer #2 : There are 5 Spice Girls.
Sub question #3 : Hydrogen\u2019s atomic number squared exceeds number of Spice Girls?
Sub answer #3 : Since Hydrogen's atomic number squared is 1, the number of Spice Girls are 5, and 1 is smaller than 5, Hydrogen\u2019s atomic number squared is less than the number of Spice Girls.
So the answer is no.

[Example 4]
Question: Is it common to see frost during some college commencements?
Output:
Sub question #0 : When does College commencement ceremonies usually happen?
Sub answer #0 : College commencement ceremonies can happen in December, May, and June.
Sub question #1 : Does it usually frost in December?
Sub answer #1 : December is in the winter, so there can be frost.
Sub question #2 : Is it common to see frost during some college commencements?
Sub answer #2 : Since there can be frost in December and a college commencement are held in December, there could be frost at some commencements.
So the answer is yes.

[Example 5]
Question: Could a llama birth twice during War in Vietnam (1945-46)?
Output:
Sub question #0 : How long was the Vietnam war?
Sub answer #0 : The War in Vietnam was 6 months.
Sub question #1 : How long is the gestation period?
Sub answer #1 : The gestation period for a llama is 11 months.
Sub question #2 : How long does it take for a llama to birth twice?
Sub answer #2 : Since the gestation period for a llama is 11 months, and 11 times 2 is 22, it will take 22 months.
Sub question #3 : Could a llama birth twice during War in Vietnam (1945-46)?
Sub answer #3 : Since it takes 22 months for a llama to birth twice, War in Vietnam was 6 months, and 22 is bigger than 6, llama could not give birth twice during the War in Vietnam.
So the answer is no.

[Example 6]
Question: Would a pear sink in water?
Output:
Sub question #0 : What is the density of a pear?
Sub answer #0 : The density of a pear is about 0.6g/cm3.
Sub question #1 : What is the density of water?
Sub answer #1 : The density of water is 1g/cm3.
Sub question #2 : Is the density of pear smaller than water?
Sub answer #2 : Since 0.6 is smaller than 1, the density of pear is smaller than water.
Sub question #3 : If the density of an object is less than water, what happens?
Sub answer #3 : Objects less dense than water float.
Sub question #4 : Would a pear sink in water?
Sub answer #4 : Since a pear has a smaller density than water, a pear would float.
So the answer is no.

[Example 7]
Question: {}
Output:
"""


# formatting returned output from gpt-3 for search module
def formatter(input, question):
    output = {}
    output["question"] = question
    output["explanation"] = {}
    output["output"] = {}
    for index in range(math.floor(len(input)/2)):
        output["explanation"][str(index)] = {}
        output["explanation"][str(index)]["sub_question"] = input[index*2]
        output["explanation"][str(index)]["sub_answer"] = input[index*2+1]
        output["explanation"][str(index)]["evidence_document"] = {}
    output["output"]["final_answer"] = input[-1]

    return output


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.post("/test")
async def test(input: Input):
    output = formatter(my_decoder.decode(demo.format(input.question), key=os.getenv('GPT3_KEY')), input.question)
    output = await search_yul.search(output, os.getenv('GOOGLE_SEARCH_API_KEY'), os.getenv('GOOGLE_ENGINE_ID_KEY'))
    output = my_summarizer.process_one(output)

    return output


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    