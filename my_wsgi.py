# my_wsgi.py
def app(environ, start_response):
    from urllib.parse import parse_qs

    if environ['PATH_INFO'] == '/static/sample.html':
        response_body = open('/home/kostya/Documents/project8_hw5/static/sample.html').read()
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body.encode('utf-8')]

    # Получение параметров GET и POST
    parameters = environ.get('QUERY_STRING', '')
    if environ.get('REQUEST_METHOD') == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        post_params = parse_qs(request_body.decode('utf-8'))
    else:
        post_params = {}

    # Парсинг параметров GET
    get_params = parse_qs(parameters)

    # Формирование ответа
    response_body = []
    response_body.append('GET parameters:\n')
    for key, values in get_params.items():
        response_body.append(f'{key}: {values}\n')

    response_body.append('\nPOST parameters:\n')
    for key, values in post_params.items():
        response_body.append(f'{key}: {values}\n')

    response_body = ''.join(response_body)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]
