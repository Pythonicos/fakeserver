import helper

helper.DOMAIN = '0.0.0.0:8080'

# CRIAR REDIRECT
# set redirect sample
helper.set_redirect_chain_from_url("redirect1.html", [
    "redirect2.html",
    "redirect3.html",
    "teste.html",  # sempre termina em um TEMPLATE ou DOWNLOAD de arquivo
])

# set arquivo
helper.set_filename_to_download("meuarquivo.txt", b'bytes do arquivo')

# set arquivo redirect
# set redirect sample
helper.set_redirect_chain_from_url("redirect-file-1.html", [
    "redirect-file-2.html",
    "redirect-file-3.html",
    "download/meuarquivo.txt",  # sempre termina em um TEMPLATE ou DOWNLOAD de arquivo
])

# mudar resposta do template
helper.set_url_to_template("teste.html", "not_found.html")


# resetar
helper.reset_mocks()
