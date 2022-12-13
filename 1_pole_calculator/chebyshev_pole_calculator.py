import matplotlib.pyplot as plt
import numpy as np
import math
import array


n = int(input("Input desired order of Type 1 Chebishev low-pass filter: "))
epsilon = float(input("Input desired ripple coefficient: "))

filter_name='n={0}_epsilon={1}.png'.format(n,epsilon)

print('')


v = (1/n)*math.asinh(1/epsilon)

u = np.zeros(n)
sigma = np.zeros(n)
omega = np.zeros(n)

for k in range(n):

	u[k] = ((2*(k+1)-1)/(2*n))*math.pi

	sigma[k] = -math.sin(u[k])*math.sinh(v)
	omega[k] = +math.cos(u[k])*math.cosh(v)

	print('p_{0} = {1:.4f} + j*({2:.4f})'.format(k+1,sigma[k],omega[k]))
	print('')


plt.scatter(sigma, omega, label= 'poles')

plt.savefig(filter_name)

