import os
import pandas as pd
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings, VertexAI
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.docstore.document import Document

from src.utils.formatting import format_rag_response

class RAGEngine:
    def __init__(self, project_id="your-project-id", location="us-central1"):
        self.mock_mode = False
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        # Try initializing Vertex AI or Google GenAI
        api_key = os.environ.get("GOOGLE_API_KEY")
        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if api_key:
            try:
                print("Found GOOGLE_API_KEY. Initializing Google GenAI...")
                from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
                self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
                self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", google_api_key=api_key)
                print("Google GenAI initialized successfully (Gemini 2.0 Flash).")
            except Exception as e:
                print(f"Google GenAI initialization failed: {e}. Switching to MOCK mode.")
                self.mock_mode = True
                self.embeddings = None
                self.llm = None

        elif creds_path:
            try:
                print("Found GOOGLE_APPLICATION_CREDENTIALS. Initializing Vertex AI...")
                self.embeddings = VertexAIEmbeddings(model_name="text-embedding-004")
                self.llm = VertexAI(model_name="gemini-1.5-flash-001")
                print("Vertex AI initialized (lazy connection).")
            except Exception as e:
                print(f"Vertex AI connection failed: {e}. Switching to MOCK mode.")
                self.mock_mode = True
                self.embeddings = None
                self.llm = None
        else:
            print("No credentials found (GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS). Defaulting to MOCK mode.")
            self.mock_mode = True
            self.embeddings = None
            self.llm = None

    def ingest_data(self, df, text_col='clean_text'):
        print("Ingesting data into RAG system...")
        
        documents = []
        for idx, row in df.iterrows():
            # Use content preview as source if title not available
            content = str(row.get(text_col, row.get('content', '')))
            
            # Try to get a meaningful source name
            if 'title' in row and pd.notna(row['title']):
                source = str(row['title'])
            elif 'content' in row:
                # Use first 50 chars of content as title
                source = str(row['content'])[:50] + "..."
            else:
                source = content[:50] + "..."
            
            doc = Document(
                page_content=content, 
                metadata={
                    "source": source,
                    "category": str(row.get('category', 'General'))
                }
            )
            documents.append(doc)
            
        chunks = self.text_splitter.split_documents(documents)
        
        if self.mock_mode:
            self.vector_store = "MockStore"
            self.chunks = chunks
        else:
            try:
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            except Exception as e:
                print(f"Vector store creation failed: {e}")
                self.mock_mode = True
                self.chunks = chunks
            
        print(f"Ingested {len(chunks)} chunks.")

    def search(self, query, k=3):
        if self.mock_mode:
            return self._mock_search(query, k)
        
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            print(f"Vector search failed: {e}. Switching to MOCK mode.")
            self.mock_mode = True
            return self._mock_search(query, k)

    def _mock_search(self, query, k):
        results = []
        for doc in self.chunks:
            if any(word in doc.page_content.lower() for word in query.lower().split()):
                results.append(doc)
                if len(results) >= k:
                    break
        if not results:
            results = self.chunks[:k]
        return results

    def generate_answer(self, query, docs):
        # Handle greetings explicitly in mock mode
        greetings = ['hi', 'hello', 'hey', 'greetings']
        if self.mock_mode and any(g in query.lower().split() for g in greetings):
            return "Hello! I am currently running in Mock Mode because I couldn't connect to Vertex AI. I can still search the loaded news dataset for you. Try asking about 'technology', 'sports', or 'finance'!"

        context = "\\n\\n".join([d.page_content for d in docs])
        
        if self.mock_mode:
            # Improve mock response to be more descriptive
            return f"[MOCK] I found some relevant news articles. One source mentions: '{docs[0].page_content[:150]}...'. (Note: Connect Vertex AI for full synthesis)."
            
        prompt = f"""You are an intelligent News Agent assistant powered by Gemini.

Context from News Database:
{context}

User Question: {query}

Instructions:
1. Answer the user's question using the Context provided above
2. Be specific and reference the news articles when relevant
3. If the Context contains relevant information, USE IT to answer
4. Keep your answer concise and helpful

Answer:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"LLM generation failed: {e}. Switching to MOCK mode.")
            self.mock_mode = True
            return f"[MOCK (Fallback)] Based on the retrieved documents, here is a summary for '{query}': {docs[0].page_content[:100]}..."

    def process_query(self, query):
        # This method is for CLI usage, returns formatted print
        # For API, we will use search() and generate_answer() directly
        print(f"Processing RAG query: {query}")
        docs = self.search(query)
        answer = self.generate_answer(query, docs)
        
        retrieved_items = [{"source": d.metadata.get('source', 'Unknown'), "score": 0.95} for d in docs]
        
        format_rag_response(
            query=query,
            retrieved_items=retrieved_items,
            summary=answer[:100] + "...",
            final_answer=answer
        )
        return answer
