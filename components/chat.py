import streamlit as st
from streamlit_chat import message
import openai
import dotenv
import os
from dbus_next.service import ServiceInterface, method, dbus_property, signal, Variant
from dbus_next.aio import MessageBus
import asyncio
import nest_asyncio

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Chat(object):
    
    def __init__(self):
#         nest_asyncio.apply()
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.load_bus_data())
    
    # bus stuff
    
    async def load_bus_data(self):
        self.bus = await MessageBus().connect()
        
        self.introspection = await self.bus.introspect('ca.samiyousef.tpu', '/textbookai/editai')

        self.ai_obj = self.bus.get_proxy_object('ca.samiyousef.tpu', '/textbookai/editai', self.introspection)
        
        self.ai = self.ai_obj.get_interface('ca.samiyousef.tpu.editai')
        
        print("connect to bus")
        
    async def get_answer(self, question):
        
        answer = await self.ai.call_ask(question)
        
        st.session_state.chat += f'\nDocuBot: {answer}'
        st.session_state.B = ''
        st.session_state.chat += "\n\n"

    def chat(self):
        st.title('DocuBot Chat')

        st.text_area('Chat Log', key='chat', disabled=True, height=300)

        st.text_input('Input', key='B', on_change=self.submit)

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

        css = """
        <style>
            .block-container {
                padding-bottom: 2rem !important;
                padding-top: 2rem !important;
            }
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main > div {
                flex-grow: unset !important;
                height: 0 !important;
            }
        </style>
        """

        st.components.v1.html(js, height=0)
        st.markdown(css, unsafe_allow_html=True)

    def submit(self):
        question = st.session_state.B
        st.session_state.chat += f'User: {question}'

#         # TODO: Change the context
#         context = """
#         related information : george martin has said that he decided to kill robb stark because he wished to keep the story difficult to predict : " i killed ned because everybody th, re, after witnessing the murder of his pregnant wife and their child.lord bolton personally executes robb, stabbing him through the heart while taunt, ynden tully. though they succeed with lannister help, he is killed by arya stark, who subsequently bakes him into a pie. *'''black walder rivers'''(, ering of the stark forces at " the red wedding " ; in the ensuing massacre, roose kills robb while his mother catelyn and wife talisa are both killed as, roose suspects that ramsay murdered roose's legitimate heir and expects that ramsay will kill all of roose's future children. he is described as ugly, question : who killed robb stark? < work > answer : "'
#         "'the stark heir is a man of great power,'" said lord bolton. "'he is a great lord, and a great king.'"
#         " the stark boy is a boy of great wealth, " said ser rodrik. " he is the son of a great knight, and he is heir to the throne of winterfell.'
#         the lord of winterfell is a son of the lord,'said ser hosteen frey. " the boy is the heir to winterfell, and the heir of the house stark.'the boy's father is a lord, " ser rodrick said. " and the boy has a great power.'he has a power, and his father is the lord.'' the lord is the king,'' he commands,'and the lord commands.'and so on. "
#         the lords of the north were silent for a time. " i do not know what to make of this, " lord bolton said at last. " it is a strange tale, but i will not deny that it is true
#         """

#         prompt = "Answer the following question based on the context provided:\n\n" + context + "\n\nQ: " + st.session_state.B + "\nA:"
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             temperature=0.5,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are DocuBot, a helpful study assistant that answers questions given some context. The context is:" + context,
#                 },
#                 {
#                     "role": "assistant",
#                     "content": "I will prepend your response with 'NO_CON' if the question does not relate to the context.",
#                 },
#                 {
#                     "role": "user",
#                     "content": "If the question does not relate to the context, prepend your response with 'NO_CON' and answer the question based on what you know. " + st.session_state.B,
#                 },
#             ]
#         )
#         response = response.choices[0].message.content
#         if response.startswith("NO_CON"):
#             response = response.replace("NO_CON:", "")
#             response = response.replace("NO_CON", "")
#             response = response[:2].lower() + response[2:]
#             response = "I can't find anything about that in your documents. From what I know, " + response

        st.session_state.chat += f'\nwaiting for response ...'
#         nest_asyncio.apply()
        self.loop.run_until_complete(self.get_answer(question))
        
        # Send to server and replace below with response
        
    