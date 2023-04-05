import streamlit as st
from streamlit_chat import message
import openai
import dotenv
import os

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


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
    st.session_state.chat += f'User: {st.session_state.B}'

    # TODO: Change the context
    context = """
    related information : george martin has said that he decided to kill robb stark because he wished to keep the story difficult to predict : " i killed ned because everybody th, re, after witnessing the murder of his pregnant wife and their child.lord bolton personally executes robb, stabbing him through the heart while taunt, ynden tully. though they succeed with lannister help, he is killed by arya stark, who subsequently bakes him into a pie. *'''black walder rivers'''(, ering of the stark forces at " the red wedding " ; in the ensuing massacre, roose kills robb while his mother catelyn and wife talisa are both killed as, roose suspects that ramsay murdered roose's legitimate heir and expects that ramsay will kill all of roose's future children. he is described as ugly, question : who killed robb stark? < work > answer : "'
    "'the stark heir is a man of great power,'" said lord bolton. "'he is a great lord, and a great king.'"
    " the stark boy is a boy of great wealth, " said ser rodrik. " he is the son of a great knight, and he is heir to the throne of winterfell.'
    the lord of winterfell is a son of the lord,'said ser hosteen frey. " the boy is the heir to winterfell, and the heir of the house stark.'the boy's father is a lord, " ser rodrick said. " and the boy has a great power.'he has a power, and his father is the lord.'' the lord is the king,'' he commands,'and the lord commands.'and so on. "
    the lords of the north were silent for a time. " i do not know what to make of this, " lord bolton said at last. " it is a strange tale, but i will not deny that it is true
    """

    prompt = "Answer the following question based on the context provided:\n\n" + context + "\n\nQ: " + st.session_state.B + "\nA:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": "You are DocuBot, a helpful study assistant that answers questions given some context. The context is:" + context,
            },
            {
                "role": "assistant",
                "content": "I will prepend your response with 'NO_CON' if the question does not relate to the context.",
            },
            {
                "role": "user",
                "content": "If the question does not relate to the context, prepend your response with 'NO_CON' and answer the question based on what you know. " + st.session_state.B,
            },
        ]
    )
    response = response.choices[0].message.content
    if response.startswith("NO_CON"):
        response = response.replace("NO_CON:", "")
        response = response.replace("NO_CON", "")
        response = response[:2].lower() + response[2:]
        response = "I can't find anything about that in your documents. From what I know, " + response
    # Send to server and replace below with response
    st.session_state.chat += f'\nDocuBot: {response}'
    st.session_state.B = ''
    st.session_state.chat += "\n\n"