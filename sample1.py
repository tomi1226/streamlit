import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px


#side bar
option = st.sidebar.selectbox(
    'How would you like to be contacted?',
     ('1', '2', '3'))
points = st.sidebar.slider('How old are you?', 0.2, 0.9, 0.5)
Ns = st.sidebar.number_input('Insert a number', 1, 20, 4, 1)

st.write('option:', option)
st.write("points", points)
st.write("number Ns", Ns)

st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')

"""
# 初めての Streamlit
データフレームを表として出力できます:
"""

df = pd.DataFrame({
   'first column': [1, 2, 3, 4],
   'second column': map(lambda x: x/Ns, [10, 20, 30, 40])
})

st.dataframe(df)

"""
# グラフ描画の例
"""

chart_data = pd.DataFrame(
    np.random.randn(int(points*100), int(option)))

st.line_chart(chart_data)

x2 = np.random.randn(200)
hist_data = [x2]
group_labels = ['Group 1']
fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5])
#fig = ff.create_distplot(np.random.randn(200), ['random'])
#st.plotly_chart(fig)

x1 = np.linspace(-np.pi, np.pi, 500)
fig = px.line(x=x1, y=[points*np.sin(x1*Ns), np.cos(x1*Ns/2)])

# df = px.data.gapminder().query("continent=='Oceania'")
# fig = px.line(df, x="year", y="lifeExp", color='country')
st.plotly_chart(fig)