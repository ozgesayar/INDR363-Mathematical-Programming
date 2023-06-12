"""
Created on Thu Dec 16 13:12:33 2021

@author: Amirreza Pashapour
"""
# A Set Covering Problem

from pyomo.environ import *

M = ConcreteModel()

# A is the coefficient matrix
A = [[1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
     [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
     [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1],
     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
     [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
     [0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
     [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1]]

# Costs for each assignment of crew to flights
C = [2, 3, 4, 6, 7, 5, 7, 8, 9, 9, 8, 9]

nSet = len(A) # number of rows
nFlight = len(A[0]) # number of columns

Set = RangeSet(nSet)
Flight = RangeSet(nFlight)

M.x = Var(Flight, within=Binary) # 1: if a crew is assigned to flight j

M.obj = Objective(expr = sum(C[j-1]*M.x[j] for j in Flight),
                  sense = minimize)

M.set_limit = ConstraintList()

#Covering each set element at least once
for i in Set:
    M.set_limit.add(sum(A[i-1][j-1]*M.x[j] for j in Flight) >= 1)

# Only 3 crews can be assigned to flights
M.crew_limit = ConstraintList()
M.crew_limit.add(sum(M.x[j] for j in Flight)==3)

solver = SolverFactory('cplex_direct')
solution = solver.solve(M)
display(M)
print("------------------------------------------")
print("Optimal Objective Value : ", value(M.obj))
print("Chosen crew : ")
for j in Flight:
    if value(M.x[j])>0.5:
        print(j)
print("------------------------------------------")