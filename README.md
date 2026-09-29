\# Payments Operations Knowledge Assistant



A Python application that answers questions about fictional payments

procedures using retrieval-augmented generation (RAG).



Built as a portfolio project inspired by reporting, reconciliation

and investigation activities in payments operations.



\## Features



\- Searches Markdown procedures using embeddings and Chroma.

\- Generates answers using retrieved evidence.

\- Displays source filenames, section headings and supporting passages.

\- Declines questions that the available documents cannot answer.

\- Includes a Streamlit interface and six live evaluation tests.



\## Architecture



Documents → Section splitting → OpenAI embeddings → Chroma index



Question → Question embedding → Retrieve three passages

→ LLM structured response → Citation checks → Answer and sources



The application follows a fixed retrieval workflow. It does not

autonomously plan tasks or perform payment actions.



\## Technology



Python, OpenAI API, Chroma, Streamlit, Pydantic, python-dotenv and pytest.



\## Sample documents



The knowledge base contains three fictional documents with 15 sections:



\- Rejected payment submissions

\- Payment reconciliation

\- Safe data handling



These are demonstration procedures, not Global Payments policies.



\## Setup



Use Python 3.10 and create a virtual environment:



```bash

python -m venv .venv

```



Activate it in Windows Git Bash:



```bash

source .venv/Scripts/activate

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



Create a local `.env` file:



```dotenv

OPENAI\_API\_KEY=your\_api\_key\_here

```



Build the index:



```bash

python index\_documents.py

```



Run the app:



```bash

python -m streamlit run app.py

```



\## Evaluation



Run the live tests:



```bash

python -m pytest tests/test\_assistant.py -v

```



An initial run passed all six tests in 12.04 seconds. The cases cover:



\- Relevant citations for three supported questions

\- An unknown refund deadline

\- An unrelated weather question

\- An instruction to invent an official policy



The answer prompt was subsequently refined to preserve conditional

wording in the source documents. A manual retry question confirmed

the revised wording with the relevant citation.



Tests make live API calls and require a valid API key and quota.

Results may vary between runs.



\## Limitations



\- Evaluation currently covers a small set of questions.

\- Citation checks verify that references exist, not that every claim

&#x20; is supported by the cited passage.

\- Refusal relies partly on model judgement.

\- The application has no authentication or document access controls.

\- Questions are independent; there is no conversation memory.

\- The interface warns against sensitive data, but automated detection

&#x20; or redaction is not implemented.

\- Indexing is designed for the small Markdown demonstration corpus.

\- This is a portfolio prototype, not a production payments system.



\## Data and secrets



Use fictional procedures and synthetic data only.



The `.env`, `.venv` and `.chroma` directories or files are excluded

through `.gitignore`. Never commit API keys or customer records.

