from __future__ import annotations

import time
import uuid

from openai import OpenAI
from openai.types.beta import Assistant, Thread

from app.core.chat.storage import ChatStorage


instructions = """
This is a conversation with an AI assistant.
The assistant is helpful, creative, clever, and very friendly.
You are a customer support chatbot. Use your knowledge base to best respond to customer queries.
Retrieve and present detailed information from the provided text. Focus on answering questions that are asked in natural language.
"""


class ChatHandler:
    def __init__(self, *, api_key: str, model: str):
        self.model = model

        self.client = OpenAI(api_key=api_key)
        self.assistant = self.get_new_assistance()
        self.storage = ChatStorage[Thread]()
        self.timeout = 10

    def get_new_assistance(self) -> Assistant:
        return self.client.beta.assistants.create(
            instructions=instructions, model=self.model, tools=[{"type": "retrieval"}]
        )

    def _run(self, thread: Thread):
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions,
        )

        count = 0.0
        while run := self.client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        ):
            if run.status == "completed":
                yield
                break

            time.sleep(0.5)
            if count > self.timeout:
                yield "Sorry, I'm taking too long to respond. Please try again later."
                break

            count += 0.5

    def _get_response(self, thread: Thread):
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)

        response = []
        for message in messages:
            response.append(
                {"role": message.role, "text": message.content[-1].text.value}
            )
        return response

    def get_response(self, *, session_id: str | None = None, message: str):
        if session_id is None and session_id not in self.storage:
            return self.create_chat(message)

        if session_id is None:
            raise ValueError("Session ID is required")

        thread = self.storage.get(session_id)
        next(self._run(thread))
        response = self._get_response(thread)
        return {"session_id": session_id, "response": response}

    def create_chat(self, message: str) -> str:
        new_session_id = self.create_session()
        thread = self.client.beta.threads.create()

        self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=message
        )

        self.storage.add(new_session_id, thread)
        return new_session_id

    @staticmethod
    def create_session() -> str:
        return uuid.uuid4().hex
