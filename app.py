import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="CyberSec RAG Asistanı", page_icon="🛡️", layout="wide")
st.title("🛡️ Kurumsal Siber Güvenlik RAG Asistanı")
st.markdown("*Microsoft AI Innovators Project | Geliştirici: Kaan KARAKAN*")

# --- SOHBET GEÇMİŞİ (MEMORY) AYARLARI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kenar Çubuğu (Sidebar) - Doküman Yükleme
with st.sidebar:
    st.header("📂 Veri Kaynağı Yükle")
    st.markdown("Analiz edilecek siber güvenlik standartları PDF'ini yükleyin.")
    uploaded_file = st.file_uploader("PDF Dosyası Seçin", type="pdf")
    
    st.markdown("---")
    st.markdown("**Sistem Durumu:**")
    st.success("Ollama (Llama 3.2:1B) Aktif")
    st.success("HuggingFace Embeddings Aktif")
    st.success("ChromaDB Vektör Tabanı Aktif")

# --- RAG MİMARİSİ (CACHE İLE HIZLANDIRILMIŞ) ---
@st.cache_resource
def process_document(file_path, is_pdf=False):
    if is_pdf:
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
        
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    chunks = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vector_db.as_retriever(search_kwargs={"k": 3})

def build_rag_chain(retriever):
    llm = Ollama(model="llama3.2:1b")
    # Katı Prompt: Halüsinasyonu engeller
    template = """Sen uzman bir siber güvenlik asistanısın. Sadece aşağıdaki bağlamı (context) kullanarak cevap ver. 
    Eğer sorunun cevabı bağlamda yoksa kesinlikle uydurma, 'Bu bilgi sağlanan dokümanda bulunmamaktadır.' de.
    Kısa, net ve profesyonel bir Türkçe kullan.
    
    Bağlam:
    {context}
    
    Soru: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

# --- ANA İŞLEYİŞ ---
if uploaded_file is not None:
    # Kullanıcının yüklediği PDF'i geçici olarak kaydet ve işle
    with st.spinner("PDF Analiz Ediliyor ve Vektör Veritabanı Oluşturuluyor..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        retriever = process_document(tmp_file_path, is_pdf=True)
        rag_chain = build_rag_chain(retriever)
        st.sidebar.success("Doküman Başarıyla İşlendi!")
else:
    # Varsayılan olarak data.txt kullan
    retriever = process_document("data.txt", is_pdf=False)
    rag_chain = build_rag_chain(retriever)
    st.sidebar.info("Şu an varsayılan veri seti (data.txt) kullanılıyor.")

# --- SOHBET ARAYÜZÜ (CHAT UI) ---
# Önceki mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni soru al
if prompt := st.chat_input("NIST veya Azure standartları hakkında soru sorun..."):
    # Kullanıcı mesajını ekrana bas ve geçmişe ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay Zekadan cevap al
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyor..."):
            response = rag_chain.invoke(prompt)
            st.markdown(response)
    
    # Asistanın cevabını geçmişe ekle
    st.session_state.messages.append({"role": "assistant", "content": response})