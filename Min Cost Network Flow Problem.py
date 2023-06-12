# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:13:36 2021

@author: HP
"""
# MIN COXT NETWORK FLOW PROBLEM
from pyomo.environ import *

M = ConcreteModel()

#number of nodes
nNode = 11
V = range(1,nNode+1)

O = [1,2]
I = [3]
B = [4,5]
DC = [6,7,8,9,10,11]  

P = {1:30, 2: 68, 3: 20}
R = {4:220, 5:200}     
D = {6: 103, 7: 74, 8:50 , 9:60 , 10:102 , 11:13} 

# defining cost of shipment between facilities
c = {(1,4):0.026 , (1,5):0.017,
     (2,4):0.037 , (2,5):0.017,
     (3,4):0.032 , (3,5):0.033,
     (4,6):0 ,     (4,7):0.04 , (4,8):0.052 , (4,9):0.017 , (4,10):0.055 , (4,11):0.042,
     (5,6):0.032 , (5,7):0.041 , (5,8):0.039 , (5,9):0.027 , (5,10):0.023 , (5,11):0.043}                 

#amount of shipment
M.O = Var(O, B, within = NonNegativeReals)
M.I = Var(I, B, within = NonNegativeReals)
M.B = Var(B, DC, within = NonNegativeReals)

#defining objective
def obj_rule(M): return sum(c[(o,b)]*M.O[(o,b)] for o in O for b in B) + sum(c[(i,b)]*M.I[(i,b)] for i in I for b in B) + sum(c[(b,dc)]*M.B[(b,dc)] for b in B for dc in DC)
M.Objective = Objective(rule=obj_rule, sense = minimize)
        
def constraint1(M, o): return sum(M.O[(o,b)] for b in B) <= P[o]
M.Constraint1 = Constraint(O, rule = constraint1)

def constraint2(M, i): return sum(M.I[(i,b)] for b in B) <= P[i]
M.Constraint2 = Constraint(I, rule = constraint2)

def constraint3(M, b): return sum(8.333*M.O[(o,b)] for o in O) + sum(9.091*M.I[(i,b)] for i in I) <= R[b]
M.Constraint3 = Constraint(B, rule = constraint3)

def constraint4(M,dc): return sum(M.B[(b,dc)] for b in B) >= D[dc]
M.Constraint4 = Constraint(DC, rule = constraint4)

def constraint5(M,b): return sum(8.333*M.O[(o,b)] for o in O) + sum(9.091*M.I[(i,b)] for i in I) - sum(M.B[(b,dc)] for dc in DC) == 0
M.Constraint5 = Constraint(B, rule = constraint5)

M.dual = Suffix(direction=Suffix.IMPORT)
M.slack = Suffix(direction=Suffix.IMPORT)
M.rc = Suffix(direction=Suffix.IMPORT)

solver = SolverFactory('glpk')
solver.solve(M)
M.pprint()
M.display()

display(M.dual)
display(M.slack)
display(M.rc)

