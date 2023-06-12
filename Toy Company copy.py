"""
Created on Thu Dec 16 13:12:33 2021

@author: Amirreza Pashapour
"""
# A Set Covering Problem

from pyomo.environ import *

M = ConcreteModel()

toySet = RangeSet(2)      # Toy company set
factorySet = RangeSet(2)  # Factory set

# Fixed cost of producing toy i
fixedCost = [50000, 80000]

# Cell i-j shows the amount of production for toy i by factory j
productionRate = [[50, 40],
                  [40, 25]]

# Profit obtained by each unit of i-th toy
profit = [10, 15]

# Amount of available time for factory j
timeLimit = [500, 700]

# Large Number
B = 1000

M.y = Var(factorySet, within = Binary) # 1: if factory j is used
M.t = Var(toySet, within = Binary)     # 1: if toy i is produced
# x: number of hours used to produce toy i by factory j 
M.x = Var(toySet, factorySet, within = NonNegativeIntegers)

M.obj = Objective(expr = sum(-fixedCost[i-1]*M.t[i] for i in toySet)+
                  sum(profit[i-1]*productionRate[i-1][j-1]*M.x[i,j] for i in toySet for j in factorySet)
                  , sense = maximize)
# only 1 factory can be used
M.factoryLimit = ConstraintList()
M.factoryLimit.add(sum(M.y[j] for j in factorySet)<=1)

# xij takes value if toy i is produced by factory j
M.toyProduction = ConstraintList()
for i in toySet:
    for j in factorySet:
        M.toyProduction.add(M.x[i,j]<=B*M.y[j])
        M.toyProduction.add(M.x[i,j]<=B*M.t[i])

# Each factory has a time limit
M.timeLimit = ConstraintList()
for j in factorySet:
    M.timeLimit.add(sum(M.x[i,j] for i in toySet)<=timeLimit[j-1])

solver = SolverFactory('glpk')
solution = solver.solve(M)
display(M)