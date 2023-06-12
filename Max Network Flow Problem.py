# MAX NETWORK FLOW PROBLEM
from pyomo.environ import *

M = ConcreteModel()

nNode = 6
V = RangeSet(nNode)
A = [(1,2),(1,3),(1,4),
     (2,5),
     (3,4),(3,6),
     (4,2),(4,6),
     (5,4),(5,6),
     (6,1)]

u = {(1,2):3,(1,3):3,(1,4):2,
     (2,5):4,
     (3,4):1,(3,6):2,
     (4,2):1,(4,6):2,
     (5,4):1,(5,6):1,
     (6,1):100}

M.x = Var(A, within = NonNegativeReals)

M.obj = Objective(expr = M.x[(6,1)], sense = maximize)

M.flowBalance = ConstraintList()
for i in V:    #incoming = outgoing
    M.flowBalance.add(sum(M.x[(j,i)] for j in V if (j,i) in A) ==
                      sum(M.x[(i,k)] for k in V if (i,k) in A))

M.flowLimit = ConstraintList()
for a in A:    # Upper limits
    M.flowBalance.add(M.x[a]<=u[a])

solver = SolverFactory('cplex')
solution = solver.solve(M)
display(M)
print(value(M.obj))