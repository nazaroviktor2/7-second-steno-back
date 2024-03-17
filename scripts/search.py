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
      "_id": "3688f681-4596-471b-809f-cdb02c50d868"
    }
  },
  "highlight": {
    "fields": {
      "content": {
        "highlight_query": {
          "bool": {
            "should": [
              {"match": {"content": "выполни"}},
              {"match": {"content": "осуществи"}},
              {"match": {"content": "согласуй"}},
              {"match": {"content": "организуй"}},
              {"match": {"content": "нагенерируй"}},
              {"match": {"content": "придумай"}},
              {"match": {"content": "настрой"}},
              {"match": {"content": "реализуй"}},
              {"match": {"content": "обеспечи"}},
              {"match": {"content": "создай"}},
              {"match": {"content": "построй"}},
              {"match": {"content": "сконструируй"}},
              {"match": {"content": "сформируй"}},
              {"match": {"content": "обеспечь"}}
            ]
          }
        }
      }
    },
    "fragment_size": 150,
    "pre_tags": ["<em>"],
    "post_tags": ["</em>"]
  },
  "_source": True,
  "size": 1
}

highlight = client.search(index="orders", body=h_query)
print(highlight['hits']["hits"])
