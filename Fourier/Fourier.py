import streamlit as st
import pandas as pd
import numpy as np
from scipy import integrate
import plotly.express as px

st.title('Fourier series')
#フーリエ級数展開の説明
with st.beta_expander("フーリエ級数展開の説明"):
    r'''
    周期性の波形$f(x)$は式(1)の形式の[フーリエ級数](https://ja.wikipedia.org/wiki/%E3%83%95%E3%83%BC%E3%83%AA%E3%82%A8%E7%B4%9A%E6%95%B0)で表すことができる．
    周期$2\pi$の繰り返し波形の積分区間を$0\sim 2\pi$とする．
    $$
        \tag{1} g(x)=\frac{a_0}{2}+\sum _ {n=1}^{\infty} \left(a_n \cos(nx)+b_n \sin(nx) \right)
    $$
    ここで、各係数は[三角関数の直交性](https://mathematicsgarden.com/sankakutyokkou/)により整数倍のコサイン波及びサイン波を入力関数に乗じて1周期の積分により求められる．
    $$
        \tag{2} \begin{aligned}
        a_0&=\frac{1}{\pi}\int_{0}^{2\pi} f(x) dx \\
        a_n&=\frac{1}{\pi}\int_{0}^{2\pi} f(x)\cos(nx) dx, \; (n=1,2,3, \cdots) \\
        b_n&=\frac{1}{\pi}\int_{0}^{2\pi} f(x)\sin(nx) dx, \; (n=1,2,3, \cdots)
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

in_chart = st.sidebar.empty()
duty = st.sidebar.slider('Duty cycle', 0.05, 0.95, 0.5, 0.05)
if wfselected is 'Rectangular':
    tr = st.sidebar.slider('tr, tf', 0.0, 0.4, 0.0, 0.05)



#入力波形関数の定義
def inputFunc(wfselected):
    if wfselected == 'Rectangular':
        def wfin(x):    #Rectangular
            if np.pi*(1-duty) < x and x < np.pi*(1+duty):
                y = 1
            else:
                y = 0
            return y
    elif wfselected == 'Triangular':
        def wfin(x):    #Triangular
            if x < 2*np.pi*duty:
                y = x/(2*np.pi*duty)
            else:
                y = 1-(x-2*np.pi*duty)/(2*np.pi*(1-duty))
            return y
    elif wfselected == 'Sawtooth':
        def wfin(x):    #Sawtooth
            if x < 2*np.pi*duty:
                y = x/(2*np.pi*duty)
            else:
                y = 0
            return y
    else:
        def wfin(x):
            return ""
    return wfin

#入力波形関数
wfin = inputFunc(wfselected)

#入力波形プロット
x = np.arange(0, 2*np.pi, 0.01)
y = [wfin(x) for x in x]
fig_in = px.line(x=x,y=y)
fig_in.update_layout(width=300, height=200, margin_l=10, margin_r=10, margin_t=10, margin_b=10)
in_chart.plotly_chart(fig_in)


#Fourier積分関数
new_limit = 200
def intwfcos(n):
    wf=lambda x,N=n:wfin(x)*np.cos(N*x)
    int=(integrate.quad(wf, 0, 2*np.pi, limit = new_limit)[0])/np.pi
    return int

def intwfsin(n):
    wf=lambda x,N=n:wfin(x)*np.sin(N*x)
    int=(integrate.quad(wf, 0, 2*np.pi, limit = new_limit)[0])/np.pi
    return int

n=range(1,40)
a0=(integrate.quad(wfin, 0, 2*np.pi, limit = 200)[0])/np.pi
an=list(map(intwfcos,n))
bn=list(map(intwfsin,n))

gain=[np.sqrt(x**2+y**2) for x,y in zip(an,bn)]  #リスト内包表記
fig_g = px.bar(x=n,y=gain)
st.plotly_chart(fig_g)
