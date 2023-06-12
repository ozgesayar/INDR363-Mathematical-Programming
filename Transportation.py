from pyomo.environ import *

M = ConcreteModel()

# Item range
supplySet = ['A','B','C']
demandSet = ['M','N','O','P']

# Parameters
Cost = {('A','M'):34,('A','N'):13,('A','O'):17,('A','P'):14,
        ('B','M'):16,('B','N'): 8,('B','O'):14,('B','P'):10,
        ('C','M'):21,('C','N'):14,('C','O'):12,('C','P'): 9}

Supply = {('A'):250,('B'):300,('C'):500}
Demand = {('M'):300,('N'):150,('O'):250,('P'):250}

# Variables
M.x = Var(supplySet, demandSet, within = NonNegativeIntegers)

# Objective
M.obj = Objective(expr = sum(Cost[(i,j)]*M.x[i,j] for i in supplySet for j in demandSet),
                  sense = minimize)

# Constraints
M.supplyLimit = ConstraintList()
for i in supplySet:
    M.supplyLimit.add(sum(M.x[i,j] for j in demandSet)<=Supply[i])
M.demandLimit = ConstraintList()
for j in demandSet:
    M.demandLimit.add(sum(M.x[i,j] for i in supplySet)>=Demand[j])

solver = SolverFactory('cplex_direct')
solution = solver.solve(M)
display(M)






