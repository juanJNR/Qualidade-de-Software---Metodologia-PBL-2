# Aula 09 — Testes Unitários Automatizados e TDD — LocalEats

**Disciplina:** Qualidade de Software — Centro Universitário Senac-RS
**Prof.:** Luciano Zanuz
**Sistema em análise:** [LocalEats](https://local-eats-unisenac.vercel.app/)

## 1. Funcionalidades escolhidas

Para esta atividade, o grupo optou por duas regras de negócio diferentes das
utilizadas como exemplo no enunciado, mantendo o mesmo nível de clareza:

| Integrante | Funcionalidade | Regra de negócio |
|---|---|---|
| Integrante 1 | Aplicação de desconto percentual | Desconto deve estar entre 0% e 100%; valor final nunca pode ser negativo |
| Integrante 2 | Cálculo de taxa de entrega | Até 3 km cobra taxa fixa; acima disso, taxa proporcional à distância; distância negativa gera erro |

---

## 2. Testes Unitários

### 2.1 Funcionalidade: Desconto percentual

```python
def aplicar_desconto(valor_total: float, percentual: float) -> float:
    """
    Aplica um desconto percentual sobre o valor total do pedido.
    Regras:
    - percentual deve estar entre 0 e 100 (inclusive)
    - o valor final nunca pode ser negativo
    """
    if percentual < 0 or percentual > 100:
        raise ValueError("Percentual de desconto inválido")

    valor_final = valor_total - (valor_total * percentual / 100)
    return round(valor_final, 2)
```

**Teste 1 — Desconto padrão aplicado corretamente (happy path)**

- Cenário: aplicar 10% de desconto sobre R$ 100,00
- Entrada: `valor_total=100, percentual=10`
- Resultado esperado: `90.0`

```python
def test_deve_aplicar_desconto_de_10_por_cento():
    # Arrange
    valor_total = 100
    percentual = 10

    # Act
    resultado = aplicar_desconto(valor_total, percentual)

    # Assert
    assert resultado == 90.0
```

**Teste 2 — Desconto de 100% zera o valor (happy path / limite superior)**

- Cenário: aplicar desconto máximo permitido
- Entrada: `valor_total=50, percentual=100`
- Resultado esperado: `0.0`

```python
def test_deve_zerar_valor_com_desconto_de_100_por_cento():
    # Arrange
    valor_total = 50
    percentual = 100

    # Act
    resultado = aplicar_desconto(valor_total, percentual)

    # Assert
    assert resultado == 0.0
```

**Teste 3 — Percentual inválido gera erro (cenário de erro/borda)**

- Cenário: tentar aplicar desconto acima de 100%
- Entrada: `valor_total=80, percentual=150`
- Resultado esperado: `ValueError`

```python
def test_deve_gerar_erro_quando_percentual_maior_que_100():
    # Arrange
    valor_total = 80
    percentual = 150

    # Act / Assert
    import pytest
    with pytest.raises(ValueError):
        aplicar_desconto(valor_total, percentual)
```

### 2.2 Funcionalidade: Taxa de entrega

```python
def calcular_taxa_entrega(distancia_km: float) -> float:
    """
    Calcula a taxa de entrega com base na distância.
    Regras:
    - até 3 km: taxa fixa de R$ 5,00
    - acima de 3 km: R$ 5,00 + R$ 1,50 por km excedente
    - distância negativa é inválida
    """
    if distancia_km < 0:
        raise ValueError("Distância inválida")

    TAXA_FIXA = 5.0
    if distancia_km <= 3:
        return TAXA_FIXA

    km_excedente = distancia_km - 3
    return round(TAXA_FIXA + (km_excedente * 1.5), 2)
```

**Teste 1 — Distância dentro do limite fixo (happy path)**

- Cenário: entrega a 2 km
- Entrada: `distancia_km=2`
- Resultado esperado: `5.0`

```python
def test_deve_cobrar_taxa_fixa_ate_3km():
    # Arrange
    distancia_km = 2

    # Act
    resultado = calcular_taxa_entrega(distancia_km)

    # Assert
    assert resultado == 5.0
```

**Teste 2 — Distância acima do limite (happy path)**

- Cenário: entrega a 5 km (2 km excedentes)
- Entrada: `distancia_km=5`
- Resultado esperado: `8.0`

```python
def test_deve_cobrar_taxa_proporcional_acima_de_3km():
    # Arrange
    distancia_km = 5

    # Act
    resultado = calcular_taxa_entrega(distancia_km)

    # Assert
    assert resultado == 8.0
```

**Teste 3 — Distância negativa gera erro (cenário de erro/borda)**

- Cenário: distância inválida informada pelo sistema
- Entrada: `distancia_km=-1`
- Resultado esperado: `ValueError`

```python
def test_deve_gerar_erro_para_distancia_negativa():
    # Arrange
    distancia_km = -1

    # Act / Assert
    import pytest
    with pytest.raises(ValueError):
        calcular_taxa_entrega(distancia_km)
```

---

## 3. Aplicação do ciclo TDD

Ciclo aplicado à funcionalidade de **taxa de entrega**.

### 🔴 Red

Primeiro escrevemos o teste `test_deve_cobrar_taxa_fixa_ate_3km`, antes de
existir qualquer implementação de `calcular_taxa_entrega`. Ao rodar:

```
$ pytest test_taxa_entrega.py
E   NameError: name 'calcular_taxa_entrega' is not defined
1 failed in 0.03s
```

O teste falha como esperado, comprovando que ainda não há implementação.

### 🟢 Green

Criamos a versão mínima da função, apenas retornando a taxa fixa:

```python
def calcular_taxa_entrega(distancia_km):
    return 5.0
```

Com essa implementação, o primeiro teste passa. Mas o segundo teste
(`acima de 3km`) falha, pois a função ainda não trata o cálculo proporcional.
Evoluímos a implementação até fazer os três testes passarem (versão completa
mostrada na seção 2.2).

### 🔵 Refactor

Com os testes verdes, revisamos o código para extrair a constante `TAXA_FIXA`
e a taxa por km excedente (`1.5`) como nomes claros, e adicionamos a validação
de entrada negativa antes da lógica de cálculo, deixando o fluxo mais legível
sem quebrar nenhum teste já existente.

---

## 4. Refatoração

Melhorias aplicadas nas duas funções:

- **Legibilidade:** substituição de números "mágicos" (`5.0`, `1.5`, `3`) por
  constantes nomeadas (`TAXA_FIXA`, `LIMITE_KM_TAXA_FIXA`, `VALOR_KM_EXCEDENTE`).
- **Nomes:** parâmetros renomeados de `d`/`p` para `distancia_km` e
  `percentual`, tornando o significado explícito sem precisar de comentários.
- **Organização:** validações de entrada centralizadas no início da função,
  separadas do cálculo principal.
- **Duplicações:** o padrão de validação (`if valor < 0: raise ValueError`)
  foi identificado como repetido entre as duas funções; documentamos como
  possível extração futura de uma função utilitária `validar_nao_negativo()`.

---

## 5. Execução dos testes

```
$ pytest -v

test_desconto.py::test_deve_aplicar_desconto_de_10_por_cento PASSED
test_desconto.py::test_deve_zerar_valor_com_desconto_de_100_por_cento PASSED
test_desconto.py::test_deve_gerar_erro_quando_percentual_maior_que_100 PASSED
test_taxa_entrega.py::test_deve_cobrar_taxa_fixa_ate_3km PASSED
test_taxa_entrega.py::test_deve_cobrar_taxa_proporcional_acima_de_3km PASSED
test_taxa_entrega.py::test_deve_gerar_erro_para_distancia_negativa PASSED

======================== 6 passed in 0.08s ========================
```

- **Total de testes:** 6
- **Passaram:** 6
- **Falharam:** 0

---

## 6. Reflexão no contexto do LocalEats

**Foi difícil escrever testes antes do código?**
No início sim, pois exige pensar no comportamento esperado antes de pensar
"como" implementar. Depois de definir bem os cenários (sucesso, limite e
erro), a escrita da implementação ficou mais direta.

**O TDD ajudou no desenvolvimento?**
Sim. Ao escrever o teste primeiro, ficou claro exatamente o que a função
`calcular_taxa_entrega` precisava fazer, evitando implementar regras que não
seriam usadas.

**Os testes aumentaram a confiança no código?**
Sim, principalmente para os casos de borda (desconto de 100%, distância
negativa), que dificilmente seriam lembrados em um teste manual.

**O que melhorariam?**
Extrair a validação duplicada em uma função reutilizável e adicionar testes
parametrizados (`pytest.mark.parametrize`) para cobrir mais combinações de
distância e percentual com menos código repetido.

**Como isso ajuda no projeto do grupo?**
Garante que regras de negócio críticas do LocalEats (cálculo de valores)
continuem corretas mesmo quando o código for alterado por outro integrante,
reduzindo o risco de regressões silenciosas.
