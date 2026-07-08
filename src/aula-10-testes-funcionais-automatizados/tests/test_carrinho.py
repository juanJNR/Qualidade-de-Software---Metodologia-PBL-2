from pages.restaurante_page import RestaurantePage
from pages.carrinho_page import CarrinhoPage


def test_adicionar_item_ao_carrinho(page):
    restaurante = RestaurantePage(page)
    carrinho = CarrinhoPage(page)

    restaurante.acessar()
    restaurante.abrir_restaurante("Restaurante Sabor Caseiro")
    restaurante.adicionar_item("Feijoada Completa")

    carrinho.abrir()
    assert carrinho.item_presente("Feijoada Completa")
