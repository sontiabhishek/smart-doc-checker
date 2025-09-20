import streamlit as st
import os
from docx import Document
from textblob import TextBlob
import datetime

def read_text_file(uploaded_file):
    """Reads the content of a text file."""
    return uploaded_file.read().decode()

def read_docx_file(uploaded_file):
    """Reads the content of a docx file."""
    document = Document(uploaded_file)
    full_text = []
    for paragraph in document.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

def correct_spelling(text):
    """Corrects spelling mistakes in the given text using TextBlob."""
    blob = TextBlob(text)
    return str(blob.correct())

def generate_report(original_text, corrected_text):
    """Generates a report and saves it to the reports directory."""
    report_filename = os.path.join("reports", f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_filename, "w") as f:
        f.write("--- Report ---\n")
        f.write(f"Number of docs checked: {st.session_state.usage_count}\n")
        f.write(f"Billing summary: {st.session_state.usage_count * 10} INR\n")
        f.write("\n--- Original Text ---\n")
        f.write(original_text)
        f.write("\n--- Corrected Text ---\n")
        f.write(corrected_text)
    return report_filename


def display_billing_summary():
    st.write(f"Docs Checked: {st.session_state.usage_count}")
    st.write(f"Total Bill: {st.session_state.usage_count * 10} INR")

def simulate_policy_update():
    """Simulates an external policy update and displays the corrected version."""
    sample_policy = "New polcy: Atendance requierd 80%"
    st.subheader("Simulated Policy Update:")
    st.write(f"Original: {sample_policy}")

    st.write(f"Corrected: {corrected_policy}")



def main():
    # Initialize session state for usage counter
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0


    st.title("Smart Document Checker")
    st.write("Upload a document to extract and display its text content.")

    # Ensure the 'reports' directory exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # File upload section
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "docx", "pdf"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        # Read the file based on its extension
        if file_extension == "txt":
            raw_text = read_text_file(uploaded_file)
        elif file_extension == "docx":
            raw_text = read_docx_file(uploaded_file)       
        else:
            st.error("Unsupported file type. Please upload a .txt or .docx file.")
            return  # Stop further execution

        # Increment usage counter
        st.session_state.usage_count += 1



        # Display the raw text
        st.subheader("Raw Text:")
        st.text_area("Document Content", raw_text, height=300)

        # Correct spelling
        corrected_text = correct_spelling(raw_text)

        # Display original and corrected text side by side
        col1, col2 = st.columns(2)
        with col1:

            st.subheader("Original Text")
            st.write(raw_text)
        with col2:
            st.subheader("Corrected Text")
            st.write(corrected_text)
        # Basic Analysis (Placeholder - to be implemented later)

        st.write("Here, you would implement text analysis using libraries like TextBlob.")

        st.subheader("Billing Summary:")
        # Display billing summary

        # Display billing summary
        if st.button("Generate Report"):
            report_file = generate_report(raw_text, corrected_text)
            st.success(f"Report saved to {report_file}")

if __name__ == "__main__":
    main()