import os
import subprocess
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
import logging
from PyPDF2 import PdfReader  # Update the import statement
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
from PyPDF2 import PdfReader
from PyPDF2 import PdfReader

class PdfExtractMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'pdf-text-extraction'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling PDF text extraction: {message}")

        pdf_path = message.content

        if not pdf_path:
            error_message = "Invalid PDF path"
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": error_message,
            })
            logger.error(error_message)
            message_store.add_message(response_message)
            return

        logger.info(f"Extracting text from PDF: {pdf_path}")

        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()  # Update this line

                response_message = Message({
                    "message_type": "response",
                    "extracted_text": text,
                })
                logger.info(f"Adding response message to store: {response_message.to_dict()}")
                message_store.add_message(response_message)
        except Exception as e:
            error_message = f"Failed to extract text from PDF: {str(e)}"
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": error_message,
            })
            logger.error(error_message)
            message_store.add_message(response_message)

    @classmethod
    def get_examples(cls):
        return [
       #     {"message_type": "pdf-text-extraction", "content": "./handlers/pdf_files/0335354008_60373195_2023-03-23_U.pdf"},
        #    {"message_type": "pdf-text-extraction", "content": "./handlers/pdf_files/1234567890_98765432_2023-04-15_V.pdf"}
        ]
