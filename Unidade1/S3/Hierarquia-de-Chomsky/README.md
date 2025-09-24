### Projeto: Exercícios — Hierarquia de Chomsky e Máquinas

Descrição
---------

Ferramentas e exercícios didáticos sobre autômatos e a hierarquia de Chomsky. A interface gráfica (`src.gui`) ajuda a listar e executar testes em `tests/` e a executar os exemplos em `src/exercises.py`.

Execução rápida
---------------

Se você estiver no Windows, o script `run_all.bat` automatiza a criação/ativação do ambiente virtual, instala dependências e (opcionalmente) inicia a GUI. Recomendo começar por ele:

```cmd
run_all.bat
```

Estrutura principal
------------------

- `src/exercises.py`: respostas e demos (funções `q1()`..`q10()`, `dfa_even_a`, `pda_an_bn`, `tm_increment_binary`).
- `src/gui.py`: interface Tkinter para listar testes e executar exercícios.
- `tests/test_exercises.py`: suíte de testes usando `pytest`.

Como executar (resumido)
-----------------------

As instruções abaixo assumem que você está em Windows (`cmd.exe`). Ajuste conforme necessário para PowerShell/Linux/macOS.

1) Criar e ativar ambiente virtual (recomendado)

```cmd
python -m venv .venv
.venv\Scripts\activate
```

2) Instalar dependências

```cmd
python -m pip install --upgrade pip
python -m pip install pytest
```

3) Rodar testes

```cmd
python -m pytest -q
```

4) Executar demos (terminal)

```cmd
python -m src.exercises
```

5) Executar a GUI

IMPORTANTE: execute a GUI a partir da raiz do projeto (não do diretório `src`).

```cmd
cd D:\...\Hierarquia-de-Chomsky
python -m src.gui
```

Aviso: NÃO execute `src/gui.py` diretamente (por exemplo `python src/gui.py`) — isso pode causar erros de importação. Se precisar executar de dentro de `src`, veja a seção de solução de problemas abaixo.

Solução de problemas comum
--------------------------

- Erro: `ModuleNotFoundError: No module named 'src'`
  - Causa: executar `python -m src.gui` estando dentro de `.../src` faz com que o interpretador espere um pacote `src` dentro do diretório atual.
  - Correto: execute a partir da raiz do projeto (veja o passo 5 acima) ou ajuste `PYTHONPATH` (não recomendado como prática padrão):

```cmd
cd D:\...\Hierarquia-de-Chomsky\src
set PYTHONPATH=%CD%\..
python -m src.gui
```

- VS Code: use uma configuração `launch.json` que execute o módulo `src.gui` com `cwd` apontando para a raiz do projeto (exemplo abaixo).

Exemplo de `launch.json` (VS Code)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run GUI (module)",
      "type": "python",
      "request": "launch",
      "module": "src.gui",
      "cwd": "${workspaceFolder}/Unidade1/S3/Hierarquia-de-Chomsky"
    }
  ]
}
```

Observações
-----------

- As implementações são educacionais e destinadas a demonstração didática.
- Requer Python 3.8+ e `pytest` para rodar os testes.

Dicas rápidas
------------

- Verificar Tkinter (Windows):

```cmd
python -c "import tkinter; print(tkinter.TkVersion)"
```

- Para re-executar a lista de testes na GUI sem reiniciar, feche e reabra a janela (posso adicionar um botão "Refresh" se preferir).

Arquivos úteis
-------------

- `requirements.txt`: lista mínima de dependências (ex.: `pytest`).
- `run_all.bat`: script Windows que cria/ativa `.venv`, instala dependências e (opcionalmente) executa a GUI.

Para usar o `run_all.bat`, abra o Explorer na pasta do projeto e dê um duplo-clique, ou rode no `cmd.exe`:

```cmd
run_all.bat
```