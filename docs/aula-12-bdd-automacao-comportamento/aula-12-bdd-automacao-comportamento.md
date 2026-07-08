# Aula 12 — BDD e Automação Orientada a Comportamento — LocalEats

**Disciplina:** Qualidade de Software — Centro Universitário Senac-RS
**Prof.:** Luciano Zanuz
**Sistema em análise:** [LocalEats](https://local-eats-unisenac.vercel.app/)
**Stack:** Python + pytest + pytest-bdd + Playwright

## 1. Fluxos escolhidos

| Integrante | Fluxo | Cenários esperados |
|---|---|---|
| Integrante 1 | Filtro por categoria | filtro aplicado corretamente; lista atualizada; categoria destacada |
| Integrante 2 | Navegação entre páginas | página carrega corretamente; navegação sem erro; elementos principais aparecem |

---

## 2. Escrita dos cenários BDD

**`features/filtro_categoria.feature`**

```gherkin
Feature: Filtro de restaurantes por categoria

  Scenario: Filtrar restaurantes por categoria de comida japonesa
    Given que o usuário está na página de Explorar
    When ele seleciona a categoria "Japonesa"
    Then o sistema deve exibir apenas restaurantes da categoria "Japonesa"

  Scenario: Remover filtro de categoria
    Given que o usuário aplicou o filtro "Japonesa"
    When ele remove o filtro aplicado
    Then o sistema deve exibir novamente todos os restaurantes
```

**`features/navegacao_paginas.feature`**

```gherkin
Feature: Navegação entre páginas do sistema

  Scenario: Acessar a página de Favoritos
    Given que o usuário está na página inicial do LocalEats
    When ele clica no menu "Favoritos"
    Then o sistema deve exibir a página de restaurantes favoritados

  Scenario: Acessar a página de Meus Pedidos
    Given que o usuário está na página inicial do LocalEats
    When ele clica no menu "Meus Pedidos"
    Then o sistema deve exibir a lista de pedidos realizados
```

---

## 3. Implementação da automação com pytest-bdd

Automatizamos o cenário **"Acessar a página de Favoritos"**.

Estrutura mínima:

```
features/
  navegacao_paginas.feature
tests/
  test_navegacao_paginas.py
```

**`tests/test_navegacao_paginas.py`**

```python
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
```

---

## 4. Organização do projeto

```
projeto/
│
├── features/
│   ├── filtro_categoria.feature
│   └── navegacao_paginas.feature
├── tests/
│   └── test_navegacao_paginas.py
├── evidencias/
│   └── execucao-pytest.png
```

---

## 5. Execução dos testes

```
$ pytest -v

test_navegacao_paginas.py::test_acessar_a_pagina_de_favoritos PASSED

======================== 1 passed in 2.14s ========================
```

- **Total de cenários:** 1 (automatizado nesta entrega)
- **Passaram:** 1
- **Falharam:** 0

*(Evidência da execução registrada em `evidencias/execucao-pytest.png`.)*

---

## 6. Análise crítica

**O cenário escrito ficou compreensível?**
Sim. A frase "clica no menu Favoritos" e "exibe a página de restaurantes
favoritados" descreve o comportamento sem mencionar detalhes técnicos como
seletores CSS ou nomes de funções.

**O teste automatizado ficou legível?**
Sim, os steps `given/when/then` têm nomes próximos da linguagem natural,
facilitando a leitura por quem não programa.

**O BDD ajudou a entender o comportamento?**
Sim, principalmente porque obrigou o grupo a descrever primeiro o
comportamento esperado do usuário antes de pensar em código.

**Quais dificuldades surgiram?**
Reaproveitar os mesmos steps para cenários parecidos (ex.: "Meus Pedidos"),
já que pytest-bdd casa os textos literalmente — foi necessário planejar
frases reutilizáveis com parâmetros para não duplicar steps.

**Os seletores foram frágeis?**
Um pouco: `get_by_text('Favoritos')` depende do texto exato do menu. Se o
texto mudar para "Meus Favoritos" no menu, o teste quebraria.

**O teste ficou dependente da interface?**
Sim, é um teste de UI, então qualquer mudança visual relevante no menu afeta
o teste — isso é esperado neste tipo de automação.

**O cenário representa realmente uma regra de negócio?**
Sim: garantir que o usuário consegue acessar seus favoritos é uma regra de
navegação essencial do produto, não apenas um detalhe técnico.

**O que tornaria o teste mais robusto?**
Usar `data-testid` nos itens de menu em vez de texto visível, e adicionar
esperas explícitas para elementos carregados de forma assíncrona.

---

## 7. Reflexão no contexto do LocalEats

**BDD melhora comunicação entre equipe?**
Sim, os cenários em Gherkin podem ser lidos e validados por integrantes que
não programam, aproximando negócio e desenvolvimento.

**Todo teste deve ser escrito em BDD?**
Não. Testes muito técnicos (ex.: validação isolada de uma função matemática)
não ganham muito ao serem escritos em Gherkin; o BDD faz mais sentido para
comportamentos visíveis ao usuário.

**Quando vale a pena usar BDD?**
Em fluxos que representam regras de negócio importantes e que precisam ser
validadas/entendidas por pessoas não técnicas, como product owners.

**O comportamento ficou mais claro?**
Sim, descrever "o que" o sistema deve fazer antes de "como" ele faz ajudou o
grupo a alinhar expectativas antes de implementar.

**Como isso ajuda no projeto do grupo?**
Cria uma documentação viva dos comportamentos esperados do LocalEats, que
pode ser consultada e validada continuamente conforme o sistema evolui.
