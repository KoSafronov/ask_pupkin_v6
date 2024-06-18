def application(env, start_responce):
    start_responce('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]
