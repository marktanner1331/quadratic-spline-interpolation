from sympy import *
import numpy as np
import matplotlib.pyplot as plt

points = np.array([[0, 0.1], [0.5, 0.2], [1, 1], [1.5, 0.5], [2, 1]])
n = len(points) - 1

x, y = symbols('x, y')
a = symbols('a1:%d'%(n+1))
b = symbols('b1:%d'%(n+1))
c = symbols('c1:%d'%(n+1))

f = [a[i]*x**2 + b[i]*x + c[i] - y for i in range(n)]

equations = []
equations.append(f[0].subs(x, points[0, 0]).subs(y, points[0, 1]))

for i in range(n - 1):
    equations.append(f[i].subs(x, points[i + 1, 0]).subs(y, points[i + 1, 1]))
    equations.append(f[i + 1].subs(x, points[i + 1, 0]).subs(y, points[i + 1, 1]))

equations.append(f[-1].subs(x, points[-1, 0]).subs(y, points[-1, 1]))

fdx = [diff(fi, x) for fi in f]
for i in range(n - 1):
    equations.append(fdx[i].subs(x, points[i + 1, 0]) - fdx[i + 1].subs(x, points[i + 1, 0]))

# equations.append(a[0])

solvedForA0 = solve(equations, a[1:] + b + c)
# print(latex(solvedForA0))

error = a[0]**2
for i in range(1, n):
    error += solvedForA0[a[i]]**2
error /= n

error = simplify(error)
errorDiff = diff(error, a[0])
solved = solve(equations + [errorDiff], a + b + c)


plt.scatter(points[:, 0], points[:, 1])

# with error diff
solved = solve(equations + [errorDiff], a + b + c)
#print(solved)

for i in range(n):
    span = np.linspace(points[i, 0], points[i + 1, 0], 100)
    fi = f[i].subs(solved)
    if i == 0:
        plt.plot(span, [solve(fi.subs(x, i)) for i in span], 'b', label="mse(a)")
    else:
        plt.plot(span, [solve(fi.subs(x, i)) for i in span], 'b')

               
# with a0 = a1
solved = solve(equations + [a[0] - a[1]], a + b + c)
#[print(latex(fi.subs(solved))) for fi in f]

for i in range(n):
    span = np.linspace(points[i, 0], points[i + 1, 0], 100)
    fi = f[i].subs(solved)
    if i == 0:
        plt.plot(span, [solve(fi.subs(x, i)) for i in span], 'g', label="a0 = a1")
    else:
        plt.plot(span, [solve(fi.subs(x, i)) for i in span], 'g')


# with a0 = 0
solved = solve(equations + [a[0]], a + b + c)
#[print(latex(fi.subs(solved))) for fi in f]

for i in range(n):
    span = np.linspace(points[i, 0], points[i + 1, 0], 100)
    fi = f[i].subs(solved)
    if i == 0:
        plt.plot(span, [solve(fi.subs(x, i)) for i in span], 'r', label="a0 = 0")
    else:
        plt.plot(span, [solve(fi.subs(x, i)) for i in span], 'r')
    
plt.grid()
plt.legend()
plt.show()
