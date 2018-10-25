from werkzeug.wrappers import Request, Response


@Request.application
def application(request):

    ctype = request.content_type

    if ctype is None:
        ctype = 'text/html'

    if request.method == 'GET' or request.method == 'POST':

        if '/img/' in request.path:
            content = open(request.path[1:], 'rb')
        elif '.css' in request.path:
                ctype = 'text/css'
                content = open(request.path[1:], 'rb')
        elif '.html' in request.path or '.js' in request.path:
            content = open(request.path[1:], 'rb')
        else:
            content = open('mySite.html', 'rb')

        response = Response(content)
        response.status = "200 OK"
        response.status_code = 200
        response.content_type = ctype + '; charset=utf-8'
        response.content_language = 'PL'
    else:
        return Response("Tylko metody GET i POST", status="501 not impelented")

    return response


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = run_simple('0.0.0.0', 3317, application).wsgi_app()
