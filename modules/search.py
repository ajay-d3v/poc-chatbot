from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Initialize gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not in the provided context, say, 
    "The answer is not available in the context." Avoid providing incorrect information.

    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    model = ChatGroq(model="llama3-8b-8192", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def get_answer(query):
    # Load the FAISS vector store
    vectordb = FAISS.load_local("db", embeddings=embeddings, allow_dangerous_deserialization=True)

    # Retrieve relevant documents
    docs = vectordb.similarity_search(query, k=5)
    if not docs:
        return "No relevant document found for this query."

    # Use the conversational chain to generate the response
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": query}, return_only_outputs=True)

    return response["output_text"]
