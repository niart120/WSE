from typing import Set,List,Dict,Tuple
import random
import secrets

from solver import Solver

def _show_result(result_dict:Dict)->None:
    score = sum(result_dict.values())
    print(f"Solver score:{sum(result_dict.values())}")
    k,v = max(result_dict.items(),key=lambda x:x[1])
    print(f"Worst case:{k}({v} steps)")

class Evaluator():
    def __init__(self, problem_space:Set[str], question_space:Set[str]) -> None:
        self.problems = set(problem_space)
        self.questions = set(question_space)

    def check_solver(self, solver:Solver):
        solver.reset()
        testcase = self.make_testcase()
        result_dict = {}
        for t in testcase:
            result_dict[t] = 0
        
        for t in testcase:
            print(f"answer:{t}")
            score = self._eval(t,solver)
            result_dict[t] = score
            solver.reset()
        
        for k, v in result_dict.items():
            print(f"name:{k}, score:{v}")
        

    def evalualte(self, solver:Solver, show_result:bool = True)->int:
        #ソルバの初期化
        solver.reset()

        # 問題リストの作成
        problems_list = self.make_problem_list()
        result_dict = {}
        for p in self.problems:
            result_dict[p] = 0

        for p in problems_list:
            # 出題と評価
            try:
                score = self._eval(p, solver)
            #評価中に例外を送出した場合はペナルティ
            except:
                score = 20
            # 評価値の更新
            result_dict[p] = max(result_dict[p],score)
            solver.reset()

        if show_result:
            _show_result(result_dict)
        
        # ソルバのスコア:problems_listの各要素に対する最悪評価値の総和
        result = sum(result_dict.values())
        
        return result
    
    def _eval(self, p:str, solver:Solver):
        for i in range(1,11):
            q = solver.question()
            #質問可能な文字列か判定
            if q in self.questions:
                r = Evaluator._compare(p, q)
                #質問内容と比較結果をソルバに渡す
                solver.response(q, *r)
                #正解時の処理
                if p == q:
                    #スコアを返す
                    return i
            #そうでない場合は例外を投げる
            else:
                raise ValueError(q)
                
        #制限質問数以内に回答出来なかった場合ペナルティスコアを返す
        return 20

    def _compare(problem:str, question:str)->Tuple[int]:
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
                    r[j] = 1
                    a[i] = "_"
                    b[j] = "#"
        
        result = tuple(r)
        return result

    def make_problem_list(self, multiplier:int = 2)->List[str]:
        #Notice:seedingが内部的にハッシュ関数などを噛ませて32bitで行われてる場合は攻撃可能
        # 乱数生成器の初期化
        random.seed(secrets.randbits(128))
        # 問題リストは問題空間の任意の要素を少なくとも一つ持つ
        problems_list = list(self.problems)
        # 追加する問題のサンプリング
        additional = random.choices(problems_list,k=len(problems_list)*(multiplier-1))
        # 問題リストと結合
        problems_list.extend(additional)
        # 乱数生成器を再度初期化
        random.seed(secrets.randbits(128))
        # シャッフル
        problems_list = random.sample(problems_list,len(problems_list))
        return problems_list

    def make_testcase(self)->List[str]:
        random.seed(secrets.randbits(128))
        testcase = random.sample(list(self.problems), min(10, len(self.problems)))
        return testcase