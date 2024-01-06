import streamlit as st
import spacy
import fitz
import base64
import os


def load_ner_model():
    # Update this path to your local NER model path
    model_path = 'model-best'
    return spacy.load(model_path)

def show_pdf(file_content):
    base64_pdf = base64.b64encode(file_content).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title("Resume Parser Web App")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.success('You have been upload a PDF!')
        # st.subheader("Uploaded PDF Content:")
        file_buffer = uploaded_file.read()
        doc = fitz.open("pdf", file_buffer)
        text = " ".join(page.get_text("text") for page in doc)
        # st.write(text)

        st.subheader("Extracted Entities:")
        ner_model = load_ner_model()
        doc = ner_model(text)
        for ent in doc.ents:
            st.write(f"{ent.label_} -> {ent.text}")

        # Call the function to display the entire PDF
        show_pdf(file_buffer)

if __name__ == "__main__":
    main()