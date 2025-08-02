#!/usr/bin/env python3
# Una empresa necesita asignar cuatro puestos de trabajo a cuatro trabajadores. El costo de desempeñar un puesto es una
# función de las habilidades de los trabajadores. En la tabla siguiente se resume el costo de las asignaciones. El trabajador 1
# no puede tener el puesto 3, y el trabajador 3 no puede desempeñar el puesto 4. Determine la asignación óptima mediante
# programación lineal

# $50 $50  —  $20
# $70 $40 $20 $30
# $90 $30 $50  —
# $70 $20 $60 $70

longValue = 50000
costos = [
    [50, 50, longValue, 20],
    [70, 40, 20, 30],
    [90, 30, 50, longValue],
    [70, 20, 60, 70],
]

import pulp as p

problem = p.LpProblem(name="Problema_de_trabajos", sense=p.LpMinimize)

# persons = []
# for i in range(1, 4):
#     for j in range(1, 4):
#         persons.append((i, j))
# print(persons)
x = p.LpVariable.matrix("table", (range(4), range(4)), lowBound=0, upBound=1)

for i in range(4):
    problem += p.lpSum([x[i][j] for j in range(4)]) == 1
for i in range(4):
    problem += p.lpSum([x[j][i] for j in range(4)]) == 1
#
problem += x[0][3] == 0
problem += x[2][3] == 0
#
# # Función a minimizar:
# # T = x1 + x2 + x3 + x4
#
finalMatrix = [
    [costos[0][j] * x[0][j] for j in range(4)],
    [costos[1][j] * x[1][j] for j in range(4)],
    [costos[2][j] * x[2][j] for j in range(4)],
    [costos[3][j] * x[3][j] for j in range(4)],
]

problem += p.lpSum(finalMatrix)

status = problem.solve()
# print(status)

for i in range(4):
    for j in range(4):
        print(p.value(x[i][j]), end="\t")
    print()
