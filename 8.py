#!/usr/bin/env python3

import pulp as p
import math as m
import sympy as sp


def addVectors(v1: list[float], v2: list[float]) -> list[float]:
    return [v1[i] + v2[i] for i in range(len(v1))]


def multVector(v: list[float], k: float) -> list[float]:
    return [i * k for i in v]


def getHipotenuse(v: list[float]) -> float:
    return m.sqrt(sum([i**2 for i in v]))


def evalVector(system: list[any], inputs: list[float]) -> list[float]:
    output = []
    for f in system:
        output.append(f(*inputs))

    return output


def evalMatrix(system: list[list[any]], inputs: list[float]) -> list[list[float]]:
    output = []
    inps = {f"x{i}": inputs[i] for i in range(len(inputs))}
    for row in system:
        rowOutput = []
        for cell in row:
            cel = cell.subs(inps)
            rowOutput.append(cel)
        output.append(rowOutput)

    return output


def deriveSystem(system: list[any], variables: list[any]) -> list[list[any]]:
    outMatrix = []
    for f in system:
        outRow = []
        for var in variables:
            der = sp.diff(f, var)
            outRow.append(der)

        outMatrix.append(outRow)
    return outMatrix


def solveForVariable(J_X, R, varCount: int, tolerance) -> list[float]:
    y = p.LpVariable.dict("ys", range(varCount))
    problem = p.LpProblem("subproblema", sense=p.LpMaximize)
    print("R", R)

    for i in range(varCount):
        iterAdd = [J_X[i][j] * y[i] for j in range(varCount)]
        print(iterAdd, "==", R[i])
        problem += p.lpSum(iterAdd) == R[i]

    # problem += p.lpSum([y[i] for i in range(varCount)]) >= tolerance

    problem += p.lpSum([y[i] for i in range(varCount)])
    status = problem.solve()

    return [p.value(y[i]) for i in range(varCount)]


def solve(
    varCount: int,
    system: list[any],
    initialAprox: list[float],
    tolerance: float = 1e-7,
    maxIter: int = 100,
) -> (list[list[float]], list[float], bool, int):
    vars = [sp.symbols(f"x{x}") for x in range(varCount)]
    print("VARS", vars)
    expr = [f(*vars) for f in system]

    X = initialAprox
    approxs = [X]
    for i in range(maxIter):
        print("Computing F_X...", system, X)
        F_X = evalVector(system, X)
        print("Computing J...", expr, vars)
        J = deriveSystem(expr, vars)
        print("Computing J_X...", J, X)
        J_X = evalMatrix(J, X)
        print("J_X", J_X)

        print("Solving for J_X y = -F_X...", F_X)
        Y = solveForVariable(J_X, multVector(F_X, -1), varCount, tolerance)
        print("Y is", Y)
        X = addVectors(X, Y)
        print("NEW X IS", X)
        approxs.append(X)
        print("Hipo", getHipotenuse(Y), "<=", tolerance)
        if getHipotenuse(Y) <= tolerance:
            return approxs, X, False, i

    return approxs, X, True, maxIter


aproximations, final, reachedLimit, iterations = solve(
    3,
    [
        lambda x, y, z: 3 * x - sp.cos(y * z) - 0.5,
        lambda x, y, z: x**2 - 81 * (y + 0.1) ** 2 + sp.sin(z) + 1.06,
        lambda x, y, z: sp.exp(-x * y) + 20 * z + (10 * m.pi - 3) / 3,
    ],
    initialAprox=[-0.5, 1.06, (10 * m.pi - 3) / 3],
    tolerance=1e-7,
    maxIter=100,
)

if reachedLimit:
    print("LIMIT REACHED!")

print(f"FOUND WITH {iterations} ITERATIONS")
print("Approximations:")
for app in aproximations:
    print("*", app)

print("FINAL RESULT:")
print(final)
