(Bu proje, Microsoft AI Innovators yaz stajı programı kapsamında, sıfırdan modern Üretken Yapay Zeka (GenAI) mimarileri ve RAG sistemleri öğrenilerek geliştirilmiştir. Geliştirme sürecinde sektörel standartlara uyum sağlamak amacıyla AI asistanlarından mimari destek alınmıştır.)

# 🛡️ Kurumsal Siber Güvenlik RAG Asistanı

**Microsoft AI Innovators Project**

Bu proje, kurumsal siber güvenlik standartlarını (NIST, OWASP, Azure Cloud Security) temel alarak geliştirilmiş, %100 yerel çalışan ve veri gizliliğini merkeze alan bir RAG (Retrieval-Augmented Generation) yapay zeka asistanıdır.

---

## 🎬 Proje Sunum Videosu

Projenin canlı demosunu, kod mimarisini ve detaylı sunumunu izlemek için aşağıdaki bağlantıya tıklayabilirsiniz:

👉 [YouTube Üzerinden Sunumu İzlemek İçin Tıklayın](https://www.youtube.com/watch?v=Cl1EERGzSfY)

---

## 🚀 Proje Vizyonu ve Amacı

Şirketlerin hassas siber güvenlik mimarilerini ve iç yönergelerini bulut tabanlı (OpenAI vb.) modellere yüklemek ciddi bir veri ihlali riskidir. Bu proje, hiçbir veriyi internete çıkarmadan, tamamen yerel makinede çalışan bir LLM ile şirket içi dokümanların güvenle sorgulanabilmesini sağlar.

---

## 🧠 Kullanılan Teknolojiler (Tech Stack)

* **LLM (Büyük Dil Modeli):** Llama 3.2 (3B Parametre) - Ollama üzerinden yerel çalıştırıldı.
* **Orkestrasyon:** LangChain (LCEL Mimarisi)
* **Vektör Veritabanı:** ChromaDB
* **Gömme (Embedding) Modeli:** HuggingFace (`all-MiniLM-L6-v2`)
* **Arayüz (UI):** Streamlit (Session State ile Chatbot deneyimi)
* **Veri İşleme:** `PyPDFLoader`, `RecursiveCharacterTextSplitter`

---

## 🎯 Öne Çıkan Özellikler

* **Tamamen Yerel ve Güvenli (Air-gapped):** Veriler dış sunuculara gitmez.
* **Dinamik PDF Analizi:** Kullanıcılar kendi siber güvenlik yönergelerini (PDF) arayüzden yükleyip anında sorgulayabilir.
* **Anti-Halüsinasyon (Strict Prompting):** Model, yalnızca sağlanan bağlam (context) üzerinden cevap verecek şekilde kısıtlanmıştır. Bağlam dışı sorularda uydurma yapmaz.
* **Hafızalı Sohbet (Chat History):** Önceki soruları ekranda tutarak kesintisiz bir deneyim sunar.

---

## ⚙️ Kurulum ve Çalıştırma

```bash
# 1. Gerekli kütüphaneleri yükleyin
pip install streamlit langchain langchain-community langchain-chroma langchain-huggingface pypdf sentence-transformers

# 2. Ollama'yı kurup modeli çekin
ollama pull llama3.2

# 3. Uygulamayı başlatın
streamlit run app.py