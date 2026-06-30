import streamlit as st

def ocultar_menu_streamlit():

    st.markdown("""
    <style>

    [data-testid="stSidebarNav"] {
        display:none;
    }

    #MainMenu {
        visibility:hidden;
    }

    footer {
        visibility:hidden;
    }

    header {
        visibility:hidden;
    }

    section[data-testid="stSidebar"]{
        background:#0a0a0a;
        border-right:1px solid #202020;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span{
        color:white;
    }

    .main {
        visibility: visible !important;
        display: block !important;
    }

    .stButton > button{
        width:100%;
        border-radius:12px;
        border:1px solid #ff0000;
        background:#111111;
        color:white;
        font-weight:600;
        transition:0.2s;
    }

    .stButton > button:hover{
        border:1px solid #ff0000;
        background:#ff0000;
        color:white;
    }

    </style>
    """, unsafe_allow_html=True)
