from task2chunks import Documents, sentence_chunks
from lab6_search import Retriever

records = []

for doc_number, document in enumerate(Documents, start=1):
    chunks = sentence_chunks(document, 40)

    for chunk in chunks:
        records.append({
            "id": f"document{doc_number}:{chunk['id']}",
            "doc": f"document{doc_number}",
            "start": chunk["start"],
            "end": chunk["end"],
            "text": chunk["text"]
        })


queries = [
    "What happens if a student has low attendance due to sickness?",
    "Can a student submit an assignment after the deadline?",
    "How can students get help with university account problems?"
]


engine = Retriever(records, "tfidf")

for query in queries:
    print("Query:", query)

    results = engine.search(query, k=3)

    for record, score in results:
        print("Chunk ID:", record["id"])
        print("Document:", record["doc"])
        print("Score:", round(score, 3))
        print("Original Evidence:", record["text"])
        print("--------------------")