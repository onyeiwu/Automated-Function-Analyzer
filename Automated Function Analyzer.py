import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import fsolve

# Prompt the user to input a function
user_input = input("Enter a function in terms of x (e.g., x**3 - 9*x**2 + 26*x - 27): ")

# Define the symbolic variable and function
x = sp.symbols('x')
eqn_sympy = sp.sympify(user_input)  # Convert user input to symbolic expression

# Compute first and second derivatives
first_derivative = sp.diff(eqn_sympy, x)
second_derivative = sp.diff(first_derivative, x)

# Convert symbolic expressions to functions for computation
eqn = sp.lambdify(x, eqn_sympy, "numpy")
first_eqn = sp.lambdify(x, first_derivative, "numpy")
second_eqn = sp.lambdify(x, second_derivative, "numpy")

# Solve f'(x) = 0 for turning points
turning_points = fsolve(first_eqn, [-1, 2])  # Initial guesses

# Identify and classify the nature of the turning points
for x_t in turning_points:
    second_derivative_value = second_eqn(x_t)
    if second_derivative_value > 0:
        classification = "Minimum"
    elif second_derivative_value < 0:
        classification = "Maximum"
    else:
        classification = "Inflection Point"
    print(f"Turning point at x = {x_t:.2f} is a {classification}")

# Solve f''(x) = 0 for inflection points
inflection_points = fsolve(second_eqn, [0])  # Initial guess near 0

# Generate x values for plotting
x_vals = np.linspace(-2, 4, 1000)
y_vals = eqn(x_vals)

# Plot the function
plt.figure(figsize=(10, 6), dpi=300)
plt.plot(x_vals, y_vals, label=rf'$f(x) = {user_input}$', color='blue')

# Mark turning points
for x_t in turning_points:
    y_t = eqn(x_t)
    second_derivative_value = second_eqn(x_t)
    color = 'green' if second_derivative_value > 0 else "red"  # Red for max, green for min
    label = "Min" if second_derivative_value > 0 else "Max"
    plt.scatter(x_t, y_t, color=color, s=100, label=f'{label} at $x = {x_t:.2f}$')
    plt.axvline(x_t, color=color, linestyle="--", alpha=0.5)
    plt.axhline(y_t, color=color, linestyle="--", alpha=0.5)

# Mark inflection points
for x_inf in inflection_points:
    y_inf = eqn(x_inf)
    plt.scatter(x_inf, y_inf, color="purple", s=100, label=f'Inflection at $x = {x_inf:.2f}$')
    plt.axvline(x_inf, color="purple", linestyle="--", alpha=0.5)

# Labels and formatting
plt.title(f"Turning Points of $f(x) = {user_input}$")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.legend(loc="right")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()
