from Professor import Professor 
import copy
class Individuo :
    def __init__(self, professores):
        self.aptidao = 0
        self.professores = copy.deepcopy(professores)
    
    def fitnessEvaluation (self, turmas):
        self.aptidao = 7000
        for i in range (len(self.professores[0].grade)) : 
            count = [0 for i in range (turmas)]
            for j in range (len(self.professores)):
                num = self.professores[j].grade[i]

                if num > 0 :
                    count [ num - 1 ]  += 1 
                
                for posicao in count :
                    self.aptidao -= abs((posicao - 1) * 50)