#!/usr/bin/env python
import random
import simpleSat
import sys
import argparse

class Generator():
    def __init__(self):        
        args = self.getArgs()
        self.gamma = args.gamma
        self.nVariables = args.nvariables
        self.nClauses = args.nclauses
        self.length = args.length
        self.distribution = args.distribution
        self.dictionary = {
            "uniform":(self.uniformRandomGamma,(self.length,self.nVariables,self.nClauses,self.gamma)),
            "neighborhood":(self.uniformRandomGamma,(self.length,self.nVariables,self.nClauses,self.gamma)),
            "power":(self.uniformRandomGamma,(self.length,self.nVariables,self.nClauses,self.gamma))
        }
        
    def getArgs(self):
        parser = argparse.ArgumentParser(description='Generate a sat problem.')
        parser.add_argument('--gamma','-g', default=None, type=float, help='Gamma')
        parser.add_argument('--nvariables','-nv', default=30, type=int, help='Number of variables')
        parser.add_argument('--nclauses','-nc', default=129, type=int, help='Number of Clauses')
        parser.add_argument('--length','-l', default=3, type=int, help='Clause length')
        parser.add_argument('--descriptive','-d', action='store_const', const=True, default=False, help='Descriptive mode')
        parser.add_argument('--distribution','-dist', default="uniform", type=str, choices=["uniform","neighborhood","power"], help='Distribution type (Uniform random, neighborhood, or power law)')
        args = parser.parse_args()
        return args
        
    def generate(self):
        return self.dictionary[self.distribution][0](*self.dictionary[self.distribution][1])  #Looks up the word, calls the corresponding function with corresponding parameters. '*' unpacks tuple into arguments
        
    def uniformRandom(self, length, nClauses, nVariables):
        variablePool = [(x + 1) for x in range(nVariables)]
        signs = [-1,1]
        return simpleSat.Sat([simpleSat.Clause([(random.choice(variablePool) * random.choice(signs)) for x in range(length)]) for x in range(nClauses)])
        
    def uniformRandomGamma(self, length, nVariables, nClauses, gamma=None):
        variablePool = [(x + 1) for x in range(nVariables)]
        if gamma:
            nClauses = int(round(gamma*nVariables))
        signs = [-1,1]
        return simpleSat.Sat([simpleSat.Clause([(random.choice(variablePool) * random.choice(signs)) for x in range(length)]) for x in range(nClauses)])
        
    def parseText(self, clauseList):
        return simpleSat.Sat([simpleSat.Clause(eval(clauseText.lstrip("c"))) for clauseText in clauseList])
        
if __name__ == "__main__":
    generator = Generator()
    print(generator.generate())
