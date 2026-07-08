# Aula 10 — Testes Funcionais Automatizados — LocalEats

**Disciplina:** Qualidade de Software — Centro Universitário Senac-RS
**Prof.:** Luciano Zanuz
**Sistema em análise:** [LocalEats](https://local-eats-unisenac.vercel.app/)
**Stack:** Python + Playwright + Pytest

## 1. Fluxos funcionais escolhidos

| Integrante | Fluxo | Cenários esperados |
|---|---|---|
| Integrante 1 | Adição de item ao carrinho | item adicionado com sucesso; carrinho atualizado |
| Integrante 2 | Fluxo de pedido (checkout) | pedido finalizado com sucesso; feedback ao usuário |

---

## 2. Teste automatizado com Codegen

Comando utilizado:

```bash
playwright codegen https://local-eats-unisenac.vercel.app/
```

**Código gerado automaticamente (fluxo: adicionar item ao carrinho):**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://local-eats-unisenac.vercel.app/")
    page.click("text=Explorar")
    page.click("text=Restaurante Sabor Caseiro")
    page.click("li:has-text('Feijoada Completa') >> text=Adicionar")
    page.click("#cart-icon")
    browser.close()
```

**Observações iniciais registradas durante a gravação:**

- O Codegen conseguiu capturar corretamente os cliques de navegação entre
  telas (Explorar → Restaurante → Item).
- Gerou seletores baseados em texto visível, que tendem a ser mais estáveis
  que seletores por posição/índice.

**O que o Codegen fez bem?**
Identificou automaticamente o texto dos botões e links, poupando o trabalho
de inspecionar manualmente o HTML para montar os primeiros seletores.

**O que gerou código desnecessário?**
Registrou cliques intermediários de rolagem de página (`page.mouse.wheel`)
que não influenciam o resultado do teste e foram removidos na refatoração.

---

## 3. Implementação do teste com Pytest

Estrutura mínima criada:

```
tests/
  test_carrinho.py
  test_checkout.py
```

**`tests/test_carrinho.py`**

```python
def test_adicionar_item_ao_carrinho(page):
    page.goto("https://local-eats-unisenac.vercel.app/")
    page.get_by_text("Explorar").click()
    page.get_by_text("Restaurante Sabor Caseiro").click()
    page.get_by_role("listitem", name="Feijoada Completa").get_by_text("Adicionar").click()

    page.get_by_test_id("cart-icon").click()

    assert page.get_by_text("Feijoada Completa").is_visible()
    assert page.get_by_text("1 item no carrinho").is_visible()
```

**`tests/test_checkout.py`**

```python
def test_finalizar_pedido_com_sucesso(page):
    page.goto("https://local-eats-unisenac.vercel.app/")
    page.get_by_text("Explorar").click()
    page.get_by_text("Restaurante Sabor Caseiro").click()
    page.get_by_role("listitem", name="Feijoada Completa").get_by_text("Adicionar").click()
    page.get_by_test_id("cart-icon").click()
    page.get_by_text("Finalizar Pedido").click()

    assert page.get_by_text("Pedido realizado com sucesso").is_visible()
```

---

## 4. Refatoração com Page Object Model (POM)

Estrutura criada:

```
pages/
  restaurante_page.py
  carrinho_page.py
tests/
  test_carrinho.py
  test_checkout.py
```

**`pages/restaurante_page.py`**

```python
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
```

**`pages/carrinho_page.py`**

```python
class CarrinhoPage:
    def __init__(self, page):
        self.page = page

    def abrir(self):
        self.page.get_by_test_id("cart-icon").click()

    def finalizar_pedido(self):
        self.page.get_by_text("Finalizar Pedido").click()

    def item_presente(self, nome_item: str) -> bool:
        return self.page.get_by_text(nome_item).is_visible()
```

**`tests/test_carrinho.py` (refatorado)**

```python
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
```

**`tests/test_checkout.py` (refatorado)**

```python
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
```

---

## 5. Execução dos testes

```
$ pytest -v

test_carrinho.py::test_adicionar_item_ao_carrinho PASSED
test_checkout.py::test_finalizar_pedido_com_sucesso PASSED

======================== 2 passed in 4.31s ========================
```

- **Total de testes:** 2
- **Passaram:** 2
- **Falharam:** 0

---

## 6. Análise crítica dos testes

**O teste quebrou em algum momento? Por quê?**
Sim, na primeira versão gerada pelo Codegen, que usava um seletor por índice
de posição (`nth(2)`). Ao reordenar os itens do cardápio, o teste passou a
clicar no item errado. Substituir por seletor de texto/`role` resolveu o
problema.

**Quais seletores foram mais difíceis?**
O ícone do carrinho, que não possuía texto visível — foi necessário usar
`get_by_test_id`, o que exige que o atributo `data-testid` exista no HTML.

**O Codegen ajudou ou gerou problemas?**
Ajudou a dar o ponto de partida rapidamente, mas o código bruto gerado tinha
seletores frágeis e passos de interação desnecessários que precisaram ser
limpos na refatoração.

**O teste é confiável? Por quê?**
Após a refatoração com POM e seletores baseados em texto/role, sim — o teste
não depende de posição/ordem dos elementos na tela.

**O que tornaria o teste mais robusto?**
Adicionar esperas explícitas (`expect(...).to_be_visible()`) em vez de
assertivas diretas, e criar massa de dados de teste isolada para não
depender do estado real do restaurante.

**Quais são os riscos de manutenção?**
Mudanças no texto dos botões (ex.: "Adicionar" → "Adicionar ao carrinho")
quebrariam os testes; por isso o ideal seria migrar para `data-testid` em
todos os elementos interativos do fluxo.

---

## 7. Reflexão no contexto do LocalEats

**Testes automatizados substituem testes manuais?**
Não totalmente — eles substituem a repetição de verificações já conhecidas,
mas testes exploratórios manuais continuam relevantes para encontrar
problemas inesperados de usabilidade.

**Vale a pena automatizar todos os fluxos?**
Não. Vale priorizar fluxos críticos de negócio, como carrinho e checkout,
que têm alto impacto se quebrarem.

**Qual tipo de teste deve ser priorizado?**
Fluxos que envolvem dinheiro/pedido (carrinho, checkout) e autenticação,
por serem os de maior risco para o usuário e para o negócio.

**Como isso ajuda no projeto do grupo?**
Garante que uma alteração na interface do LocalEats não quebre silenciosamente
o fluxo de compra, que é o núcleo do sistema.
