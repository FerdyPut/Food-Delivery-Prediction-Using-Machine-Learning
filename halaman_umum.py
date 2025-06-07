from streamlit_option_menu import option_menu
import streamlit as st

# Page config
st.set_page_config(page_title="Food Time Delivery Project", layout="wide")

# NAVIGATION BAR (ATAS)
st.title("Food Time Delivery Tools")
selected = option_menu(
    menu_title= None,
    options=["Introduction", "EDA", "Prediction Tools"],
    icons=["book", "archive","tools"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "black", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#ff4b4b", "color": "white"},
    }
)

# SECTION CONTROL
if selected == "Introduction":
    import intro
    intro.tampilkan_halaman_umum()
elif selected == "EDA":
    import eda
    eda.eda()
