from solver import Solver

import json
import math
from collections import Counter
def distance(problem, question):
    """[summary]
    Args:
        problem ([type]): [description]
        question ([type]): [description]
    Returns:
        [type]: [description]
    """

    a,b = list(problem), list(question)
    r = [2]*5
    for i in range(5):
        if a[i] == b[i]:
            r[i] = 0
            a[i] = "_"
            b[i] = "#"
    
    for i in range(5):
        for j in range(5):
            if i==j:continue
            if a[i]==b[j]:
                r[i] = 1
                a[i] = "_"
                b[j] = "#"
    
    result = tuple(r)
    return result

class EntropySolver(Solver):
    def __init__(self, problems, questions):
        n = len(problems)
        m = len(questions)

        reverse_dict = {}
        subset_dict_list = [{} for _ in range(m)]

        for i in range(n):
            question = questions[i]
            reverse_dict[question] = i
            for j in range(m):
                problem = problems[j]
                d = distance(problem,question)
                if d in subset_dict_list[i]:
                    subset_dict_list[i][d].append(j)
                else:
                    subset_dict_list[i][d] = [j]
        
        for subset_dict in subset_dict_list:
            for k,v in subset_dict.items():
                subset_dict[k] = set(v)

        self.subset_dict_list = subset_dict_list
        self.n = n
        self.m = m
        self.questions = questions
        self.reverse_dict = reverse_dict

        self.candidates = set(range(n))


    def get_entropy(self, id):
        eventset = set(self.candidates)
        n = len(eventset)
        entropy = 0
        for subset in self.subset_dict_list[id].values():
            #joint probability
            jointset = subset & eventset
            k = len(jointset)
            p = k/n
            if p==0:continue
            entropy += p*math.log2(p)
        entropy = -entropy
        return entropy

    def get_entropy_byname(self, name):
        id = self.reverse_dict[name]
        return self.get_entropy(id,eventset)

    def get_informationcontent(self, id, respond):
        eventset = set(self.candidates)
        n = len(eventset)
        subset = self.get_subset(id,respond)
        jointset = subset & eventset
        k = len(jointset)
        p = k/n
        entropy = 0
        if p!=0:
            entropy = -math.log2(p)
        return entropy

    def get_informationcontent_byname(self, name, respond, eventset=None):
        id = self.reverse_dict[name]
        return self.get_informationcontent(id, respond)

    def get_subset(self, id, respond):
        return self.subset_dict_list[id][respond]
    
    def get_subset_byname(self, name, respond):
        return self.get_subset(self.reverse_dict[name], respond)

    def question(self) -> str:
        if len(self.candidates)==1:
            i = list(self.candidates)[0]
            return self.questions[i]
        lst = []
        for i in range(self.m):
            eta = self.get_entropy(i), self.questions[i]
            lst.append(eta)
        _, query = max(lst)
        return query

    def response(self, question:str, r1: int, r2: int, r3: int, r4: int, r5: int) -> None:
        r = (r1, r2, r3, r4, r5)
        self.candidates = self.candidates & self.get_subset_byname(question, r)
        #print(question, r, len(self.candidates))
        return

    def reset(self) -> None:
        self.candidates = set(range(self.n))
        return