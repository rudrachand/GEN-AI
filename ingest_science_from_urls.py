import os
import sys
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

# ✅ Import your embedding function from your file
from get_embedding_function import get_embedding_function

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma_science"
DATA_SOURCE_URL = "https://esample.vivadigital.in/new-directions/science/class-8"

def get_chapter_links_with_playwright(main_url):
    print(f"🔍 Fetching chapter links from: {main_url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(main_url)
        page.wait_for_timeout(5000)  # Wait for JS to load

        # If links are in elements with a specific class, update this selector accordingly
        links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
        chapter_links = [link for link in links if "/new-directions/science/class-8/" in link]

        browser.close()

        if chapter_links:
            print(f"✅ Found {len(chapter_links)} chapter links.")
        else:
            print("❌ No chapter URLs found. Check page structure or connectivity.")
        return chapter_links


def load_documents(urls):
    print("📄 Loading documents from chapter URLs...")
    all_docs = []
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"⚠️ Failed to load {url}: {e}")
    return all_docs

def split_documents(documents):
    print("✂️ Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

def store_documents(chunks):
    print(f"💾 Storing {len(chunks)} chunks into Chroma DB at `{CHROMA_PATH}`...")
    embedding_function = get_embedding_function()
    db = Chroma.from_documents(chunks, embedding_function, persist_directory=CHROMA_PATH)
    db.persist()
    print("✅ Done storing!")

def main():
    chapter_urls = get_chapter_links_with_playwright(DATA_SOURCE_URL)
    if not chapter_urls:
        sys.exit("❌ Exiting: No chapter URLs to process.")

    documents = load_documents(chapter_urls)
    if not documents:
        sys.exit("❌ Exiting: No documents loaded.")

    chunks = split_documents(documents)
    store_documents(chunks)

if __name__ == "__main__":
    main()
