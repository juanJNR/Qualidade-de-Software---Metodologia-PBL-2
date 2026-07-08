Feature: Filtro de restaurantes por categoria

  Scenario: Filtrar restaurantes por categoria de comida japonesa
    Given que o usuário está na página de Explorar
    When ele seleciona a categoria "Japonesa"
    Then o sistema deve exibir apenas restaurantes da categoria "Japonesa"

  Scenario: Remover filtro de categoria
    Given que o usuário aplicou o filtro "Japonesa"
    When ele remove o filtro aplicado
    Then o sistema deve exibir novamente todos os restaurantes
