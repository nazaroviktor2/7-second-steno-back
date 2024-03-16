import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch
load_dotenv()
host = os.environ.get("SEARCH_ENGINE_HOST")

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts=[host],
    http_compress=True, # enables gzip compression for request bodies
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)


response = client.indices.delete(
    index='orders'
)
