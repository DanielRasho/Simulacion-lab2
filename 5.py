def biseccion(f, interval, maxIter, tolerance):
    x0, x1 = interval

    for i in range(maxIter):
        new_x = (x0 + x1) / 2
        new_y = f(new_x)

        #print(f"Iter {i}: x = {new_x}, f(x) = {new_y}")
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
        # print(f"Iter {i}: x = {x}, f(x) = {f_x}, df(x) = {df_x}, next_x = {next_x}")

        if abs(next_x - x) < tolerance or abs(f_x) < tolerance:
            return next_x

        x = next_x

    print("Method did not converge.")
    return x

def add_root_if_new(roots, root, tolerance):
    if root is not None and all(abs(root - r) > tolerance for r in roots):
        roots.append(root)

def find_all_roots_bisection(f, interval, steps, maxIter=100, tolerance=1e-6):
    x_start, x_end = interval
    step_size = (x_end - x_start) / steps
    roots = []

    for i in range(steps):
        x0 = x_start + i * step_size
        x1 = x0 + step_size
        y0 = f(x0)
        y1 = f(x1)

        if y0 * y1 <= 0:  # sign change or exactly zero
            root = biseccion(f, (x0, x1), maxIter, tolerance)
            if all(abs(root - r) > tolerance for r in roots):  # avoid duplicates
                roots.append(root)

    return roots

def find_all_roots_secant(f, interval, steps, maxIter=100, tolerance=1e-6):
    x_start, x_end = interval
    step_size = (x_end - x_start) / steps
    roots = []

    for i in range(steps):
        x0 = x_start + i * step_size
        x1 = x0 + step_size
        y0 = f(x0)
        y1 = f(x1)

        if y0 * y1 <= 0:  # likely a sign change
            root = secant(f, (x0, x1), maxIter, tolerance)
            add_root_if_new(roots, root, tolerance)

    return roots

def find_all_roots_newton(f, df, interval, steps, maxIter=100, tolerance=1e-6):
    x_start, x_end = interval
    step_size = (x_end - x_start) / steps
    roots = []

    for i in range(steps):
        x0 = x_start + i * step_size
        root = newton(f, df, x0, maxIter, tolerance)
        add_root_if_new(roots, root, tolerance)

    return roots

f = lambda x : x**2 + (1 / (x - 7))
df = lambda x : 2*x - 1/((x-7)**2)
tol = 1e-7

print("bisection roots:", find_all_roots_bisection(f, (-1 , 1), steps=100, tolerance=tol))
print("Secant roots:", find_all_roots_secant(f, (-1 , 1), steps=100, tolerance=tol))
print("Newton roots:", find_all_roots_newton(f, df, (-1 , 1), steps=100, tolerance=tol))