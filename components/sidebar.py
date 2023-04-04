import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Upload desired documents\n"
            "2. Ask question and get context based responses\n"
        )

        st.write('# Document Manager')

        user_document = st.file_uploader(
            "Upload a pdf, docx, or txt file",
            type=["pdf"],
        )

        print(user_document)

        document = None
        if user_document is not None:
            if user_document.name.endswith(".pdf"):
                document = user_document
            else:
                raise ValueError("Only PDFs are supported!")
            
            try:
                with st.spinner("Processing Documents..."):
                    upload_document(document)
            except:
                st.error("Upload failed!")
            print(document)