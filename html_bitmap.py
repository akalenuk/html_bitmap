def to_hex(r, g, b):
	if r%16==0 and g%16==0 and b%16==0:
		if r==g and r==b:
			return '#%01x' % (r/16)
		return '#%01x%01x%01x' % (r/16, g/16, b/16)
	return '#%02x%02x%02x' % (r, g, b)

def new_bitmap(w, h, col=""):
	return [[col for j in range(w)] for i in range(h)]

def pixel_on(bitmap, x, y, col=""):
	if y < len(bitmap):
		if x < len(bitmap[y]):
			bitmap[y][x] = col
			
def rect_on(bitmap, x, y, w, h, col=""):
	for i in range(y, y+h):
		for j in range(x, x+w):
			pixel_on(bitmap, j, i, col)
 
def line_on(bitmap, x1, y1, x2, y2, col="", width=1):	# Bresenham's
	points = []
	step = abs(y2-y1) > abs(x2-x1)
	if step:
		x1, y1 = y1, x1
		x2, y2 = y2, x2

	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if step:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
			
	if rev:
		points.reverse()

	for (x, y) in points:
		if width == 1:
			pixel_on(bitmap, x, y, col)
		else:
			rect_on(bitmap, x-width/2, y-width/2, width, width, col)


def circle_on(bitmap, cx, cy, r, col="", width=1):	# Bresenham's
	def circle_points_on(bitmap, x, y, cx, cy, col):
		pixel_on(bitmap, cx + x, cy + y, col)
		pixel_on(bitmap, cx - x, cy - y, col)  
		pixel_on(bitmap, cx + x, cy - y, col)
		pixel_on(bitmap, cx - x, cy + y, col)
	        if x != y:
			pixel_on(bitmap, cx + y, cy + x, col)
			pixel_on(bitmap, cx - y, cy - x, col)
			pixel_on(bitmap, cx + y, cy - x, col)
			pixel_on(bitmap, cx - y, cy + x, col) 

	x = 0
	yin = r - int(width/2)
	yout = r + int(width/2)

	din = 1 - r - int(width/2) 
	deltaEin = 3
	deltaSEin = -2*(r - int(width/2)) + 5 
	dout = 1 - r + int(width/2) 
	deltaEout = 3 
	deltaSEout = -2*(r + int(width/2)) + 5 

	for y in range(yin, yout):
		circle_points_on(bitmap, x, y, cx, cy, col)
            
	while yout > x:
		if din < 0:
			din = din + deltaEin
			deltaEin = deltaEin + 2
			deltaSEin = deltaSEin + 2
		else:
			din = din + deltaSEin
			deltaEin = deltaEin + 2
			deltaSEin = deltaSEin + 4
			yin = yin - 1
		if dout < 0:
			dout = dout + deltaEout
			deltaEout = deltaEout + 2
			deltaSEout = deltaSEout + 2
		else:
			dout = dout + deltaSEout
			deltaEout = deltaEout + 2
			deltaSEout = deltaSEout + 4
			yout = yout - 1
		x = x + 1
		for y in range(yin,yout):
			circle_points_on(bitmap, x, y, cx, cy, col)


def to_html(bitmap):
	opt_bitmap = [[(c, 1, 1) for c in cline] for cline in bitmap]
	W = len(opt_bitmap[0])
	H = len(opt_bitmap)
	for i in range( H ):
		for j in range( W ):
			(c, w, h) = opt_bitmap[i][j]
			if w < 0 or h < 0:
				continue
			dj = W - j
			for jj in range(j+1, W):
				(cj, wj, hj) = opt_bitmap[i][jj]
				if wj < 0 or hj < 0 or cj != c:
					dj = jj - j
					break
			
			di = H - i
			for ii in range(i+1, H):
				for jj in range(j, j + dj):
					(cij, wij, hij) = opt_bitmap[ii][jj]
					if wij < 0 or hij < 0 or cij != c:
						di = ii - i
						break
				if di != H - i:
					break

			if di != 1 or dj != 1:
				for ii in range(i, i+di):
					for jj in range(j, j+dj):
						opt_bitmap[ii][jj] = (c, -1, -1)
			opt_bitmap[i][j] = (c, dj, di)
 

	ret = "<table border=0 cellspacing=0 cellpadding=0 width=" + str(W) + ">\n"
	ret += "<tr height=0>"
	for c in bitmap[0]:
		ret += "<td width=1></td>"
	ret += "</tr>\n"

	for cline in opt_bitmap:
		ret += "<tr height=1>"
		for (c, w, h) in cline:
			if c == "":
				bg = ""
			else:
				bg = " bgcolor=" + c

			if w < 0 or h < 0:
				continue
			elif w > 1 and h > 1:
				ret += "<td" + bg + " colspan=" + str(w) + " rowspan=" + str(h) + "></td>"
			elif w > 1:
				ret += "<td" + bg + " colspan=" + str(w) + "></td>"
			elif h > 1:
				ret += "<td" + bg + " rowspan=" + str(h) + "></td>"
			else:
				ret += "<td" + bg + "></td>"
		ret += "</tr>\n"


	ret += "</table>"
	
	return ret



if __name__ == "__main__":
	from random import random

	bitmap = new_bitmap(512, 384)	
	rect_on(bitmap, 20, 20, 236, 344, to_hex(128, 128, 128))
	rect_on(bitmap, 256, 20, 236, 344, to_hex(128, 0, 0))
	
	for i in range(20):
		x = int(random()*412)
		y = int(random()*284)
		r = int(random()*255)
		g = int(random()*255)
		b = int(random()*255)
		rect_on(bitmap, x, y, 100, 100, to_hex(r, g, b))
	
	for i in range(20):
		x = int(random()*512)
		y = int(random()*384)
		x2 = int(random()*512)
		y2 = int(random()*384)
		r = int(random()*255)
		g = int(random()*255)
		b = int(random()*255)
		w = int(random()*5)+1
		line_on(bitmap, x, y, x2, y2, to_hex(r, g, b), w)
		
		
	for i in range(20):
		x = int(random()*512)
		y = int(random()*384)
		ra = int(random()*100)
		r = int(random()*255)
		g = int(random()*255)
		b = int(random()*255)
		w = int(random()*5)+1
		circle_on(bitmap, x, y, ra, to_hex(r, g, b), w)

	print to_html(bitmap)
