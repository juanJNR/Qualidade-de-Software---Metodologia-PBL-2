import pytest
from taxa_entrega import calcular_taxa_entrega


def test_deve_cobrar_taxa_fixa_ate_3km():
    # Arrange
    distancia_km = 2

    # Act
    resultado = calcular_taxa_entrega(distancia_km)

    # Assert
    assert resultado == 5.0


def test_deve_cobrar_taxa_proporcional_acima_de_3km():
    # Arrange
    distancia_km = 5

    # Act
    resultado = calcular_taxa_entrega(distancia_km)

    # Assert
    assert resultado == 8.0


def test_deve_gerar_erro_para_distancia_negativa():
    # Arrange
    distancia_km = -1

    # Act / Assert
    with pytest.raises(ValueError):
        calcular_taxa_entrega(distancia_km)
