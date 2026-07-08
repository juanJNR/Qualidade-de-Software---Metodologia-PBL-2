from pages.restaurante_page import RestaurantePage
from pages.carrinho_page import CarrinhoPage


def test_finalizar_pedido_com_sucesso(page):
    restaurante = RestaurantePage(page)
    carrinho = CarrinhoPage(page)

    restaurante.acessar()
    restaurante.abrir_restaurante("Restaurante Sabor Caseiro")
    restaurante.adicionar_item("Feijoada Completa")

    carrinho.abrir()
    carrinho.finalizar_pedido()

    assert page.get_by_text("Pedido realizado com sucesso").is_visible()
