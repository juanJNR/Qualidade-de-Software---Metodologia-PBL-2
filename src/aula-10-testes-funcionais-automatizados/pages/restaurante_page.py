class RestaurantePage:
    def __init__(self, page):
        self.page = page

    def acessar(self):
        self.page.goto("https://local-eats-unisenac.vercel.app/")
        self.page.get_by_text("Explorar").click()

    def abrir_restaurante(self, nome: str):
        self.page.get_by_text(nome).click()

    def adicionar_item(self, nome_item: str):
        self.page.get_by_role("listitem", name=nome_item).get_by_text("Adicionar").click()
