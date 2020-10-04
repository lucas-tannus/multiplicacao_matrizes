import time
import os
import timeit
import numpy as np
import csv
import math


def Algoritmo1(x, y):
  z = np.zeros(shape =(len(x),len(y[0])))
  
  for i in range(n):
    for j in range(p):
        z[i][j] = 0
        for k in range(m):
            z[i][j] += x[i][k] * y[k][j]

  return z


def strassen(x, y):

	if len(x) == 1:
		return x * y

	xrow, xcol = x.shape
	yrow, ycol = y.shape

	a, b, c, d = x[:xrow//2, :xcol//2], x[:xrow//2, xcol//2:], x[xrow//2:, :xcol//2], x[xrow//2:, xcol//2:]
	e, f, g, h = y[:yrow//2, :ycol//2], y[:yrow//2, ycol//2:], y[yrow//2:, :ycol//2], y[yrow//2:, ycol//2:]

	p1 = strassen(a, f - h)
	p2 = strassen(a + b, h)
	p3 = strassen(c + d, e)
	p4 = strassen(d, g - e)
	p5 = strassen(a + d, e + h)
	p6 = strassen(b - d, g + h)
	p7 = strassen(a - c, e + f)

	out = np.zeros(shape=(xrow, ycol))

	out[:xrow//2, :ycol//2] = p5 + p4 - p2 + p6
	out[:xrow//2, ycol//2:] = p1 + p2
	out[xrow//2:, :ycol//2] = p3 + p4
	out[xrow//2:, ycol//2:] = p1 + p5 - p3 - p7

	return out

with open('times_2n_v2.csv', 'w+', newline='') as csv_file:
	for size in [2**i for i in range(1, 12)]:
		A = np.random.randint(0, 5000, size=(size, size))
		B = np.random.randint(0, 5000, size=(size, size))

		n = len(A)
		m = len(B)
		p = len(B[0])

		if math.ceil(math.log(n, 2)) != math.floor(math.log(n, 2)):
			n2 = 2 ** int(math.ceil(math.log(n, 2)))

			x = np.zeros(shape=(n2,n2))
			for i in range(n):
				for j in range(n):
					x[i][j] = A[i][j]

			y = np.zeros(shape=(n2,n2))
			for i in range(n):
				for j in range(n):
					y[i][j] = B[i][j]
		
			A = x
			B = y

		tempos_algoritmo1 = []
		tempos_strassen = []
		print('Iniciando cálculo para matriz tamanho {}...'.format(size))
		for _ in range(20):
			start_time = time.time()
			Algoritmo1(A, B)
			end_time = time.time()
			t = (end_time - start_time)
			tempos_algoritmo1.append(t)

			start_time = time.time()
			strassen(A, B)
			end_time = time.time()
			t = (end_time - start_time)
			tempos_strassen.append(t)

		print_algoritmo1 = ['Algoritmo1', size]
		print_algoritmo1.extend(tempos_algoritmo1)
		print_strassen = ['Strassen', size]
		print_strassen.extend(tempos_strassen)

		writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
		writer.writerow(print_algoritmo1)
		writer.writerow(print_strassen)

		print('Tamanho {} finalizado'.format(size))
