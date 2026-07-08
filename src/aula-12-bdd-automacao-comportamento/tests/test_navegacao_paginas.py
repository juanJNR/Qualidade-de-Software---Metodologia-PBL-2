from pytest_bdd import scenarios, given, when, then

scenarios('../features/navegacao_paginas.feature')


@given('que o usuário está na página inicial do LocalEats')
def acessar_pagina_inicial(page):
    page.goto('https://local-eats-unisenac.vercel.app/')


@when('ele clica no menu "Favoritos"')
def clicar_favoritos(page):
    page.get_by_text('Favoritos').click()


@then('o sistema deve exibir a página de restaurantes favoritados')
def validar_pagina_favoritos(page):
    assert page.get_by_text('Meus Favoritos').is_visible()
