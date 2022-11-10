from eval import Evaluator
from entropysolver import EntropySolver

import json

def main():
    msg = '###Wordle Evaluator###'
    print(msg)
    
    names = []
    with open("./names.json",encoding="utf-8") as js:
        names.extend(json.load(js))


    evaler = Evaluator(set(names), set(names))
    solver = EntropySolver()
    
    #evaler.check_solver(solver)
    evaler.evalualte(solver)

    
if __name__ == "__main__":
    main()