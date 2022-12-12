# Pole calculator for type 1 Chebyshev low-pass filters

## Table of contents

1. [Introduction](#Introduction)
2. [Type 1 Chebyshev filters](#Type-1-Chebyshev-filters)
3. [Pole calculation](#Pole-calculation)    
4. [Example: 7th order low-pass filter with $\epsilon=1$](#example-7th-order-low-pass-filter-with-epsilon1)
	
## Introduction

Simple python script i made for the calculation of poles for n-th order Type 1 Chebyshev low-pass filters. The script prints on the terminal the poles values and generates a plot in the folder it's located.  

## Type 1 Chebyshev filters

Type 1 Chebishev low pass filters are characterized by a very small transient band, at the price of oscillations in the passing band. The higher the filter's oreder, the more smaller the transient band is and the more oscillations in passing band we have.  
A filter of the n-th order is characterized by the following transfer function

$$
|H_{LP}^{(n)}(j\omega)|^2 = \frac{H_0^2}{1 + \epsilon^2\cdot C_n^2(\omega)}
$$

where

* $\omega = 2\pi f$
* $H_0$ is the **maximum amplification in the filter's passing band**
* $\epsilon$ is the **ripple factor**, whose contribute to the max amplitude in the passing band is given by 

$$\begin{align}
k_p &= 20 \cdot \log_{10}(\sqrt{1 +\epsilon^2}) &[dB]
\end{align}$$

* $C_n(\omega)$ is the **n-th order Chebyshev polynomial** (which can be found tabulated, [here](https://brilliant.org/wiki/chebyshev-polynomials-definition-and-properties/) as an example), where **n** corresponds to the filter order, which are defined as such 

$$\begin{align}
C_n(\omega) &= cos(n \cdot arccos(\omega))  &\omega &\in [0,1]\\
C_n(\omega) &= cos(n \cdot arccosh(\omega)) &\omega &\geq 1
\end{align}$$  

More than $H_{LP}^{(n)}(j\omega)$ it's usually preferred the **normalized transfer function**, defined as

$$
|N_{LP}^{(n)}(j\omega)|^2=\frac{|H_{LP}^{(n)}(j\omega)|^2}{H_0^2} = \frac{1}{1 + \epsilon^2\cdot C_n^2(\omega)}
$$

## Pole calculation

Poles for Type 1 Chebyshev lay along the left side of an ellpise, with one real for odd values of n.  
Studying the tranfer function the following expression for pole calculation can be derived:

$$\begin{align}
p_k &= \sigma_k + j \omega_k\\
\sigma_k &= -sin(u_k) \cdot sinh(v)\\
\omega_k &= +cos(u_k)\cdot cosh(v)\\
u_k & = \frac{2k-1}{2n}\cdot \pi\\
v &= \frac{1}{n}\cdot arcsinh \left( \frac{1}{\epsilon} \right)\\
\end{align}$$

## Example: 7th order low-pass filter with $\epsilon=1$

For a 7th order low-pass filter with $\epsilon=1$ the normalized transfer function becomes

$$\begin{align}
|N_{LP}^{(7)}(j\omega)|^2 = \frac{1}{1 + (64\omega^7 - 112 \omega^5 + 56\omega^3 - 7\omega)^2}
\end{align}$$

Using the above formulas we get

$$\begin{align}
u_1 & = \frac{1}{14}  \cdot \pi\\
u_2 & = \frac{3}{14}  \cdot \pi\\
u_3 & = \frac{5}{14}  \cdot \pi\\
u_4 & = \frac{1}{2}   \cdot \pi\\
u_5 & = \frac{9}{14}  \cdot \pi\\
u_6 & = \frac{11}{14} \cdot \pi\\
u_7 & = \frac{13}{14} \cdot \pi\\
v &= 0.1259
\end{align}$$

This leads to the following 7 poles 

$$\begin{align}
p_1 & = −0.0281 + j · 0.9827 \\
p_2 & = −0.0787 + j · 0.7880 \\
p_3 & = −0.1137 + j · 0.4373 \\
p_4 & = −0.1262				\\
p_5 & = −0.1137 − j · 0.4373 \\
p_6 & = −0.0787 − j · 0.7880 \\
p_7 & = −0.0281 − j · 0.9827
\end{align}$$


![Image](https://github.com/Squar3wave/python_chebyshev/blob/master/n%3D7_epsilon%3D1.0.png)
