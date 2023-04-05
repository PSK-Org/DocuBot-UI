import streamlit as st
import streamlit_authenticator as stauth

import time

import yaml
from yaml.loader import SafeLoader

from components.login import login
from components.sidebar import sidebar
from components.chat import chat

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'sidebar')

    sauce = """
    <style>
    footer {
	    visibility: hidden;
	}
    footer:after {
        content:'2023 - Made with ❤️ by PSK'; 
        visibility: visible;
        display: block;
        position: relative;
        padding: 5px;
        top: calc(100vh - 2.5rem);
        font-size: 1rem;
    }
    </style>
    """

    st.markdown(sauce, unsafe_allow_html=True)
    
    if authentication_status:
        st.write(f'Welcome *{name}*')
        sidebar()
        chat()
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

    #with st.spinner("Loading..."):
        #time.sleep(5)
    #st.success("Done!")
