Feature: Navegação entre páginas do sistema

  Scenario: Acessar a página de Favoritos
    Given que o usuário está na página inicial do LocalEats
    When ele clica no menu "Favoritos"
    Then o sistema deve exibir a página de restaurantes favoritados

  Scenario: Acessar a página de Meus Pedidos
    Given que o usuário está na página inicial do LocalEats
    When ele clica no menu "Meus Pedidos"
    Then o sistema deve exibir a lista de pedidos realizados
