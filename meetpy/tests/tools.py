# coding: utf-8

import http
from wsgiref.simple_server import make_server


# Using constants instead of https.HTTPStatus for more readable names.
# (for example 302 is HTTPStatus.FOUND)
HTTP_OK_200 = 200
HTTP_REDIRECT_302 = 302
HTTP_REDIRECT_301 = 301


def redirects(response, target):
    REDIRECT_CODES = {HTTP_REDIRECT_301, HTTP_REDIRECT_302}

    # TODO: handle redirect_chain for follow=True requests
    assert response.status_code in REDIRECT_CODES, response.status_code
    assert response.url == target
    return True


def contains(response, text):
    assert text in response.content.decode('utf-8')
    return True


def template_used(response, template_name, http_status=HTTP_OK_200):
    """
    :response: respone from django test client.
    :template_name: string with path to template.

    :rtype: bool
    """
    assert response.status_code == http_status, response.status_code
    templates = [t.name for t in response.templates if t.name]
    assert template_name in templates, templates
    return True


def serve_response(response, host='0.0.0.0', port=9876):
    """
    Useful when doing stuff with pdb -- can serve django's response with http.
    use case: looking at response in tests.
    usage: 1) serve(response),
           2) go to http://localhost:9876/
           3) PROFIT
    """

    def render(env, start_response):
        status = '%s %s' % (
            str(response.status_code),
            http.client.responses[response.status_code]
        )
        # ._headers looks like {'content-type': ('Content-Type', 'text/html')}
        # that's why we need just .values
        start_response(status, list(response._headers.values()))
        return [response.content]

    srv = make_server(host, port, render)
    print("Go to http://{}:{}".format(host, port))
    srv.serve_forever()
