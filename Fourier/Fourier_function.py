import numpy as np
from scipy import integrate
import plotly.express as px

#入力波形の定義
inputName = ('Rectangular','Triangular','Sawtooth')
duty=0.5

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

#入力波形の描画



def inputFig(x):
    y = [wfin(x) for x in x]

    fig = px.line(x=x,y=y)
    fig.update_layout(width=300,height=200,margin_l=10,margin_r=10,margin_t=10,margin_b=10)
    return fig

# n倍周波数のcos波、sin波を入力波形にかけて-piからpiまで積分する
# 入力波形が不連続の場合はlimit値(default=50)を増やさないとエラーになる

new_limit = 200

def intwfcos(n):
    wf=lambda x,N=n:wfin(x)*np.cos(N*x)
    int=(integrate.quad(wf, 0, 2*np.pi, limit = new_limit)[0])/np.pi
    return int

def intwfsin(n):
    wf=lambda x,N=n:wfin(x)*np.sin(N*x)
    int=(integrate.quad(wf, 0, 2*np.pi, limit = new_limit)[0])/np.pi
    return int
