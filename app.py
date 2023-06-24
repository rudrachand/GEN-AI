import streamlit as st
import openai
import json
from config import api_key

openai.api_key = api_key

def generate_product_description(notes):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Write a product description based on the below information and give best unique punch line.\n\n{notes}\n\nDescription:",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']

def main():
    st.title("🌟 Product Content Generator 🚀")

    # Input field for notes
    notes = st.text_area("📝 Enter product information")

    # Generate button
    if st.button("🔥 Generate Description"):
        if notes:
            with st.spinner("🎉 Generating description..."):
                product_description = generate_product_description(notes)
            st.subheader("📣 Generated Description:")
            st.success(product_description)
        else:
            st.warning("⚠️ Please enter product information.")

if __name__ == "__main__":
    main()