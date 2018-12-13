from typing import List

import requests

DOMAIN = "0.0.0.0:8080"


def set_url_to_template(url, url_response):
    """
    wrapper for flask test app route "set"
    :param url:
    :param url_response:
    :return:
    """
    return requests.post(
        "http://" + DOMAIN + "/set/{url}?response={url_response}".format(url=url, url_response=url_response)
    )


def set_custom_page_content(custom_content, url: str = "custom.html"):
    """
    wrapper for flask test app route "set"
    :param url:
    :param custom_content:
    :return:
    """
    return requests.post(
        "http://" + DOMAIN + "/set/{url}?response={url_response}".format(url=url, url_response='custom.html'),
        files={'file': custom_content.encode()}
    )


def set_filename_to_download(filename, file_bytes):
    """
    wrapper for flask test app route "set-download"
    :param filename: file requested
    :param file_bytes: expected bytes
    :return:
    """
    return requests.post(
        "http://" + DOMAIN + "/set-download/{filename}".format(filename=filename), files={'file': file_bytes})


def set_redirect_chain_from_url(start_url: str, redirect_chain: List[str]):
    """
    Set redirect chain starting from url. Fill just the final paths, not the http://<domain>:<port>/
    Ex.: start_url='start_url.html', redirect_chain=['redirect/1', 'bb.html']
    :param start_url: initial url
    :param redirect_chain: next urls. Last url will be the page
    :return:
    """
    return requests.post(
        "http://" + DOMAIN + "/set-redirect/{start}".format(start=start_url), json=redirect_chain
    )


def reset_mocks():
    """
    wrapper for flask test app route "reset"
    :return:
    """
    return requests.post("http://" + DOMAIN + "/reset")
