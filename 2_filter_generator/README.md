# Generation of a n-th order Type 1 Chebyshev filters

## Table of contents
1. [Introduction](#Introducyion)
1. [Low-pass filter generation](#Low-pass-filter-generation)
	1. [Examples](#Examples)
		1. [5th order filter with $\epsilon=1.0$](#5th-order-filter-with-epsilon10)
		2. [6th order filter with $\epsilon=1.0$](#6th-order-filter-with-epsilon10)
		3. [7th order filter with $\epsilon=1.0$](#7th-order-filter-with-epsilon10)
2. [Low-pass to Band-pass conversion](#Low-pass-to-Band-pass-conversion)
	1. [Examples](#Examples)
		1. [5th order filter with $\epsilon=1.0$](#5th-order-filter-with-epsilon10-1)
		2. [6th order filter with $\epsilon=1.0$](#6th-order-filter-with-epsilon10-1)
		3. [7th order filter with $\epsilon=1.0$](#7th-order-filter-with-epsilon10-1)
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

#### 5th order filter with $\epsilon=1.0$

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

#### 6th order filter with $\epsilon=1.0$

#### 7th order filter with $\epsilon=1.0$

## Low-pass to Band-pass conversion

### Examples

#### 5th order filter with $\epsilon=1.0$

#### 6th order filter with $\epsilon=1.0$

#### 7th order filter with $\epsilon=1.0$

## To-do list

- [ ] Write proper documentation for the currently working code
- [ ] Add the conversion to High-pass
- [ ] Rename the file from ``chebyshev_lp_to_bp.py`` once all features are available

