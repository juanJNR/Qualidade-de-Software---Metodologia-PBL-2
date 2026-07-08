import pytest
from desconto import aplicar_desconto


def test_deve_aplicar_desconto_de_10_por_cento():
    # Arrange
    valor_total = 100
    percentual = 10

    # Act
    resultado = aplicar_desconto(valor_total, percentual)

    # Assert
    assert resultado == 90.0


def test_deve_zerar_valor_com_desconto_de_100_por_cento():
    # Arrange
    valor_total = 50
    percentual = 100

    # Act
    resultado = aplicar_desconto(valor_total, percentual)

    # Assert
    assert resultado == 0.0


def test_deve_gerar_erro_quando_percentual_maior_que_100():
    # Arrange
    valor_total = 80
    percentual = 150

    # Act / Assert
    with pytest.raises(ValueError):
        aplicar_desconto(valor_total, percentual)
