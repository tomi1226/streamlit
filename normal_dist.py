import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Sidebar
file = st.sidebar.file_uploader('File uploader')
st.sidebar.selectbox('Select_bar', [1,2,3])
st.sidebar.multiselect('Multiselect_bar', [1,2,3])
sample = st.sidebar.slider('Sample size', min_value=200, max_value=500)


# Main
st.title("Streamlit widgets")
data = np.random.randn(sample, 1)

fig = px.histogram(data, range_x=[-5, 5])
st.plotly_chart(fig)

values = st.slider('Select a range of values',0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)
st.number_input('Value set')
