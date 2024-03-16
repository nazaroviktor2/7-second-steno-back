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

q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

indexes = (client.indices.get_alias("*")).keys()
print([client.indices.get_mapping(index) for index in indexes])
