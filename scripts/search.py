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

query = {
    "query": {
        "bool": {
            "should": [
                {"match": {"content": "добрый день"}},
                {"match": {"content": "эфир"}}
            ],
            "minimum_should_match": 1
        }
    },
    "highlight": {
        "fields": {
            "content": {}
        },
        "pre_tags": ["<em>"],
        "post_tags": ["</em>"],
        "highlight_query": {
            "match": {
                "content": "добрый день"
            }
        }
    }
}

# # Выполнение поискового запроса
# response = client.search(index="orders", body=query)
# print(response)
#
#
# # Обработка результатов
# for hit in response["hits"]["hits"]:
#     print(hit["highlight"])


h_query = {
    "query": {
        "term": {
            "_id": "1"
        }
    },
    "highlight": {
        "fields": {
            "content": {
                "highlight_query": {
                    "match": {
                        "content": "эфир"
                    }
                }
            }
        },
        "fragment_size": 150,
        "pre_tags": ["<em>"],
        "post_tags": ["</em>"]
    },
    "_source": False,
    "size": 1
}

highlight = client.search(index="orders", body=h_query)
print(highlight['hits'])
