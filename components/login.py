import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

def login():

    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )    

    name, authentication_status, username = authenticator.login('Login', 'main')

    return name, authentication_status, username