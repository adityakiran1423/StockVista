# frontend code render using streamlit
import time
import datetime
from datetime import date
import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide", initial_sidebar_state="expanded")

#st.logo("Img/BullBear.jpg")
st.title("StockVista")
st.write("The only one stop for your next investment decision!")

response = st.text_input("Are you interested in the stock market?")
st.write(f"You have entered {response} as your response")



# code for sidebar
today = date.today()  # today's date
# st.write('''# StockVista ''')  # title
st.sidebar.image("Img/BullBear.jpg", width=250,
                 use_column_width=False)  # logo
st.sidebar.write('''# StockVista ''')

with st.sidebar: 
        selected = option_menu("Info", ["About", "Home", "Analytics"])

start = st.sidebar.date_input(
    'Start', datetime.date(2022, 1, 1))  # start date input
end = st.sidebar.date_input('End', datetime.date.today())  # end date input
