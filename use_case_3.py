EPS = 1e-10

def sign(x):
	if x < 0:
		return -1
	return 1

def px(ais, x):	# calculating polinomial by its coefficients
	if ais == []:
		return 0
	return ais[0] + x * px(ais[1:], x)

def dp(pol):	# first derivative
	i = 1
	d = []
	for ai in pol[1:]:
		d += [ai * i]
		i += 1
	return d

def root_ab(fx, a, b):	# finds [root] in monotonic (a, b) if there is one, [] elsewise
	c = (a + b) / 2.0
	if sign( fx(a) ) == sign( fx(b) ):	# no root in (a, b)
		return []
	if abs( fx(c) ) < EPS:	# ok to be considered root
		return [c]
	if sign( fx(c) ) != sign( fx(a) ):	# left half
		return root_ab(fx, a, c)
	if sign( fx(c) ) != sign( fx(b) ):	# right half
		return root_ab(fx, c, b)

def root_a(fx, a, d):	# finds root in monotonic (a, inf) d>0 or (-inf, a) d<0, if there is one
	if sign( fx(a+d) - fx(a) ) == sign( fx(a) ):
		return []	# no root
	if sign( fx(a+d) ) != sign( fx(a) ):
		return root_ab(fx, a, a+d)	# there is a root in (a, a+d)
	return root_a(fx, a+d, d*2)	# we need a bigger d


def find_single_root(pol):
	return root_a(lambda x: px(pol, x), 0, -1.0) + root_a(lambda x: px(pol, x), 0, 1.0)

def pol_roots(pol):
	if len(pol) == 2:	# ax + b = 0 
		return [-pol[0] / pol[1]]
	dp_roots = pol_roots( dp(pol) )
	if dp_roots == []:
		return find_single_root(pol)
	return pol_root_l(pol, dp_roots)

def pol_root_l(pol, xs):
	on_inf_x1 = root_a(lambda x: px(pol, x), xs[0], -1.0) # root on (-inf, x0)
	return on_inf_x1 + pol_root_r(pol, xs)

def pol_root_r(pol, xs):
	if len( xs ) == 1:
		return root_a(lambda x: px(pol, x), xs[0], 1.0) # root in (xn, inf)
	on_a_b = root_ab(lambda x: px(pol, x), xs[0], xs[1]) # root in (xi, xi+1)
	return on_a_b + pol_root_r(pol, xs[1:])


if __name__ == "__main__":
	pol1 = [-2.0, 0.0, 1.0]
	pol2 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
	pol3 = [23.0, -54.0, 23.0, -12.0, 1.0]
	# graphics
	from html_bitmap import *
	bmp1 = new_bitmap(500, 500)
	bmp2 = new_bitmap(500, 500)
	bmp3 = new_bitmap(500, 500)
	
	SCALE = 100.0

	def x_to_sx( x ):
		return x * SCALE + 250

	def y_to_sy( y ):
		return 250 - (y * SCALE)

	def sx_to_x( sx ):
		return (sx - 250) / SCALE
		
	def orths_on( bmp ):
		line_on(bmp, 0,250, 500,250, col = '#000', width = 1)
		line_on(bmp, 250,0, 250,500, col = '#000', width = 1)
		line_on(bmp, x_to_sx(0.03), y_to_sy(1), x_to_sx(-0.03), y_to_sy(1), col = '#000', width = 1)
		line_on(bmp, x_to_sx(1), y_to_sy(0.03), x_to_sx(1), y_to_sy(-0.03), col = '#000', width = 1)

	orths_on( bmp1 )
	orths_on( bmp2 )
	orths_on( bmp3 )

	for i in range(1,500):
		line_on(bmp1, i, y_to_sy( px(pol1, sx_to_x(i)) ), i-1, y_to_sy( px(pol1, sx_to_x(i-1)) ), '#700')
		line_on(bmp2, i, y_to_sy( px(pol2, sx_to_x(i)) ), i-1, y_to_sy( px(pol2, sx_to_x(i-1)) ), '#060')
		line_on(bmp3, i, y_to_sy( px(pol3, sx_to_x(i)) ), i-1, y_to_sy( px(pol3, sx_to_x(i-1)) ), '#007')

	print( to_html( bmp1 ) )
	print( pol1, pol_roots( pol1 ) )
	print( '<br>' )
	print( '<br>' )
	print( to_html( bmp2 ) )
	print( pol2, pol_roots( pol2 ) )
	print( '<br>' )
	print( '<br>' )
	print( to_html( bmp3 ) )
	print( pol3, pol_roots( pol3 ) )
	print( '<br>' )
	print( '<br>' )
