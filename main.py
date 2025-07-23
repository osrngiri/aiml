import streamlit as st
from DocuBotQuery import merch_func,pricing_func,rds_func

st.title("DocuBot")

option = st.selectbox("Select App:",options = ["MERCH", "PRICING","RDS"],)
in_put = st.text_input("?? Enter your question...")


if option == "MERCH":
    if in_put:
        print("In Merch...")
        output1 = merch_func(in_put)
        st.write("Answer is:")
        st.write(output1['result'].strip())
elif option == "PRICING":
    if in_put:
        print("In Pricing...")
        output2 = pricing_func(in_put)
        st.write("Answer is:")
        st.write(output2['result'].strip())
elif option == "RDS":
    if in_put:
        print("In RDS...")
        output3 = rds_func(in_put)
        st.write("Answer is:")
        st.write(output3['result'].strip())

