import elasticsearch7

def get_instance():
    es = elasticsearch7.Elasticsearch({'host': 'localhost', 'port': 9200}, timeout=300)
    return es

def compose_index():
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },

        'mappings': {
            'examplecase': {
                'properties': {
                    'title': {'index': 'analyzed', 'type': 'string'},
                    'dateAndTime': {'index': 'not_analyzed', 'format': 'dateOptionalTime', 'type': 'date'},
                    'people': {'index': 'analyzed', 'type': 'list'},
                    'countries': {'index': 'not_analyzed', 'type': 'string'},
                }}}
    }
    return request_body

if __name__ == '__main__':
    es = get_instance()
    es.indices.create(index='headlinesIndex', body=compose_index())
