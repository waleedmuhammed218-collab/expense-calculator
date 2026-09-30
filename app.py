import streamlit as st
from practice import app

st.title("💰 Expense Calculator")

food = st.number_input("Food", min_value=0)
transport = st.number_input("Transport", min_value=0)
things = st.number_input("Things", min_value=0)

if st.button("Calculate"):

    prompt = f"""
    Calculate my expenses:
    food = {food}
    transport = {transport}
    Things = {things}
    """

    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    st.write(result["messages"][-1].content)