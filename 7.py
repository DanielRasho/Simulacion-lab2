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

f = lambda x : x**3 - 2 * x + 2
df = lambda x : 3 * x**2 - 2
tol = 1e-7

print("NEWTON \n")
newton(f, df, 0, 10, tol)