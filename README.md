# KeycloakAccount
Python app that interacts with Keycloak's REST API and creates our accounts

<br>

## Instruções para executar a aplicação:
- Instalar os módulos necessários através de ```pip install -r requirements.txt``` no diretório principal.
- Executar o ficheiro ```app.py``` para servir a aplicação.
- Abrir o browser no endereço indicado no terminal.

<p>&nbsp</p>
  
## Coisas a fazer:

- [ ] Implementar todos os `inputs` necessários nos formulários das páginas HTML para passar à base de dados.
- [x] Melhorar o design das páginas HTML.
- [ ] Configurar a base de dados.
- [ ] Criar páginas para apresentar quando ocorrer erros de registo e afins.
- [ ] Login para o Keycloak.
- [ ] Recuperação de passwords.

<p>&nbsp</p>

## Links para testar a validação dos formulários:

Caso os dados inseridos não sejam válidos, a página vai retornar um erro no `<input>` onde ele ocorreu e dizer a razão pela qual os dados não podem ser submetidos.
Caso os dados sejam validados e submetidos com sucesso, o servidor vai dar um erro 405.

[Página para criação de contas (index.html)](http://sweet.ua.pt/jtsimoes/KeycloakAccount/index.html)

[Página para migração de contas (register-token.html)](http://sweet.ua.pt/jtsimoes/KeycloakAccount/templates/register-token.html)
