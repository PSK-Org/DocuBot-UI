import streamlit as st
from streamlit_chat import message


def chat():
    st.title('Docu Bot')

    st.text_area('Chat Log', key='chat', disabled=True, height=300)

    st.text_input('Input', key='B', on_change=submit)

    js = f"""
    <script>
        function scroll(dummy_var_to_force_repeat_execution){{
            var textAreas = parent.document.querySelectorAll('.stTextArea textarea');
            for (let index = 0; index < textAreas.length; index++) {{
                textAreas[index].style.color = 'red'
                textAreas[index].scrollTop = textAreas[index].scrollHeight;
            }}
        }}
        scroll({len(st.session_state.chat)})
    </script>
    """

    st.components.v1.html(js)

def submit():
    st.session_state.chat += f'\nB: {st.session_state.B}'
    st.session_state.chat += "\nA: Response from Model"
    st.session_state.B = ''