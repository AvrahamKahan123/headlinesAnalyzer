import elasticsearch7


def get_instance():
    es = elasticsearch7.Elasticsearch({'host': 'localhost', 'port': 9200}, timeout=300)
    return es


def compose_index():
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0 #only 1 machine so this is pointless for now
        },

        'mappings': {
            'examplecase': {
                'properties': {
                    'title': {'index': 'analyzed', 'type': 'string'},
                    'dateTime': {'index': 'analyzed', 'format': 'yyyy-MM-dd HH:mm:ss', 'type': 'date'},
                    'people': {'index': 'analyzed', 'type': 'list'},
                    'places': {'index': 'analyzed', 'type': 'string'},
                    'otherProperNouns' :{'index': 'analyzed', 'type': 'string'}
                }}}
    }
    return request_body

if __name__ == '__main__':
    es = get_instance()
    es.indices.create(index='headlinesIndex', body=compose_index())
