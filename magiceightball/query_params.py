QUERY_PARAMS = {
    'title': {
        'field': 'title',
        'query_type': 'eq'
    },
    'minRating': {
        'field': 'rating',
        'query_type': 'gte'
    }, 
    'maxRating': {
        'field': 'ratings',
        'query_type': 'lte'
    },
    'minVotes': {
        'field': 'votes',
        'query_type': 'gte' 
    },
    'maxVotes': {
        'field': 'votes',
        'query_type': 'lte'
    },
    'minYear': {
        'field': 'year',
        'query_type': 'gte'
    },
    'maxYear': {
        'field': 'year',
        'query_type': 'lte'
    },
    'minRuntime': {
        'field': 'runtime',
        'query_type': 'gte'
    },
    'maxRuntime': {
        'field': 'runtime',
        'query_type': 'lte'
    },
    'genre': {
        'field': 'genres',
        'query_type': 'contains'
    },
}