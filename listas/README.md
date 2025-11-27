# Gramática Para a Linguagem de Parênteses Pareados

A maior parte das linguagens de programação modernas suportam listas ou arrays
como estruturas de dados básicas e oferecem sintaxes convenientes para sua
criação. LISP, Lua, Python, JSON e Javascript são exemplos disso e oferecem sintaxes parecidas
entre si, mas que se diferem em alguns detalhes.

Todas essas linguagens usam colchetes `[` e `]` para delimitar listas, e 
vírgulas `,` para separar os elementos. Em todas elas também, as listas podem ser
vazias e arbitrariamente aninhadas. No entanto, existem diferenças sutis:
- LISP usa espaços para separar os elementos da lista, enquanto as outras 
  linguagens usam vírgulas.
- LISP usa um parêntese inicial `'(` para indicar o início de uma lista e o
  parêntese `)` para terminá-la.
- Lua usa `{` e `}` para delimitar listas, ao invés de colchetes.
- Lua permite elementos nomeados como em `{0, x=1, y=2}`, enquanto as outras não.
- Python, Lua e Javascript permitem uma vírgula opcional após o último elemento da 
  lista, como em `[1,2,3]`. JSON não.
- Javascript permite mais de uma vírgula consecutiva para indicar elementos 
  vazios, como em `[1,,3]`. Pode, inclusive, conter uma vírgula inicial, como 
  em `[,1,2]`.


Edite o arquivo `grammar.lark` para fazer os testes passarem. Para rodar os testes, use:

```bash

uv run pytest --tb=short
```
