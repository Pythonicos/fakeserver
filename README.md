### ROTAS PARA CONFIGURAÇÃO

##### TEMPLATES:

esses são os templates que já existem

* http://0.0.0.0:8080/not_found.html


### APONTANDO SERVER

> helper.DOMAIN = '0.0.0.0:8080'

#### ACOMPANHAR OS MOCKS EXISTENTES

ACESSE http://0.0.0.0:8080 os downloads e redirects configurados

#### RESETAR CONFIGURAÇÕES

> helper.reset_mocks()

#### MUDAR TEMPLATE DE RESPOSTA
ao acessar teste.html ele responde not_found.html (sem redirect)

> helper.set_url_to_template("teste.html", "not_found.html")

#### CRIAR REDIRECT

> helper.set_redirect_chain_from_url("redirect1.html", [
        "redirect2.html",
        "redirect3.html",
        "teste.html"
    ])  # sempre termina em um TEMPLATE ou DOWNLOAD de arquivo

#### CRIAR DOWNLOAD DE ARQUIVO

> helper.set_filename_to_download("nomedoarquivo.txt", b'bytes do arquivo')
