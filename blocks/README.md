# Gramática Para a Linguagem de Parênteses Pareados

Uma linguagem clássica que pode ser representada por uma gramática livre de 
contexto, mas não por uma expressão regular é a linguagem dos comandos agrupados 
em blocos como em "e;", "{e;}", ou no exemplo mais elaborado

```
{
    {
        e;
    }
    {
        e;
        {
            e;
        }
    }
}
``` 

Crie uma gramática Lark que identifica esta linguagem.

Edite o arquivo `grammar.lark` para fazer os testes passarem. Para rodar os testes, use:

```bash

uv run pytest --tb=short
```
