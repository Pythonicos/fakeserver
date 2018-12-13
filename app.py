"""
Test server
"""
import io
import os
from flask import Flask, jsonify, abort
from flask import Response
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory


def handle_response(code=None, message=None):
    return Response(status=code, response=message)


def handle_redirect(url):
    return redirect(url)


BEHAVIORS = {
    'custom': handle_response,
    'redirect': handle_redirect
}


def generate(file_bytes):
    """
    return a generator that iter from file_byte lines
    :param file_bytes:
    """
    io_bytes = io.BytesIO(file_bytes)
    line = io_bytes.readline()
    while line:
        yield line
        line = io_bytes.readline()


def create_app():
    """
    Create test server
    :return:
    """
    app = Flask(__name__)

    def start_mocks():
        """
        Start all configs with a cleaned dict
        """
        app.config.page = {}
        app.config.download = {}
        app.config.redirect = {}

    start_mocks()

    @app.route('/')
    def home():
        """
        return all tests routes and current mock state
        :return:
        """
        list_route = [
            ('/<template>?[status=<status_code>]', 'return static template file. Use /set to custom response'),
            ('/set/<url>?response=<new_response>', 'mock return of /<template>.'),
            ('/set-redirect/<start_url>', 'Define redirect chain from start url.'),
            ('/download/<filename>', 'return pre-defined file. Use /set-download/<filename to define file'),
            ('/stream/<filename>', 'return pre-defined file as stream. Use /set-download/<filename to define file'),
            ('/set-download/<filename> (POST)', 'mock return of /download/<filename>'),
            ('/reset', 'clean all mocks)'),
            ('CURRENT MOCKS', [{'page': app.config.page, 'download': list(app.config.download.keys())}]),
            ('CURRENT REDIRECTS', {'redirects': app.config.redirect}),
        ]

        return jsonify(list_route), 200

    @app.route('/favicon.ico')
    def favicon():
        """
        Browsers request favicon.ico for default. This route was created to avoid not found error
        :return:
        """
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    @app.route('/reset', methods=('POST', ))
    def reset_template():
        """
        Clean "to from" response page, download and redirects
        :return:
        """
        start_mocks()

        return "", 200

    @app.route('/<template_file>')
    def template(template_file):
        """
        request ex.: http://localhost:8080/<template>
        :return:
        """
        behavior, *args = request.headers.get('behavior', '').split(';')
        # 'behavior': 'error;500'
        # 'behavior': 'redirect;url'
        if behavior:
            return BEHAVIORS[behavior](*args)

        status = request.args.get('status')
        if template_file in app.config.redirect:
            return redirect(app.config.redirect[template_file])

        response_url, context = app.config.page.get(template_file) and app.config.page[template_file] or (None, {})

        if response_url:
            return render_template(response_url, **context), status or 200
        return render_template(template_file, **context), status or 201

    @app.route('/set/<url>', methods=('POST', ))
    def set_url(url):
        """
        Mock /<template>
        When "url" be requested, return "response_url"
        :param url: template name requested
        :return:
        """
        if url == "custom.html":
            app.config.page[url] = ("custom.html", {'custom': b''.join(request.files.get('file')).decode()})
        else:
            app.config.page[url] = (request.args.get('response'), {})

        return "Ok", 201

    @app.route('/set-redirect/<start_url>', methods=("POST", ))
    def set_redirect(start_url: str):
        """
        Create redirect chain. Last url needs to be template path
        Expected json: ["/redirect/<url1>", "/redirect/<url2>", ..., "/redirect/<urlN>", "/<template_file>]
        :param start_url: url that start redirect
        :return:
        """

        try:
            request.json.insert(0, start_url)
        except:
            raise Exception("Json not an List of strings")
        else:
            for i, url in enumerate(request.json):
                try:
                    app.config.redirect[url] = request.json[i + 1]
                except IndexError:
                    pass

            return "Ok", 201

    @app.route('/download/<filename>')
    def download(filename):
        """
        request a file with filename
        :param filename:
        :return:
        """
        file_byte = app.config.download.get(filename)
        headers = {'Content-Disposition': 'attachment; filename={filename}'.format(filename=filename)}
        if not file_byte:
            file_byte = b'Text test byte  test byte\ntest byte  test byte \ntest byte  test\n' * 1024 * 10**2
        return make_response(file_byte, headers)

    @app.route('/stream/<filename>')
    def download_stream(filename):
        """
        Mock /<download> route. Expected file uploaded
        :param filename:
        :return:
        """
        file_byte = app.config.download.get(filename)
        headers = {'Content-Disposition': 'attachment; filename={filename}'.format(filename=filename)}
        if not file_byte:
            file_byte = b'Text test byte  test byte\ntest byte  test byte \ntest byte  test\n' * 1024 * 10**2

        return Response(generate(file_byte), headers=headers, status=200)

    @app.route('/set-download/<filename>', methods=('POST', ))
    def set_download_route(filename):
        """
        Mock /[download|stream]/<filename>
        :param filename:
        :return:
        """
        first_file = list(request.files.keys())[0]
        file_byte = request.files[first_file]
        app.config.download[filename] = b''.join(file_byte)

        return "Ok", 201

    @app.route('/response/unauthorized')
    def unauthorized():
        """
        return a response with 401 status code
        :return:
        """
        response = Response('Access Denied', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        response.set_cookie('session_id', 'eyJ1c2VybmFtZSI6IlBhZ2RXZWJTZXJ2aWNlIn0.DcJd4Q.hVeHhePQT_TK1qANXDAX8oVLmC0')
        return response

    app.run('0.0.0.0', port=8080)


if __name__ == '__main__':
    create_app()
