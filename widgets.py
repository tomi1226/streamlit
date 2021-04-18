import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Sidebar
st.sidebar.selectbox('Select_bar', [1,2,3])
st.sidebar.multiselect('Multiselect_bar', [1,2,3])
st.sidebar.slider('Slide me bar', min_value=0, max_value=10)

with st.sidebar.beta_expander("See explanation"):
    st.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
    st.image("DVC00029.jpg")

# Main
st.title("Streamlit widgets")
values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')
st.warning('Warning message')
st.info('Info message')

col1, col2 = st.beta_columns(2)

with col1:
    st.text('Fixed width text')
    st.markdown('_Markdown_') # see *
    st.latex(r''' e^{i\pi} + 1 = 0 ''')
    st.write('Most objects') # df, err, func, keras!
    st.write(['st', 'is <', 3]) # see *
    st.title('My title')
    st.header('My header')
    st.subheader('My sub')
    st.code('for i in range(8): foo()')
    file = st.file_uploader('File uploader')

    if file is None:
        file = "DVC00029.jpg"
    
    st.image(file)

with col2:
    st.button('Hit me')
    st.checkbox('Check me out')
    st.radio('Radio', [1,2,3])
    st.selectbox('Select', [1,2,3])
    st.multiselect('Multiselect', [1,2,3])
    st.slider('Slide me', min_value=0, max_value=10)
    st.select_slider('Slide to select', options=[1,'2'])
    st.text_input('Enter some text')
    st.number_input('Enter a number')
    st.text_area('Area for textual entry')
    st.date_input('Date input')
    st.time_input('Time entry')
    st.color_picker('Pick a color')
    
df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))

st.table(df)

data = np.random.randn(10, 1)
st.line_chart(data)