### Projeto: Exercícios — Hierarquia de Chomsky e Máquinas

Conteúdo:

- `src/exercises.py`: implementações em Python com respostas objetivas e exemplos algorítmicos:
  - Respostas (funções `q1()`..`q10()`)
  - `dfa_even_a(s)` — DFA que aceita cadeias com número par de 'a'
  - `pda_an_bn(s)` — PDA simples que reconhece a^n b^n
  - `tm_increment_binary(bin_str)` — simulador simples de Máquina de Turing para incremento binário

- `tests/test_exercises.py`: testes automatizados (pytest)

Como executar:

1. Executar o módulo diretamente (mostra demos):

```bash
python -m src.exercises
```

2. Rodar testes com `pytest`:

```bash
pytest
```

5. Executar a interface visual (Tkinter) para listar e rodar testes/exercícios:

```bash
python -m src.gui
```

Isso abrirá uma janela com a lista de arquivos de teste (em `tests/`), botões para rodar os testes selecionados, rodar todos os testes, e um botão para executar os exercícios (`src.exercises`) — a saída é mostrada na área de texto.

Observações:

- As implementações são educacionais e destinadas a demonstração didática.
- Requer Python 3.8+ e `pytest` para rodar os testes.

Detalhes para abrir o projeto no VS Code e executar localmente
-----------------------------------------------------------

1) Abrir o projeto no VS Code

- Abra o VS Code e escolha "Open Folder..." (Arquivo → Abrir Pasta) e selecione a pasta do projeto:
  `D:\UNIC\linguagens-formais-automatos`.

2) Criar e ativar um virtualenv (recomendado)

- No Windows (cmd.exe) dentro da pasta do projeto:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Se preferir PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3) Instalar dependências

```cmd
python -m pip install --upgrade pip
python -m pip install pytest
```

Se quiser fixar dependências, crie um `requirements.txt` com `pytest` e rode `pip install -r requirements.txt`.

4) Rodar a interface gráfica (GUI)

Com o virtualenv ativado e estando no diretório do projeto:

```cmd
python -m src.gui
```

Isso abrirá a janela com a lista de testes, botões para executá-los e a área de saída.

5) Rodar testes pela linha de comando (opcional)

```cmd
pytest
```

6) Executar os exercícios (demos) pela linha de comando (opcional)

```cmd
python -m src.exercises
```

Dicas extras
-------------
- Se a janela da GUI não abrir, verifique se o Python tem suporte a Tkinter (na instalação oficial do Windows costuma vir junto). Para checar no terminal:

```cmd
python -c "import tkinter; print(tkinter.TkVersion)"
```

- Se o comando acima falhar, instale a versão do Python que inclua Tkinter ou habilite o componente apropriado.
- Para re-executar a lista de testes sem reiniciar a GUI, você pode fechar e reabrir a janela (ou eu adiciono um botão Refresh se preferir).

Arquivos úteis incluídos
------------------------

- `requirements.txt`: lista mínima de dependências (`pytest`) para rodar os testes.
- `run_all.bat`: script Windows que cria/ativa `.venv`, instala dependências e executa a GUI.

Para usar o `run_all.bat`, abra o Explorer na pasta do projeto e dê um duplo-clique, ou rode no `cmd.exe`:

```cmd
run_all.bat
```