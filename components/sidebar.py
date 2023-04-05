import streamlit as st
import asyncio
import time
from utils.convert import convert

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

                    upload_info = st.empty()
                    upload_info.info("Converting...")
                    print("Converting...")

                    bytes_data = document.getvalue()
                    data = asyncio.run(convert(None, "tex", bytes_data))
                    
                    upload_info.empty()
                    upload_info.info("Done. Writing the file...")
                    print(data)

                    open("m136-test-out.tex", "wb").write(data)

                    upload_info.empty()
                    upload_info.info("✅ Wrote file to m136-test-out.tex")
                    time.sleep(4)
                    upload_info.empty()

            except Exception as e:
                print(e)
                st.error("Upload failed!")
            print(document)