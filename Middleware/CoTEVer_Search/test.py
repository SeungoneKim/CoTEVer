from v2 import search
import os
import json
def main():
    with open("./tmp_input.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    tmp = search(data)
    with open(os.path.join('./', 'output_example.json'),'w',encoding="utf-8") as f:
        f.write(tmp)
main()