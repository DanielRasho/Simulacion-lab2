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

def newton_with_cycle_detection(f, df, startingPoint, maxIter, tolerance, alpha=0.5):
    x = startingPoint
    history = []

    for i in range(maxIter):
        f_x = f(x)
        df_x = df(x)

        if abs(df_x) < 1e-12:
            print(f"Derivative near zero at iteration {i}, x = {x}")
            return None

        next_x = x - f_x / df_x

        print(f"Iter {i}: x = {x}, f(x) = {f_x}, df(x) = {df_x}, next_x = {next_x}")

        if abs(next_x - x) < tolerance or abs(f_x) < tolerance:
            return next_x

        for past_x in history:
            if abs(next_x - past_x) < tolerance:
                print(f"Detected cycle with x ≈ {past_x} at iteration {i}, aborting.")
                next_x += alpha

        history.append(x)
        if len(history) > 3:
            history.pop(0)

        x = next_x

    print("Method did not converge.")
    return None

f = lambda x : x**3 - 2 * x + 2
df = lambda x : 3 * x**2 - 2
tol = 1e-7

print("NEWTON \n")
print(newton(f, df, 0, 10, tol))
print(newton_with_cycle_detection(f, df, 0, 30, tol))