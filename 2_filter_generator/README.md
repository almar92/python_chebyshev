# Generation of a n-th order Type 1 Chebyshev filters

## Table of contents
1. [Introduction](#Introducyion)
1. [Low-pass filter generation](#Low-pass-filter-generation)
	1. [Chebyshev tables](#chebyshev-tables)
	2. [Component calculation](#component-calculation)
	3. [Examples](#Examples)
2. [Low-pass to Band-pass conversion](#Low-pass-to-Band-pass-conversion)
	1. [Cutoff and center frequencies](#cutoff-and-center-frequencies)
	2. [Variable change and component calculations](#Variable-change-and-component-calculations)
	3. [Examples](#Examples-01)
4.  [To-do list](#To-do-list)


## Introduction

In order to use the script just open your terminal of choice, navigate to the scrpit's folder and run

````
python3 chebyshev_lp_to_bp.py
````

This script asks for

1. the desired filter's order 
2. the desired ripple coefficient
3. a ``.dat`` file with the relative normalized impedences (included as an examples the files for 5th, 6th and 7th order filters with $\epsilon =1.0$)
4. the desired cutoff frequencies

and outputs

1. The components needed for
	1. Low-pass filter
	2. Band-pass filter
	3. [(To-do)](#to-do) High-pass filter
2. A schematic drawn in the terminal with ASCII characters for all the filters (**Note:** the ``Gen`` symbol is a **real generator**, including it's parassite load. This was done in order not to overcrowd anymore the terminal, which already happens enough with the Pass-band representation)

## Low-pass filter generation

### Chebyshev tables

In order to avoid painful calculations for the components with the Normalized Tranfer Function (discussed [here](https://github.com/Squar3wave/python_chebyshev/tree/master/1_pole_calculator)) for the calculation of normalized impedences, one usually consults the Chebyshev tables, characterized by the filter's order and desired **ripple factor** $\epsilon$, as can be seen in detail here in [this article](https://www.rfcafe.com/references/electrical/cheby-proto-values.htm) by RF cafe. As an example, here are the table values needed for the examples given at the end of this document

|  N  | $g_1$  | $g_2$  | $g_3$  | $g_4$  | $g_5$  | $g_6$  | $g_7$  | $g_8$  |
|-----|--------|--------|--------|--------|--------|--------|--------|--------|
|  5  | 3.4817 | 0.7618 | 4.5381 | 0.7618 | 3.4817 | 1.0000 |        |        |
|  6  | 3.5045 | 0.7684 | 4.6061 | 0.7929 | 4.4641 | 0.6033 | 5.8095 |        |
|  7  | 3.5182 | 0.7723 | 4.6386 | 0.8039 | 4.6386 | 0.7723 | 3.5182 | 1.0000 |

Using a LC ladder configuration, these values can be reinterpreted as

|  N  | $C_2$  | $L_2$  | $C_3$  | $L_3$  | $C_1$  | $Z_{out}$  |
|-----|--------|--------|--------|--------|--------|------------|
|  5  | 3.4817 | 0.7618 | 4.5381 | 0.7618 | 3.4817 |   1.0000   |

Which, as we can see using the script, will have the following structure

````
--------------L_2-------L_3------------------
|         |         |         |         |
Gen       C_1       C_2       C_3       R_out
|         |         |         |         |
---------------------------------------------
````

|  N  | $C_1$  | $L_1$  | $C_2$  | $L_2$  | $C_3$  | $L_3$  | $Z_{out}$  |
|-----|--------|--------|--------|--------|--------|--------|------------|
|  6  | 3.5045 | 0.7684 | 4.6061 | 0.7929 | 4.4641 | 0.6033 |   5.8095   |

````
----L_1-------L_2-------L_3------------------
|         |         |         |         |
Gen       C_1       C_2       C_3       R_out
|         |         |         |         |
---------------------------------------------
````


|  N  | $C_2$  | $L_2$  | $C_3$  | $L_3$  | $C_4$  | $L_4$  | $C_1$  | $Z_{out}$  |
|-----|--------|--------|--------|--------|--------|--------|--------|--------|
|  7  | 3.5182 | 0.7723 | 4.6386 | 0.8039 | 4.6386 | 0.7723 | 3.5182 | 1.0000 |

````
--------------L_2-------L_3-------L_4------------------
|         |         |         |         |         |
Gen       C_1       C_2       C_3       C_4       R_out
|         |         |         |         |         |
--------------------------------------------------------
````


**NOTE:** all values reported here are **normalized**, and will be **denormalized**

We can notice two thing:

1. For odd order filters the second-to-last impedence in the table actually corresponds to the first net of the filter
2. For even order filters one can't have the same input and output loads, so a scaling factor is mandatory

### Components calculation

The values for a n-th order filter with a specific **ripple factor** $\epsilon$ and a specific **output load** $Z_{out}$ are calculated denormalizing the values found in Chebyshev tables via the following equations:

$$\begin{align}
C_i &= \frac{C_{i_{norm}} }{2\pi f_c \cdot Z_{out}}\\
L_i &= \frac{L_{i_{norm}} \cdot Z_{out} }{2\pi f_c}\\
R_{out} &=g_{n+1} \cdot Z_{out}
\end{align}$$

The term $g_{n+1}$ is the last impedence value on the n-th row of the table

### Examples

For all examples we choose $R_{out} = 50 \ [\Omega]$ and $f_c = 1 \ [MHz]$

1. 5th order filter with $\epsilon=1.0$

	````
	---------------------------
	| 1st net component       |
	---------------------------
	| C_1 = 1.1083e-08 [F]    |
	---------------------------
	| 2st net components      |
	---------------------------
	| L_2 = 6.0622e-06 [H]    |
	| C_2 = 1.1083e-08 [F]    |
	---------------------------
	| 3st net components      |
	---------------------------
	| L_3 = 6.0622e-06 [H]    |
	| C_3 = 1.4445e-08 [F]    |
	---------------------------
	| Output load             |
	---------------------------
	| R_out =5.0000e+01 [Ohm] |
	---------------------------
	````

2. 6th order filter with $\epsilon=1.0$

	````
	---------------------------
	| 1st net components      |
	---------------------------
	| L_1 = 6.1147e-06 [H]    |
	| C_1 = 1.1155e-08 [F]    |
	---------------------------
	| 2st net components      |
	---------------------------
	| L_2 = 6.3097e-06 [H]    |
	| C_2 = 1.4662e-08 [F]    |
	---------------------------
	| 3st net components      |
	---------------------------
	| L_3 = 4.8009e-06 [H]    |
	| C_3 = 1.4210e-08 [F]    |
	---------------------------
	| Output load             |
	---------------------------
	| R_out =2.9048e+02 [Ohm] |
	---------------------------
	````

3. 7th order filter with $\epsilon=1.0$

	````
	---------------------------
	| 1st net component       |
	---------------------------
	| C_1 = 1.1199e-08 [F]    |
	---------------------------
	| 2st net components      |
	---------------------------
	| L_2 = 6.1458e-06 [H]    |
	| C_2 = 1.1199e-08 [F]    |
	---------------------------
	| 3st net components      |
	---------------------------
	| L_3 = 6.3972e-06 [H]    |
	| C_3 = 1.4765e-08 [F]    |
	---------------------------
	| 4st net components      |
	---------------------------
	| L_4 = 6.1458e-06 [H]    |
	| C_4 = 1.4765e-08 [F]    |
	---------------------------
	| Output load             |
	---------------------------
	| R_out =5.0000e+01 [Ohm] |
	---------------------------
	````

## Low-pass to Band-pass conversion

### Cutoff and center frequencies

The resulting Band-pass filter will have the same passing band lenght as the original Low-pass. Thus, given a **cutoff frequency** $f_{LP}$ and calling the **two cutoff frequencies of the Band-pass** $f_{BP_r}$ (the higher one, consequently on the right) and $f_{BP_l}$ the smaller one we'll have

$$\begin{align}
f_{LP} = \Delta f_{BP} = f_{BP_r} - f_{BP_l}
\end{align}$$

Which, once decided one of the two allows us to deduce the other.  
We then define the **center frequency** as

$$
f_{mid} = \sqrt{f_{BP_r} \cdot f_{BP_l}}
$$

and the **relative bandwidth** as

$$
\Delta f_{rel} = \frac{\Delta_{BP}}{f_{mid}}
$$

### Variable change

Low-pass and Band-pass filters are bound together by the following variable change

$$\begin{align}
s = p + \frac{1}{p} \ ; \ p \in \mathbb{C}
\end{align}$$

This relation brings us two consequences:

1. Studying the inductors in the impedance point of view one finds
	$$\begin{align}
	Z_{LP}(s) = ks \rightarrow Z_{BP}(p) = kp + \frac{k}{p} \ ; \ p \in \mathbb{C}
	\end{align}$$

	This means that we have to add a capacitor in series to every inductor.  
	We can calculate the values using the following relation
	$$
	C_{s_k} = \frac{\Delta f_{rel}}{2\pi f_{mid} \cdot L_{k_{norm}} \cdot Z_{out}}
	$$

2. Conversely, studying the capacitors in the conductance point of view one finds that
	
	$$\begin{align}
	Y_{LP}(s) = ks \rightarrow Y_{BP}(p) = kp + \frac{k}{p} \ ; \ p \in \mathbb{C}
	\end{align}$$
	
	This means we have to put an inductor in parallel to each capacitor, which we can calculate with the following relation
	$$
	L_{p_k} = \frac{\Delta f_{rel} \cdot Z_{out}}{2\pi f_{mid} \cdot L_{k_{norm}}}
	$$

Following, as an example, the schematic for a 5th order Band-pass filter generated by the script

````
--------------------------L_2---C_s_2-----------L_3---C_s_3------------------------------
|                 |   |                 |   |                 |   |         |
Gen               C_1 L_p_1             C_2 L_p_2             C_3 L_p_3     R_out
|                 |   |                 |   |                 |   |         |
-----------------------------------------------------------------------------------------
````

### Examples

Like in the previous section, for all examples we choose  

* $R_{out} = 50 \ [\Omega]$ 
* $f_{LP} = 1 \ [MHz]$ 
* $f_{{BP}_l} = 265 \ [Mhz]$ 
* $f_{{BP}_r} = 275 \ [Mhz]$

1. 5th order filter with $\epsilon=1.0$

	````
	-----------------------------------------------------
	| 1st net components                                |
	-----------------------------------------------------
	| C_1 = 1.1083e-08 [F] | L_par_1 = 3.1352e-08 [H]   |
	-----------------------------------------------------
	| 2st net components                                |
	-----------------------------------------------------
	| L_2 = 6.0622e-06 [H] | C_ser_2 = 5.7317e-11 [F]   |
	| C_2 = 1.1083e-08 [F] | L_par_2 = 3.1352e-08 [H]   |
	-----------------------------------------------------
	| 3st net components                                |
	-----------------------------------------------------
	| L_3 = 6.0622e-06 [H] | C_ser_3 = 5.7317e-11 [F]   |
	| C_3 = 1.4445e-08 [F] | L_par_3 = 2.4054e-08 [H]   |
	-----------------------------------------------------
	|Output load                                        |
	-----------------------------------------------------
	| R_out =5.0000e+01 [Ohm]                           |
	-----------------------------------------------------

	````

2. 6th order filter with $\epsilon=1.0$

	````
	-----------------------------------------------------
	| 1st net components                                |
	-----------------------------------------------------
	| L_1 = 6.1147e-06 [H] | C_ser_1 = 5.6824e-11 [F]   |
	| C_1 = 1.1155e-08 [F] | L_par_1 = 3.1148e-08 [H]   |
	-----------------------------------------------------
	| 2st net components                                |
	-----------------------------------------------------
	| L_2 = 6.3097e-06 [H] | C_ser_2 = 5.5069e-11 [F]   |
	| C_2 = 1.4662e-08 [F] | L_par_2 = 2.3699e-08 [H]   |
	-----------------------------------------------------
	| 3st net components                                |
	-----------------------------------------------------
	| L_3 = 4.8009e-06 [H] | C_ser_3 = 7.2375e-11 [F]   |
	| C_3 = 1.4210e-08 [F] | L_par_3 = 2.4453e-08 [H]   |
	-----------------------------------------------------
	|Output load                                        |
	-----------------------------------------------------
	| R_out =2.9048e+02 [Ohm]                           |
	-----------------------------------------------------

	````

3. 7th order filter with $\epsilon=1.0$

	````
	-----------------------------------------------------
	| 1st net components                                |
	-----------------------------------------------------
	| C_1 = 1.1199e-08 [F] | L_par_1 = 3.1027e-08 [H]   |
	-----------------------------------------------------
	| 2st net components                                |
	-----------------------------------------------------
	| L_2 = 6.1458e-06 [H] | C_ser_2 = 5.6537e-11 [F]   |
	| C_2 = 1.1199e-08 [F] | L_par_2 = 3.1027e-08 [H]   |
	-----------------------------------------------------
	| 3st net components                                |
	-----------------------------------------------------
	| L_3 = 6.3972e-06 [H] | C_ser_3 = 5.4315e-11 [F]   |
	| C_3 = 1.4765e-08 [F] | L_par_3 = 2.3533e-08 [H]   |
	-----------------------------------------------------
	| 4st net components                                |
	-----------------------------------------------------
	| L_4 = 6.1458e-06 [H] | C_ser_4 = 5.6537e-11 [F]   |
	| C_4 = 1.4765e-08 [F] | L_par_4 = 2.3533e-08 [H]   |
	-----------------------------------------------------
	|Output load                                        |
	-----------------------------------------------------
	| R_out =5.0000e+01 [Ohm]                           |
	-----------------------------------------------------
	````

## To-do list

- [ ] Write proper documentation for the currently working code
	- [x] Low-pass filter
	- [ ] Band-pass filter
	- [ ] High-pass filter
- [ ] Add the conversion to High-pass
- [ ] Rename the file from ``chebyshev_lp_to_bp.py`` once all features are implemented
