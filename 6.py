def biseccion(f, interval, maxIter, tolerance):
    x0, x1 = interval

    for i in range(maxIter):
        new_x = (x0 + x1) / 2
        new_y = f(new_x)

        print(f"Iter {i}: x = {new_x}, f(x) = {new_y}")

        # Stopping condition
        if abs(new_y) < tolerance or abs(x1 - x0) < tolerance:
            return new_x

        # Decide the subinterval
        if new_y * f(x0) < 0:
            x1 = new_x
        else:
            x0 = new_x

    print("Method did not converge.")
    return (x0 + x1) / 2 

def secant(f, interval, maxIter, tolerance):
    x0, x1 = interval
    f_x0 = f(x0)
    f_x1 = f(x1)

    for i in range(maxIter):
        if abs(f_x1 - f_x0) < 1e-12:  # avoid division by zero
            print("Division by nearly zero in iteration", i)
            return None

        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        if abs(x2 - x1) < tolerance:
            return x2

        x0, x1 = x1, x2
        f_x0, f_x1 = f_x1, f(x2)

    print("Method did not converge after", maxIter, "iterations")
    return None

def newton(f, df, startingPoint, maxIter, tolerance):
    x = startingPoint

    for i in range(maxIter):
        f_x = f(x)
        df_x = df(x)

        if abs(df_x) < 1e-12:
            print(f"Derivative near zero at iteration {i}, x = {x}")
            return None  # Avoid division by zero

        next_x = x - f_x / df_x

        print(f"Iter {i}: x = {x}, f(x) = {f_x}, df(x) = {df_x}, next_x = {next_x}")

        if abs(next_x - x) < tolerance or abs(f_x) < tolerance:
            return next_x

        x = next_x

    print("Method did not converge.")
    return x

f = lambda x : x
df = lambda x : x
tol = 1e-7

print("BISECCION \n")
biseccion(f, (), 40, tol)

print("SECANT \n")
secant(f, (), 40, tol)

print("NEWTON \n")
newton(f, df, 3, 40, tol)