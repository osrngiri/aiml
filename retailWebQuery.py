import streamlit as st
from RetailSearch import agent_function

st.title("New Gen Retail Search")

in_put = st.text_input("👉 Enter your search...")

if in_put:
    output1 = agent_function(in_put)
    st.write("Answer is:")
    # st.write(output1['result'].strip())
    st.write(output1)