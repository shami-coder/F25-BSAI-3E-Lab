
import re

document1 = """
University Attendance Policy

Students are expected to attend all scheduled classes regularly. Attendance is important because it helps students understand lectures and complete their coursework. The university requires students to maintain at least 75 percent attendance in each subject. Students who have less than 75 percent attendance may not be allowed to appear in the final examination.

Teachers are responsible for recording student attendance in every class. Students should check their attendance records regularly and report any mistakes to their teachers.

If a student is absent because of illness, the student should provide valid medical evidence to the department. The department may consider the medical reason, but medical evidence does not automatically remove the attendance shortage. In special cases, the department can review the student's situation and make a decision according to university rules.

Students should arrive on time and avoid unnecessary absences. Attendance records are maintained by the department throughout the semester.
"""

document2 = """
Assignment Submission Policy

Students must submit their assignments through the university learning portal before the given deadline. Every assignment has a specific submission date announced by the teacher. Students should upload their work in the required file format and check that the uploaded file is correct.

Late assignments may receive a penalty according to the course policy. Students are responsible for checking the submission status after uploading their work. If the portal shows an error, students should inform their teacher or the IT help desk.

If a student faces a serious medical emergency or a technical problem with the university portal, the teacher may allow an extension after reviewing the evidence. However, an extension is not automatic, and students must contact the teacher as soon as possible.

Teachers should clearly explain assignment requirements, deadlines, marking criteria, and accepted file formats. Students should avoid waiting until the last minute to upload their assignments.
"""

document3 = """
University IT Help Desk

The university IT help desk provides technical support to students and staff. Students can contact the help desk if they have problems with their university accounts, learning portal, email, or computer systems. The help desk normally operates from Monday to Saturday, between 9 AM and 5 PM.

Students should provide their registration number and a clear explanation of the problem when requesting support. For password problems, students can use the password recovery option on the login page. If the recovery option does not work, they should contact the IT help desk for further assistance.

The help desk usually responds to normal requests during working hours. However, urgent problems that affect online examinations or important university services may receive priority, even when the normal support schedule is busy.

Students should never share their passwords with other people. Staff members are responsible for protecting student account information and maintaining the university's computer systems.
"""

Documents = [
    document1,
    document2,
    document3
]


