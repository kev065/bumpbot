import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks.manager import get_openai_callback

# Sidebar contents
with st.sidebar:
    st.title('Common questions asked during pregnancy')

    # Path to your image file
    image_path = "pregnant_woman.jpg"

    # Display the image
    st.image(image_path, caption='Helping Pregnant Women', use_container_width=True)
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built with:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
                
    Built by [Kelvin Murithi](https://www.linkedin.com/in/kayoi)
    ''')

    add_vertical_space(5)

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key is missing. Please set it in your environment variables.")
    st.stop()

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key


def main():
    st.header("BumpBot💬")

    # Get the file path from the user
    file_path = "common_pregnancy_questions.pdf"

    # Check if the file exists
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found. Please ensure the file exists.")
        return

    # Open the PDF file
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        # Extracting store name from the file path
        store_name = os.path.splitext(os.path.basename(file_path))[0]

        # Load or create FAISS index
        if os.path.exists(f"{store_name}_faiss"):
            VectorStore = FAISS.load_local(f"{store_name}_faiss", OpenAIEmbeddings())
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            VectorStore.save_local(f"{store_name}_faiss")

    # Initialize the chat messages history
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Hello. How can I help?"}]

    # Prompt for user input and save
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        docs = VectorStore.similarity_search(query=prompt, k=3)

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, we need to generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        # Call LLM
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = OpenAI()
                chain = load_qa_chain(llm=llm, chain_type="stuff")
                with get_openai_callback() as cb:
                    response = chain.run(input_documents=docs, question=prompt)

                st.write(response)

        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


if __name__ == '__main__':
    main()
