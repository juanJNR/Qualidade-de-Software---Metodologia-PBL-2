TAXA_FIXA = 5.0
LIMITE_KM_TAXA_FIXA = 3
VALOR_KM_EXCEDENTE = 1.5


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

    if distancia_km <= LIMITE_KM_TAXA_FIXA:
        return TAXA_FIXA

    km_excedente = distancia_km - LIMITE_KM_TAXA_FIXA
    return round(TAXA_FIXA + (km_excedente * VALOR_KM_EXCEDENTE), 2)
