#!/usr/bin/python
"""
This code is a demonstration of maping technique for non-linear programming 
with constrains forming an edged manifolds inner space. The idea is to map 
n-manifold inner space on R^n, solve an optimization task there, where it 
would be unconstrained, then map the results back on the manifold space.

Works well with multiple manifolds, allowing optimization on complexes.

For further explanation write me: akalenuk@gmail.com
"""
import math

EPS = 0.0001
ITERS = 10000

def min1(f, iters = ITERS):
    x = 0
    for i in range(iters):
        e = EPS
        if f(x) <= f(x-e) and f(x) <= f(x+e):
            return x
        if f(x-e) < f(x+e):
            e = -e
        while f(x+2*e) < f(x+e):
            e*=2
        x = x+e
    raise Exception('min', 'Local minimum not found in ' + str(iters) + ' iterations')

    
def minn(f, n, iters = ITERS):
    xi = [0]*n

    def fi(i):
        return lambda x: f(*([xi[j] for j in range(i)] + [x] + [xi[j] for j in range(i+1, n)])) 
    
    for i in range(iters):
        oxi = [x for x in xi]
        for j in range(n):
            xi[j] = min1( fi(j) )
        if sum([(xi[j]-oxi[j])**2 for j in range(n)]) == 0:
            return xi

    raise Exception('minn', 'Local minimum not found in ' + str(iters) + ' iterations') 
    

def Rn_to_01(a):
    return 0.5 * (1 + math.atan(a) * 2 / math.pi)


def min_mans_n(f, mans, n):
    xs = []
    for man in mans:
        def onRn(*x):
            on_man = man(*[Rn_to_01(xi) for xi in x])
            return f(*on_man)
        x = minn(onRn, n)
        rx = man(*[Rn_to_01(xi) for xi in x])
        fx = f(*rx)
        xs += [(fx, rx)]
    return min(xs)[1]


if __name__ == "__main__":
	def f2(x, y):
		return (x-4)*(x-4) + (y-3)*(y-3)

	def manifold2_1(x, y):
		return (1.0 + 2*x - math.sin(2*y), 2*math.sin(x) + y*2)

	def manifold2_2(x, y):
		return (1.0 + 2*x - math.cos(2*y), 1 + 2*math.cos(x) + y*2)

 
	# graphics
	from html_bitmap import *
	bmp = new_bitmap(500, 500)
	

	for i in range(0, 500, 1):
		for j in range(0, 500, 1):
			f = 16*int(math.atan(f2(j/100.0, i/100.0))/math.pi * 32)
			pixel_on(bmp, j, i, to_hex(f, 0, 0))

	for i in range(0, 101, 2):
		for j in range(0, 101, 2):
			x = j/100.0
			y = i/100.0
			xy = manifold2_1(x, y)
			rx = int(xy[0]*100)
			ry = int(xy[1]*100)
			pixel_on(bmp, rx, ry, "#0ee")

			xy = manifold2_2(x, y)
			rx = int(xy[0]*100)
			ry = int(xy[1]*100)
			pixel_on(bmp, rx, ry, "#0ee")
     
    
	x = min_mans_n(f2, [manifold2_1, manifold2_2], 2)

	line_on(bmp, x[0]*100-5, x[1]*100, x[0]*100, x[1]*100, "#ee0", 2)
	line_on(bmp, x[0]*100, x[1]*100+5, x[0]*100, x[1]*100, "#ee0", 2)
	line_on(bmp, x[0]*100-15, x[1]*100+15, x[0]*100, x[1]*100, "#ee0", 2)

    
	print to_html(bmp) 

	
