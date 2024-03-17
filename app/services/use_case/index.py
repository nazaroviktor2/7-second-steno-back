def add_doc_to_index(client, text: str, summary: list[dict[str, str]], preview: str, name: str, order_id: str, persons: list[str], file_path:str):
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
