# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:39:47 2021

@author: HP
"""

# MIN COXT NETWORK FLOW PROBLEM
from pyomo.environ import *

M = ConcreteModel()

#number of nodes
nNode = 14
V = range(1,nNode+1)

O = [1,2]
I = [3]
B = [4,5,12,13,14] 
#12 = potential brewery in İzmir
#13 = potential brewery in Sakarya
#14 = potential brewery in Adana
DC = [6,7,8,9,10,11]  

P = {1:30, 2: 68, 3: 20} #plant capacities
R = { 4:220, 5:200, 12:70, 13:70, 14:70 }  #brewery capacities
A = { 4:0 , 5:0, 12:50, 13:50, 14:50}    #added capacity as a result of the expansion

#annual demand of the distribution centers
D = { (1,6):103 , (1,7):74 , (1,8):50 , (1,9):60 , (1,10):102 , (1,11):13 ,
      (2,6):110 , (2,7):80 , (2,8):53 , (2,9):75 , (2,10):110 , (2,11):13 ,
      (3,6):125 , (3,7):90 , (3,8):60 , (3,9):85 , (3,10):125 , (3,11):15 } 


#cost of opening a new facility
CN = { 4:0 , 5:0 , 12:75 , 13:70 , 14:68 }

#cost of expanding the facility
CE = { 4:1000000000 , 5:1000000000 , 12:30 , 13:27 , 14:25 }

# defining cost of shipment between facilities
c = {(1,4):0.026 , (1,5):0.017, (1,12):0.002 , (1,13):0.019 , (1,14):0.032 ,
     (2,4):0.037 , (2,5):0.017, (2,12):0.031  , (2,13):0.03  , (2,14):0.022 ,
     (3,4):0.032 , (3,5):0.033, (3,12):0.004  , (3,13):0.028 , (3,14):0.048 ,
     (4,6):0 ,     (4,7):0.04 , (4,8):0.052 , (4,9):0.017 , (4,10):0.055 , (4,11):0.042,
     (5,6):0.032 , (5,7):0.041 , (5,8):0.039 , (5,9):0.027 , (5,10):0.023 , (5,11):0.043,
     (12,6):0.04 , (12,7):0 , (12,8): 0.032 , (12,9): 0.023 , (12,10):0.062 , (12,11):0.002 , 
     (13,6):0.011 , (13,7):0.034 , (13,8):0.041 , (13,9):0.011 , (13,10): 0.045 , (13,11):0.036,
     (14,6):0.067 , (14,7):0.064 , (14,8):0.04 , (14,9):0.06 , (14,10):0.024 , (14,11):0.066 }                 


years = range(1,21)

first_part = [1,2,3]
second_part = range(4,21)

#amount of shipment
M.O = Var(O, B, years, within = NonNegativeReals)
M.I = Var(I, B, years, within = NonNegativeReals)
M.B = Var(B, DC, years, within = NonNegativeReals)
M.BN = Var(B, first_part , within = Binary)
M.BE = Var(B, first_part , within = Binary)


discounting_factor = {}
opportunity_cost = 0.1

for y in years: 
 discounting_factor[y] = 1/pow(1 + opportunity_cost, y - 1)
 
 
#defining the objective function
def obj_rule(M): return sum(c[(o,b)]*M.O[(o,b,y)]*discounting_factor[y] for o in O for b in B for y in first_part) + sum(c[(i,b)]*M.I[(i,b,y)]*discounting_factor[y] for i in I for b in B for y in first_part) + sum(c[(b,dc)]*M.B[(b,dc,y)]*discounting_factor[y] for b in B for dc in DC for y in first_part) + sum(c[(b,dc)]*M.B[(b,dc,3)]*discounting_factor[y] for b in B for dc in DC for y in second_part) + sum(c[(o,b)]*M.O[(o,b,3)]*discounting_factor[y] for o in O for b in B for y in second_part) + sum(c[(i,b)]*M.I[(i,b,3)]*discounting_factor[y] for i in I for b in B for y in second_part) + sum(CN[b]*M.BN[(b, y)]*discounting_factor[y] for b in B for y in first_part) + sum(CE[b]*M.BE[(b, y)]*discounting_factor[y] for b in B for y in first_part)
M.Objective = Objective(rule=obj_rule, sense = minimize)
        
def constraint1(M, o, y): return sum(M.O[(o,b,y)] for b in B ) <= P[o]
M.Constraint1 = Constraint(O, years, rule = constraint1)

def constraint2(M, i, y): return sum(M.I[(i,b,y)] for b in B ) <= P[i]
M.Constraint2 = Constraint(I, years, rule = constraint2)

def constraint3(M, b, y): return sum(8.333*M.O[(o,b,y)] for o in O ) + sum(9.091*M.I[(i,b,y)] for i in I ) - sum( R[b]*M.BN[(b, n)] for n in range(1,y+1) ) - sum( A[b]*M.BE[(b, n)] for n in range(1,y+1) )  <= 0
M.Constraint3 = Constraint(B, first_part , rule = constraint3)

def constraint13(M, b, y): return sum(8.333*M.O[(o,b,y)] for o in O ) + sum(9.091*M.I[(i,b,y)] for i in I ) - R[b]*sum( M.BN[(b, n)] for n in first_part ) - A[b]*sum( M.BE[(b, n)] for n in first_part )  <= 0
M.Constraint13 = Constraint(B, second_part, rule = constraint13)

def constraint4(M, dc, y): return sum(M.B[(b,dc,y)] for b in B) >= D[(y, dc)]
M.Constraint4 = Constraint(DC, first_part , rule = constraint4)

def constraint14(M, dc, y): return sum(M.B[(b,dc,y)] for b in B) >= D[(3, dc)]
M.Constraint14 = Constraint(DC, second_part , rule = constraint14)

def constraint5(M, b, y): return sum(8.333*M.O[(o,b,y)] for o in O) + sum(9.091*M.I[(i,b,y)] for i in I) - sum(M.B[(b,dc,y)] for dc in DC) == 0
M.Constraint5 = Constraint(B, years, rule = constraint5)

def constraint6(M, b, y): return sum(M.BN[(b, n)] for n in range(1,y+1) ) >= M.BE[(b, y)]
M.Constraint6 = Constraint(B, first_part, rule = constraint6)

def constraint7(M, b): return sum(M.BN[(b, y)] for y in first_part ) <= 1
M.Constraint7 = Constraint(B, rule = constraint7)

def constraint8(M, b): return sum(M.BE[(b, y)] for y in first_part ) <= 1
M.Constraint8 = Constraint(B, rule = constraint8)

def constraint9(M): return M.BN[(4, 1)] == 1
M.Constraint9 = Constraint(rule = constraint9)

def constraint10(M): return M.BN[(5, 1)] == 1
M.Constraint10 = Constraint(rule = constraint10)

def constraint11(M, y): return M.BE[(4, y)] == 0
M.Constraint11 = Constraint(first_part, rule = constraint11)

def constraint12(M, y): return M.BE[(5, y)] == 0
M.Constraint12 = Constraint(first_part, rule = constraint12)


#solver = SolverFactory('glpk')
#solver.solve(M)
#M.pprint()
#M.display()

solver = SolverFactory('cplex_direct')
solution = solver.solve(M)
M.display()