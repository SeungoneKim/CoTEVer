from Sogong_AI.speedup import *
import time

with open("speedup_input.json", "r") as read_file:
    input_dict = json.load(read_file)

gogo = SpeedyPipeline(
)
start = time.time()
gogo.process_one(input_dict)
end = time.time()
print(f"It took: {end-start}")