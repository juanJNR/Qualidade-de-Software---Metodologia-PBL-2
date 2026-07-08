class CarrinhoPage:
    def __init__(self, page):
        self.page = page

    def abrir(self):
        self.page.get_by_test_id("cart-icon").click()

    def finalizar_pedido(self):
        self.page.get_by_text("Finalizar Pedido").click()

    def item_presente(self, nome_item: str) -> bool:
        return self.page.get_by_text(nome_item).is_visible()
