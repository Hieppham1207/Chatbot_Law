from docx import Document
doc = Document("law_rule.docx")

full_text = []
for para in doc.paragraphs:
    full_text.append(para.text)
text = "\n".join(full_text)
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
def split_by_articles_with_metadata(text):
    parts = re.split(r"(Điều \d+\.?.*)", text)

    articles = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i+1].strip()

        articles.append({
            "title": title,
            "content": content
        })

    return articles


def chunk_articles_with_metadata(articles, chunk_size=500, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    final_chunks = []

    for article in articles:
        title = article["title"]
        content = article["content"]

        full_text = title + "\n" + content

        if len(full_text) <= chunk_size:
            final_chunks.append({
                "text": full_text,
                "title": title
            })
        else:
            small_chunks = splitter.split_text(full_text)

            for chunk in small_chunks:
                final_chunks.append({
                    "text": chunk,
                    "title": title
                })

    return final_chunks
articles_meta = split_by_articles_with_metadata(text)

# # 2. Chunk nhỏ lại
chunks_meta = chunk_articles_with_metadata(articles_meta)
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
texts = [c["text"] for c in chunks_meta]
embed_docs = model.encode(texts)
dim = embed_docs.shape[1]
faiss.normalize_L2(embed_docs)
index = faiss.IndexFlatIP(dim)
index.add(embed_docs)
def retrieve(query, k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)

    results = []
    for i in indices[0]:
        results.append(chunks_meta[i])

    return results
import google.generativeai as genai
genai.configure(api_key= "AIzaSyA4EckDDG_GjXDcAIGQc-pZ_m7IfpyMqO4")

def call_llm(query, context):
    prompt = f"""
        Dựa vào thông tin sau:
        {context}

        Trả lời câu hỏi:
        {query}
        """

    model_gg = genai.GenerativeModel("gemini-2.5-flash")
    result = model_gg.generate_content(prompt)
    return result.text

def chatbot(query):
    docs = retrieve(query)

    context = "\n".join([doc["text"] for doc in docs])

    answer = call_llm(query, context)

    return answer,docs