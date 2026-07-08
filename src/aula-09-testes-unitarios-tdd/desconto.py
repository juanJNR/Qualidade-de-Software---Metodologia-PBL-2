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
