SYSTEM_PROMPT = """You are an enterprise knowledge assistant. Answer strictly based on the provided context chunks. If the answer is not in the context, say you do not know. Always cite the source chunk IDs you used, in the format [id]. Do not invent facts."""

QA_TEMPLATE = """Context:
{context}

Question: {question}

Answer using only the context above, with source citations like [doc::chunk-0]."""


def build_context(chunks) -> str:
    return "\n\n".join(f"[{c['id']}]\n{c['text']}" for c in chunks)


def build_prompt(question: str, chunks) -> str:
    return QA_TEMPLATE.format(context=build_context(chunks), question=question)
