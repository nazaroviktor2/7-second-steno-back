from opensearchpy import OpenSearch

from app.core.config import config

client = OpenSearch(
    hosts=[config.SEARCH_ENGINE_HOST],
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)


def add_doc_to_index(
    text: str,
    summary: list[dict[str, str]],
    preview: str,
    name: str,
    order_id: str,
    persons: list[str],
    file_path: str
):
    document = {
        'content': text,
        'summary': summary,
        'preview': preview,
        'name': name,
        "persons": persons,
        "id": order_id,
        "file_path": file_path
    }

    response = client.index(
        index='orders',
        body=document,
        id=order_id,
        refresh=True
    )


def get_file_by_id(order_id: str):
    h_query = {
        "query": {
            "term": {
                "_id": order_id
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
    return highlight['hits']["hits"]
