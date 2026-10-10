from typing import List, Optional

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_TEMPERATURE
from app.llm.prompts import SYSTEM_PROMPT


class LLMClient:
    def __init__(self, api_key: str = LLM_API_KEY, base_url: str = LLM_BASE_URL, model: str = LLM_MODEL) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.mock = not api_key

    def chat(self, question: str, context: str, history: Optional[List[dict]] = None) -> str:
        if self.mock:
            return self._mock_answer(question, context)
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(history or [])
            messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"})
            resp = client.chat.completions.create(
                model=self.model, messages=messages, temperature=LLM_TEMPERATURE
            )
            return resp.choices[0].message.content or ""
        except Exception as exc:
            return f"[llm-error] {exc}"

    @staticmethod
    def _mock_answer(question: str, context: str) -> str:
        if not context.strip():
            return "No context provided. (mock mode: set LLM_API_KEY to enable real answers.)"
        first_id = context.split("]", 1)[0].lstrip("[").strip()
        snippet = context.replace("\n", " ")[:180]
        return (
            f"Based on the retrieved context (mock mode — set LLM_API_KEY in .env for real LLM answers), "
            f"the question relates to: {snippet}... [Source: {first_id}]"
        )
