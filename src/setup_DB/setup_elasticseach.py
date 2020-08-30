import elasticsearch7


def get_instance():
    es_instance = elasticsearch7.Elasticsearch({'host': 'localhost', 'port': 9200}, timeout=300)
    return es_instance


def compose_headlines_index():
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0 #only 1 machine so this is pointless for now
        },

        'mappings': {
            'document_fields': {
                'properties': {
                    'ident': {'index': 'not_analyzed', 'type': 'int'}, # to avoid confusion with id of document
                    'title': {'index': 'analyzed', 'type': 'string'},
                    'organizations': {'index': 'analyzed', 'type': 'string'},
                    'people': {'index': 'analyzed', 'type': 'string'},
                    'places': {'index': 'analyzed', 'type': 'string'}
                }}}
    }
    return request_body


def compose_topic_index():
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0  # only 1 machine so this is pointless for now
        },

        'mappings': {
            'document_fields': {
                'properties': {
                    'ident': {'index': 'not_analyzed', 'type': 'int'},
                    'keywords': {'index': 'analyzed', 'type': 'string'},
                }}}
    }
    return request_body


if __name__ == '__main__':
    es = get_instance()
    es.indices.create(index='headlinesIndex', body=compose_headlines_index())
    es.indices.create(index='topicsIndex', body=compose_headlines_index())

