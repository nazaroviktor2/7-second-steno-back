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

settings = {"settings": {
    "index": {
        "number_of_shards": "1",
        "analysis": {
            "filter": {
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                }
            },
            "analyzer": {
                "text_analyzer": {
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer"
                    ],
                    "char_filter": [
                        "e_mapping"
                    ],
                    "type": "custom",
                    "tokenizer": "standard"
                }
            },
            "char_filter": {
                "e_mapping": {
                    "type": "mapping",
                    "mappings": [
                        "Ё => Е",
                        "ё => е"
                    ]
                }
            }
        },
        "number_of_replicas": "1"
    }
},
    "mappings": {
        "properties": {
            "id": {
                "type": "keyword"
            },
            "persons": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }},
            "summary": {
                "type": "nested",
                "properties": {
                    "name": {
                        "type": "keyword"
                    },
                    "text": {
                        "type": "text",
                        "analyzer": "text_analyzer"
                        }
                    }

            },
            "preview": {
                "type": "text",
                "analyzer": "text_analyzer"
            },
            "name": {
                "type": "text",
                "analyzer": "text_analyzer"
            },
            "content": {
                "type": "text",
                "term_vector": "with_positions_offsets",
                "analyzer": "text_analyzer"
            }
        }
    }
}

response = client.indices.create("orders", body=settings)
print(response)
indexes = (client.indices.get_alias("*")).keys()
print([client.indices.get_mapping(index) for index in indexes])
