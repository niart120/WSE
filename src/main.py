from eval import Evaluator
from entropysolver import EntropySolver

import json

def main():
    msg = '###Wordle Evaluator###'
    print(msg)
    
    questions = []
    problems = []

    with open("./questions.json",encoding="utf-8") as js:
        questions.extend(json.load(js))
    with open("./problems.json",encoding="utf-8") as js:
        problems.extend(json.load(js))

    questions = problems

    evaler = Evaluator(set(problems), set(questions))
    solver = EntropySolver(problems, questions)
    
    #evaler.check_solver(solver)
    evaler.evalualte(solver)

    
if __name__ == "__main__":
    main()