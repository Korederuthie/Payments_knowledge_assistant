import streamlit as st
from openai import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
)

from answer_question import answer_question


st.set_page_config(
    page_title="Payments Knowledge Assistant",
    page_icon="📚",
    layout="centered",
)

st.title("Payments Knowledge Assistant")
st.write(
    "Ask about payment rejections, reconciliation "
    "and safe data handling."
)
st.caption(
    "Portfolio demonstration using fictional procedures. "
    "Enter sample questions only; do not enter customer data."
)

with st.sidebar:
    st.header("Try a question")
    st.write("What should I check when a payment is rejected?")
    st.write("Can I automatically retry after insufficient funds?")
    st.write("How do I investigate an amount mismatch?")
    st.write("What is the exact refund processing deadline?")

    st.divider()
    st.caption(
        "Each question is answered independently. "
        "The assistant cannot perform payment actions."
    )

if "result" not in st.session_state:
    st.session_state.result = None

with st.form("question_form"):
    question = st.text_area(
        "Your question",
        placeholder="What should I check when a payment is rejected?",
        max_chars=1000,
    )
    submitted = st.form_submit_button(
        "Find an answer",
        type="primary",
    )

if submitted:
    # Clear previous results so failed requests cannot show old answers.
    st.session_state.result = None

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching the documents..."):
                result = answer_question(question.strip())

            st.session_state.result = {
                "question": question.strip(),
                **result,
            }

        except AuthenticationError:
            st.error("API authentication failed. Check your local API key.")

        except RateLimitError:
            st.error(
                "The API limit was reached. Check your API quota "
                "or try again later."
            )

        except APIConnectionError:
            st.error("Could not reach the API. Check your connection.")

        except APIStatusError:
            st.error("The API request failed. Please try again later.")

        except Exception as error:
            st.error(
                "The request could not be completed. "
                f"Error type: {type(error).__name__}"
            )

result = st.session_state.result

if result is not None:
    st.divider()
    st.subheader("Your question")
    st.write(result["question"])

    st.subheader("Answer")

    if result["answerable"]:
        st.write(result["answer"])
    else:
        st.info(result["answer"])

    if result["sources"]:
        st.subheader("Supporting passages")

        for source in result["sources"]:
            label = (
                f"[{source['id']}] {source['source']} "
                f"— {source['section']}"
            )

            with st.expander(label):
                st.text(source["text"])