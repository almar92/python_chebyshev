import matplotlib.pyplot as plt
import numpy as np
import math
import array
from io import StringIO

print("----------------------------------------------------------------------")
print("Type 1 Chebyshev Low-pass and corresponding Band-pass filter generator")
print("----------------------------------------------------------------------")
print("")

order   = int(input("Input desired filter order: "))
epsilon = float(input("Input desired ripple coefficient: "))

file_name = "coefficients_{0}th_order_epsilon={1}.dat".format(order, epsilon)

chebyshev   = np.loadtxt(file_name)
chebyshev_C = chebyshev[::2]

if (len(chebyshev)%2 == 0):         # Odd order filters
    chebyshev_L = chebyshev[1:-1:2]
else:                               # Even order filters
    chebyshev_L = chebyshev[1::2]

print("")
print("------------------------------------------------------------------")
print("Low-pass filter componet generation")
print("(ladder configuration LC as shown below")
print("")
print("----L-------")
print("|       |  ")
print("Gen     C  ...")
print("|       |  ")
print("------------")
print("")
print("------------------------------------------------------------------")
print("")

R_o = int(input("Input desired output load [Ohm]: "))
omega_cut = int(input("Input desired cutoff frequency [Hz]:  "))



if(len(chebyshev)%2==0):        # For odd order filters
    c_len = len(chebyshev) - int(len(chebyshev)/2)
else:
    c_len = len(chebyshev) - int(len(chebyshev)/2) - 1

l_len = len(chebyshev) - 1 - c_len

C = np.zeros(c_len)
L = np.zeros(l_len)

R_out = chebyshev[len(chebyshev)-1] * R_o

print("")

if(len(chebyshev)%2==0):        # For odd order filters

    C[c_len-1] = chebyshev[len(chebyshev)-2]/(R_o*2*math.pi*omega_cut)

    print("---------------------------")
    print("| {0}st net component       |".format(1))
    print("---------------------------")
    print("| C_{0} = {1:.4e} [F]    |".format(1,C[c_len-1]))
    print("---------------------------")
else:
    print("---------------------------")



for n in range(l_len):

    if(len(chebyshev)%2==0):        # For odd order filters
        j = n+2
    else:                           # For even order filters
        j = n+1

    print("| {0}st net components      |".format(j))
    print("---------------------------")

    C[n] = chebyshev_C[n]/(R_o*2*math.pi*omega_cut)

    L[n] = (R_o*chebyshev_L[n])/(2*math.pi*omega_cut)

    print("| L_{0} = {1:.4e} [H]    |\n| C_{0} = {2:.4e} [F]    |".format(j,L[n],C[n]))
    print("---------------------------")


print("| Output load             |")
print("---------------------------")
print("| R_out ={0:.4e} [Ohm] |".format(R_out))
print("---------------------------")
print("")




# This code section draws a schematic on the terminal for the low-pass

print("Schematic of the circuit")
print("")

if(len(chebyshev)%2==0):        # For odd order filters
    L_string = "----------"
else:                           # For even order filters
    L_string = "----L_{0}---".format(1)

C_string_1 = "|"
C_string_2 = "Gen"
C_string_3 = ""

if(len(chebyshev)%2==0):        # For odd order filters
    ll = l_len
else:
    ll = l_len-1

for k in range(ll) :

    L_string = L_string + "----L_{0}---".format(k+2)

L_string = L_string + "--------------"

for k in range(c_len) :

    C_string_1 = C_string_1 + "         |"
    C_string_2 = C_string_2 + "       C_{0}".format(k+1)
    C_string_3 = C_string_3 + "-----------"

L_string = L_string + "-"
C_string_1 = C_string_1 + "         |"
C_string_2 = C_string_2 + "       R_out"
C_string_3 = C_string_3 + "------------"

print(L_string)
print(C_string_1)
print(C_string_2)
print(C_string_1)
print(C_string_3)




# Conversion from low-pass to band-pass

print("")
print("------------------------------------------------------------------")
print("Conversion from low-pass to band-pass")
print("")
print("----L---C_ser-----------")
print("|               |   | ")
print("Gen             C   L_par ...")
print("|               |   | ")
print("------------------------")
print("")
print("------------------------------------------------------------------")
print("")

L_par = np.zeros(len(C))
C_ser = np.zeros(len(L))

f_1    = int(input("Input desired left cutoff frequency [Hz]:  "))
f_2    = int(input("Input desired right cutoff frequency [Hz]: "))
f_cent = np.sqrt(f_1*f_2)


Delta_f_rel = (f_2 - f_1)/f_cent

print("")
print("f_mid = {0:.4e}\nDelta_f_rel ={1:.4e}".format(f_cent,Delta_f_rel))
print("")


if(len(chebyshev)%2 ==0):       # For odd order filters

    L_par[len(L_par)-1] = (Delta_f_rel*R_o)/(2*math.pi*f_cent*chebyshev_C[len(C)-1])

    print("-----------------------------------------------------")
    print("| {0}st net components                                |".format(1))
    print("-----------------------------------------------------")
    print("| C_{0} = {1:.4e} [F] | L_par_{0} = {2:.4e} [H]   |".format(1,C[c_len-1],L_par[len(L_par)-1]))
    print("-----------------------------------------------------")
else:
    print("-----------------------------------------------------")

for n in range(l_len):

    if(len(chebyshev)%2==0):        # For odd order filters
        j = n+2
    else:
        j = n+1

    print("| {0}st net components                                |".format(j))
    print("-----------------------------------------------------")


    L_par[n] = (Delta_f_rel*R_o)/(2*math.pi*f_cent*chebyshev_C[n])

    C_ser[n] = (Delta_f_rel)/(2*math.pi*f_cent*chebyshev_L[n]*R_o)
    print("| L_{0} = {1:.4e} [H] | C_ser_{0} = {4:.4e} [F]   |\n| C_{0} = {2:.4e} [F] | L_par_{0} = {3:.4e} [H]   |".format(j, L[n], C[n], L_par[n], C_ser[n]))
    print("-----------------------------------------------------")



print("|Output load                                        |")
print("-----------------------------------------------------")
print("| R_out ={0:.4e} [Ohm]                           |".format(R_out))
print("-----------------------------------------------------")
print("")


# This code section draws a schematic on the terminal for the pass-band

print("Schematic of the circuit")
print("")

if(len(chebyshev)%2==0):        # For odd order filters
    L_string = "----------------------"
else:
    L_string = "----L_{0}---C_s_{0}-------".format(1)

C_string_1 = "|"
C_string_2 = "Gen  "
C_string_3 = ""

for k in range(ll) :

    L_string = L_string + "----L_{0}---C_s_{0}-------".format(k+2)

L_string = L_string + "----------------------"


for k in range(c_len) :
    C_string_1 = C_string_1 + "                 |   |"
    C_string_2 = C_string_2 + "             C_{0} L_p_{0}".format(k+1)
    C_string_3 = C_string_3 + "----------------------"

L_string = L_string     +"-"
C_string_1 = C_string_1 + "         |"
C_string_2 = C_string_2 + "     R_out"
C_string_3 = C_string_3 + "-----------------------"

print(L_string)
print(C_string_1)
print(C_string_2)
print(C_string_1)
print(C_string_3)


