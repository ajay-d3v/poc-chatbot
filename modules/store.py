import os
import fitz  # pymupdf
import pytesseract
from PIL import Image
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

# Initialize gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def read_pdf_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    text_content = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # If the page contains selectable text, use it directly
        text = page.get_text()
        if text.strip():
            text_content.append(text)
        else:
            # Perform OCR on image-only pages
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            text_content.append(ocr_text)

    doc.close()
    return "\n".join(text_content)


def create_db(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            content = read_pdf_with_ocr(pdf_path)

            # Store content with metadata
            documents.append(Document(page_content=content, metadata={"source": filename}))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Add source metadata to each text chunk
    for text in texts:
        text.metadata["source"] = text.metadata.get("source", "Unknown Source")

    # Create a FAISS vector store with gemini embeddings
    vectordb = FAISS.from_documents(texts, embedding=embeddings)
    vectordb.save_local("db")
