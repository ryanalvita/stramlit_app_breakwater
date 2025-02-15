import streamlit as st


if "y" == 'y':
    from src.components import sidebar
    sidebar.show_sidebar()

st.title('streamlit_app_breakwater')
st.write('Streamlit app for the conceptual design of breakwaters')