# BumpBot 💬

BumpBot is an AI-powered chatbot designed to assist pregnant women by answering common questions during pregnancy. Built with state-of-the-art tools, this app provides a conversational interface to offer guidance and information in a user-friendly way.

## Features

- **LLM-Powered Responses**: Utilizes OpenAI's language models for accurate and empathetic answers.
- **Custom Knowledge Base**: Extracts and processes content from a local PDF containing common pregnancy questions.
- **Contextual Chat**: Keeps track of chat history to deliver meaningful, context-aware responses.
- **Secure Vector Store**: Stores embeddings and search indices using FAISS for efficient and secure information retrieval.

## Built With

- **Streamlit**: For the interactive web interface.
- **LangChain**: For text processing and AI model orchestration.
- **OpenAI**: For embedding generation and natural language understanding.
- **PyPDF2**: For extracting content from the PDF knowledge base.

## Setup and Installation

1. Clone the repository:

    ```
    git clone https://github.com/yourusername/bumpbot.git
    cd bumpbot
    ```

2. Create and activate your virtual environment:

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Set up your OpenAI API Key:

    - Create a **.env** file in the root directory.
    - Add the following line, replacing `your_openai_api_key` with your actual API key:

        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

5. Run the app:

    ```
    streamlit run app.py
    ```

## License

[MIT](https://github.com/kev065/bumpbot/blob/main/LICENSE)
