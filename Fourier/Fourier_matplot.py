import streamlit as st
import pandas as pd
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

pi = np.pi
# plt.style.use('default') 
# plt.style.use('ggplot') 
plt.style.use('seaborn') 
# plt.style.use('bmh') 

st.title('Fourier series')
#フーリエ級数展開の説明
with st.beta_expander("フーリエ級数展開の説明"):
    r'''
    周期性の波形$f(x)$は式(1)の形式の[フーリエ級数](https://ja.wikipedia.org/wiki/%E3%83%95%E3%83%BC%E3%83%AA%E3%82%A8%E7%B4%9A%E6%95%B0)で表すことができる．
    周期$2\pi$の繰り返し波形の積分区間を$-\pi \sim \pi$とする．
    $$
        \tag{1} g(x)=\frac{a_0}{2}+\sum _ {n=1}^{\infty} \left(a_n \cos(nx)+b_n \sin(nx) \right)
    $$
    ここで、各係数は[三角関数の直交性](https://mathematicsgarden.com/sankakutyokkou/)により整数倍のコサイン波及びサイン波を入力関数に乗じて1周期の積分により求められる．
    $$
        \tag{2} \begin{aligned}
        a_0&=\frac{1}{\pi}\int_{-\pi}^{\pi} f(x) dx \\
        a_n&=\frac{1}{\pi}\int_{-\pi}^{\pi} f(x)\cos(nx) dx, \; (n=1,2,3, \cdots) \\
        b_n&=\frac{1}{\pi}\int_{-\pi}^{\pi} f(x)\sin(nx) dx, \; (n=1,2,3, \cdots)
        \end{aligned}
    $$

    奇関数(原点対称) $a_n=0$, 遇関数(y軸対称) $b_n=0$  
    $a_n \neq 0$ かつ $b_n \neq 0$ の場合  
    $$
        \tag{3} a_n \cos(nx)+b_n \sin(nx) =\sqrt{a_n^2 + b_n^2}\sin(nx+\phi) 
    $$
    $$  \tag{4} \phi=\begin{cases}
        \arctan \left(\dfrac{a_n}{b_n}\right) & 0<b_n \\
        \arctan \left(\dfrac{a_n}{b_n}\right)+\pi & b_n<0 \\
        \dfrac{1}{2}\pi & b_n=0
        \end{cases}
    $$
    '''

#入力波形の選択
st.sidebar.subheader('Input waveform')
inputName = ('Rectangular','Triangular','Sawtooth')
wfselected = st.sidebar.selectbox('Select input waveform', inputName)

wfin_chart = st.sidebar.empty()
d = st.sidebar.slider('duty cycle', 0.05, 1.0, 0.5, 0.05)
if wfselected is 'Rectangular':
    tr = st.sidebar.slider('tr, tf', 0.0, 0.4, 0.0, 0.05)

#入力波形関数の定義
def inputFunc(wfselected):
    if wfselected == 'Rectangular':
        if tr == 0:
            def wfin(x):    #Rectangular
                if -pi*d < x and x < pi*d:
                    y = 1
                else:
                    y = 0
                return y
        else:
            def wfin(x):    #Rectangular
                if -pi*(d+tr) < x and x <= -pi*(d-tr):
                    y = (x+pi*d+pi*tr)/(2*pi*tr)
                elif -pi*(d-tr) < x and x <= pi*(d-tr):
                    y = 1
                elif pi*(d-tr) < x and x <= pi*(d+tr):
                    y = 1-(x-pi*d+pi*tr)/(2*pi*tr)
                else:
                    y = 0
                return y
    elif wfselected == 'Triangular':
        def wfin(x):    #Triangular
            if x < 2*pi*d-pi:
                y = (x+pi)/(2*pi*d)
            else:
                y = (pi-x)/(2*pi*(1-d))
            return y
    elif wfselected == 'Sawtooth':
        def wfin(x):    #Sawtooth
            if x < 2*pi*d-pi:
                y = (x+pi)/(2*pi*d)
            else:
                y = 0
            return y
    else:
        def wfin(x):
            return ""
    return wfin

#入力波形
#入力波形プロット
x = np.arange(-pi, pi, 0.001)
y = [wfin(関数
wfin = inputFunc(wfselected)
x) for x in x]
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3))
ax.plot(x, y)
wfin_chart.pyplot(fig)

#Fourier積分関数: 積分して高調波次数の各係数を求める a0, a1..., b1...
new_limit = 200

@st.cache
def intwfcos(n):
    wf=lambda x,N=n:wfin(x)*np.cos(N*x)
    int=(integrate.quad(wf, -pi, pi, limit = new_limit)[0])/pi
    return int

@st.cache
def intwfsin(n):
    wf=lambda x,N=n:wfin(x)*np.sin(N*x)
    int=(integrate.quad(wf, -pi, pi, limit = new_limit)[0])/pi
    return int

n=np.arange(1,41)
a0=(integrate.quad(wfin, -pi, pi, limit = 200)[0])/pi
an=list(map(intwfcos,n))
bn=list(map(intwfsin,n))

r'''
    $$
        a_n \cos(nx)+b_n \sin(nx) =\sqrt{a_n^2 + b_n^2}\sin(nx+\phi) 
    $$
'''

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
for n in range(1,7):
       ax1.plot(x,an[n-1]*np.cos(n*x))
       ax2.plot(x,bn[n-1]*np.sin(n*x))
st.pyplot(fig)



amp=[np.sqrt(x**2+y**2) for x,y in zip(an,bn)]  #リスト内包表記

def phase(an, bn):
    an = an if an > 1e-8 else 0
    bn = bn if an > 1e-8 else 0

    if 0 < bn:
        return np.arctan(an/bn)
    elif bn < 0:
        return np.arctan(an/bn)+pi
    elif bn == 0:
        return pi/2

phase=[phase(x, y) for x,y in zip(an,bn)]

n=np.arange(1,41)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 4))
ax1.stem(n,amp)
ax2.stem(n,phase)
st.pyplot(fig)


N = st.slider('order', 2, 40, 5, 1)
def wfout(x):
    y=a0/2
    for n in range(1,N):
        y = y + an[n-1]*np.cos(n*x)+bn[n-1]*np.sin(n*x)
    return y

x = np.arange(-pi, pi, 0.001)
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
ax.plot(x, [wfin(x) for x in x])
ax.plot(x, wfout(x))
st.pyplot(fig)