def word_location(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def sentence_location(text):
    sentences = []

    for m in re.finditer(r'[^.!?]+[.!?]?', text):
        sentences.append((m.start(), m.end()))

    return sentences


def create_chunks(text, size=40, overlap=0):
    position = word_location(text)
    chunks = []

    if overlap < 0 or overlap >= size:
        raise ValueError("Invalid overlap")

    step = size - overlap

    for i in range(0, len(position), step):
        start = position[i][0]
        end = position[min(i + size, len(position)) - 1][1]

        chunks.append({
            "id": len(chunks) + 1,
            "start": start,
            "end": end,
            "text": text[start:end]
        })

        if i + size >= len(position):
            break

    return chunks


def sentence_chunks(text, budget=40):
    sentences = sentence_location(text)
    chunks = []
    current_chunk = ""
    count = 0
    chunk_start = None
    chunk_end = None

    for start, end in sentences:
        sentence = text[start:end]
        words = len(sentence.split())

        if words > budget:
            if current_chunk:
                chunks.append({
                    "id": len(chunks) + 1,
                    "start": chunk_start,
                    "end": chunk_end,
                    "text": current_chunk
                })

            current_chunk = ""
            count = 0
            chunk_start = None
            chunk_end = None

            word_spans = word_location(sentence)

            for i in range(0, len(word_spans), budget):
                s = word_spans[i][0]
                e = word_spans[min(i + budget, len(word_spans)) - 1][1]

                chunks.append({
                    "id": len(chunks) + 1,
                    "start": start + s,
                    "end": start + e,
                    "text": sentence[s:e]
                })

            continue

        chunk_start = start if chunk_start is None else chunk_start

        if count + words <= budget:
            current_chunk += sentence
            chunk_end = end
            count += words
        else:
            if current_chunk:
                chunks.append({
                    "id": len(chunks) + 1,
                    "start": chunk_start,
                    "end": chunk_end,
                    "text": current_chunk
                })

            current_chunk = sentence
            count = words
            chunk_start = start
            chunk_end = end

    if current_chunk:
        chunks.append({
            "id": len(chunks) + 1,
            "start": chunk_start,
            "end": chunk_end,
            "text": current_chunk
        })

    return chunks


if __name__ == "__main__":

    print("Document 1 Words:", len(document1.split()))
    print("Document 2 Words:", len(document2.split()))
    print("Document 3 Words:", len(document3.split()))

    print(len(Documents))

    print(word_location("My university is here"))

    print(sentence_location("My university is here. I study AI."))

    chunks = create_chunks(document1, 40, 0)

    print("Total Chunks:", len(chunks))

    for chunk in chunks:
        print("ID:", chunk["id"])
        print("Start:", chunk["start"])
        print("End:", chunk["end"])
        print("Text:", chunk["text"])
        print("----------------")

    chunks = create_chunks(document1, 40, 10)

    print("Total Chunks:", len(chunks))

    for chunk in chunks:
        print("ID:", chunk["id"])
        print("Start:", chunk["start"])
        print("End:", chunk["end"])
        print("Text:", chunk["text"])
        print("----------------")

    chunks = sentence_chunks(document1, 40)

    print("Total Sentence Chunks:", len(chunks))

    for chunk in chunks:
        print("ID:", chunk["id"])
        print("Start:", chunk["start"])
        print("End:", chunk["end"])
        print("Words:", len(chunk["text"].split()))
        print("Text:", chunk["text"])
        print("-------------------")

    long_sentence = " ".join(["University"] * 50) + "."

    long_chunks = sentence_chunks(long_sentence, 40)

    for chunk in long_chunks:
        print("Words:", len(chunk["text"].split()))
        print("Text:", chunk["text"])

    empty_chunks = sentence_chunks("", 40)
    print(empty_chunks)

    short_chunks = sentence_chunks("AI is useful. It helps students.", 40)

    for chunk in short_chunks:
        print(chunk)

    try:
        create_chunks(document1, 40, 40)
    except ValueError as error:
        print(error)

    for document in Documents:
        print("Overlap 0:", len(create_chunks(document, 40, 0)))
        print("Overlap 10:", len(create_chunks(document, 40, 10)))
        print("Sentence Aware:", len(sentence_chunks(document, 40)))
        print("-------------------")

    c0 = create_chunks(document1, 40, 0)
    c10 = create_chunks(document1, 40, 10)

    print("Overlap 0:", sum(len(c["text"]) for c in c0))
    print("Overlap 10:", sum(len(c["text"]) for c in c10))

    for chunk in sentence_chunks(document1, 40):
        if "medical evidence" in chunk["text"]:
            print("Chunk ID:", chunk["id"])
            print(chunk["text"])

    for chunk in sentence_chunks(document2, 40):
        if "extension" in chunk["text"]:
            print("Chunk ID:", chunk["id"])
            print(chunk["text"])
            print("----------------")

    for chunk in sentence_chunks(document3, 40):
        if "urgent" in chunk["text"]:
            print("Chunk ID:", chunk["id"])
            print(chunk["text"])

    text = "Dr. Ahmed teaches AI. Mr. Ali studies CS."

    print(sentence_location(text))
    
    print("\n===== CHUNK SIZE COMPARISON =====")

    for document in Documents:

        c0 = create_chunks(document, 40, 0)
        c10 = create_chunks(document, 40, 10)
        cs = sentence_chunks(document, 40)

        print("\nOverlap 0:")
        for c in c0:
            print(len(c["text"].split()))

        print("Overlap 10:")
        for c in c10:
            print(len(c["text"].split()))

        print("Sentence Aware:")
        for c in cs:
            print(len(c["text"].split()))

    print("\n===== REPEATED TEXT COMPARISON =====")

    for document in Documents:

        c0 = create_chunks(document, 40, 0)
        c10 = create_chunks(document, 40, 10)

        print("\nOverlap 0 Chunks:", len(c0))
        print("Overlap 10 Chunks:", len(c10))

        print("Overlap 0 Total Words:",
              sum(len(c["text"].split()) for c in c0))

        print("Overlap 10 Total Words:",
              sum(len(c["text"].split()) for c in c10))

        print("Repeated Words:",
              sum(len(c["text"].split()) for c in c10)
              - sum(len(c["text"].split()) for c in c0))

    print("\n===== RULE AND EXCEPTION CHECK =====")

    chunks = sentence_chunks(document1, 40)

    for chunk in chunks:
        if "75 percent attendance" in chunk["text"]:
            print("Attendance Rule: Found in Chunk", chunk["id"])

        if "medical evidence" in chunk["text"]:
            print("Medical Exception: Found in Chunk", chunk["id"])

    chunks = sentence_chunks(document2, 40)

    for chunk in chunks:
        if "before the given deadline" in chunk["text"]:
            print("Assignment Rule: Found in Chunk", chunk["id"])

        if "serious medical emergency" in chunk["text"]:
            print("Assignment Exception: Found in Chunk", chunk["id"])

    chunks = sentence_chunks(document3, 40)

    for chunk in chunks:
        if "9 AM and 5 PM" in chunk["text"]:
            print("Help Desk Rule: Found in Chunk", chunk["id"])

        if "urgent problems" in chunk["text"]:
            print("Urgent Exception: Found in Chunk", chunk["id"])