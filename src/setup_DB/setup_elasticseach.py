import elasticsearch7


def get_instance():
    es = elasticsearch7.Elasticsearch({'host': 'localhost', 'port': 9200}, timeout=300)
    return es


def compose_headlines_index():
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0 #only 1 machine so this is pointless for now
        },

        'mappings': {
            'examplecase': {
                'properties': {
                    'title': {'index': 'analyzed', 'type': 'string'},
                    'id': {'index': 'not_analyzed', 'type': 'int'},
                }}}
    }
    return request_body


def compose_cluster_index():
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0  # only 1 machine so this is pointless for now
        },

        'mappings': {
            'examplecase': {
                'properties': {
                    'titles': {'index': 'analyzed', 'type': 'string'},
                    'keywords': {'index': 'analyzed', 'type': 'string'},
                    'ids': {'index': 'not_analyzed', 'type': 'int'},
                }}}
    }
    return request_body


if __name__ == '__main__':
    es = get_instance()
    es.indices.create(index='headlinesIndex', body=compose_headlines_index())
    es.indices.create(index='clustersIndex', body=compose_headlines_index())

