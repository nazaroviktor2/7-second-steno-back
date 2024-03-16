filename = "test.txt"
with open(filename, encoding="utf8") as file:
    text = file.read()

import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()
host = os.environ.get("SEARCH_ENGINE_HOST")

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts=[host],
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

document = {
    'content': text,
    'summary': ["Говорил про погоду", "Говорил про кошек"],
    'preview': "Текст про домашних животных",
    'name': "Встреча 123",
    "persons": ["Ваня", 'Федя'],
    "id": 1
}

response = client.index(
    index='orders',
    body=document,
    id='1',
    refresh=True
)
