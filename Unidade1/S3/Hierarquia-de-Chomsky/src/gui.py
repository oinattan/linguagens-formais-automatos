import subprocess
import sys
import threading
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / 'tests'


try:
    import ttkbootstrap as tb
    from ttkbootstrap import Window
    TTKBOOTSTRAP_AVAILABLE = True
except Exception:
    tb = None
    Window = None
    TTKBOOTSTRAP_AVAILABLE = False


class TestRunnerGUI(tk.Tk if not TTKBOOTSTRAP_AVAILABLE else Window):
    def __init__(self):
        if TTKBOOTSTRAP_AVAILABLE:
            super().__init__(themename='superhero')
        else:
            super().__init__()
        self.title('Runner - Exercícios e Testes')
        # tamanho um pouco maior quando tema aplicado
        self.geometry('900x600')

        self.create_widgets()
        self.populate_test_list()
        # carregar automaticamente a descrição na info_box
        try:
            self.load_description()
        except Exception:
            pass

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=8, pady=8)

        left = ttk.Frame(frame)
        left.pack(side='left', fill='y')

        # Caixa de informação acima da lista de testes
        ttk.Label(left, text='Informação:').pack(anchor='nw')
        self.info_box = scrolledtext.ScrolledText(left, height=6, wrap='word')
        self.info_box.pack(fill='x', expand=False, pady=(0, 6))

        ttk.Label(left, text='Arquivos de teste:').pack(anchor='nw')
        self.test_listbox = tk.Listbox(left, selectmode='extended', width=40, height=12)
        self.test_listbox.pack(fill='y', expand=False)

        # area de botões com barra de rolagem vertical (para garantir visibilidade)
        btn_container = ttk.Frame(left)
        btn_container.pack(fill='both', expand=False, pady=6)

        canvas = tk.Canvas(btn_container, width=320, height=240)
        vsb = ttk.Scrollbar(btn_container, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)

        canvas.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        # botões dentro do frame rolável
        ttk.Button(scrollable_frame, text='Executar selecionados', command=self.run_selected_tests).pack(fill='x', pady=2)
        ttk.Button(scrollable_frame, text='Executar todos os testes', command=self.run_all_tests).pack(fill='x', pady=2)
        ttk.Button(scrollable_frame, text='Atualizar lista', command=self.populate_test_list).pack(fill='x', pady=2)
    # botão 'Mostrar descrição' removido: descrição agora carregada automaticamente
        ttk.Button(scrollable_frame, text='Limpar saída', command=self.clear_output).pack(fill='x', pady=2)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=6)
        ttk.Button(scrollable_frame, text='Executar exercícios', command=self.run_exercises).pack(fill='x', pady=2)
        ttk.Button(scrollable_frame, text='Abrir pasta de testes', command=self.open_tests_folder).pack(fill='x', pady=2)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=6)

        # Painel direito: dividido verticalmente em perguntas (top) e comandos/resultados (bottom)
        right_pane = ttk.PanedWindow(frame, orient='vertical')
        right_pane.pack(side='right', fill='both', expand=True)

        # Topo: perguntas com scroll
        questions_container = ttk.Frame(right_pane)
        questions_container.pack(fill='both', expand=True)
        ttk.Label(questions_container, text='Perguntas e Exercícios:').pack(anchor='nw')

        q_canvas = tk.Canvas(questions_container)
        q_vsb = ttk.Scrollbar(questions_container, orient='vertical', command=q_canvas.yview)
        q_scroll_frame = ttk.Frame(q_canvas)
        q_scroll_frame.bind('<Configure>', lambda e: q_canvas.configure(scrollregion=q_canvas.bbox('all')))
        q_canvas.create_window((0, 0), window=q_scroll_frame, anchor='nw')
        q_canvas.configure(yscrollcommand=q_vsb.set)
        q_canvas.pack(side='left', fill='both', expand=True)
        q_vsb.pack(side='right', fill='y')

        # armazenar o frame de perguntas
        self.questions_frame = q_scroll_frame

        # Bottom: comandos e resultados (área dedicada)
        cmd_container = ttk.Frame(right_pane)
        ttk.Label(cmd_container, text='Comandos e Resultados:').pack(anchor='nw')
        self.command_output = scrolledtext.ScrolledText(cmd_container, height=12, wrap='word')
        self.command_output.pack(fill='both', expand=True)

        right_pane.add(questions_container, weight=3)
        right_pane.add(cmd_container, weight=1)

        # Gerar dinamicamente as questões a partir do módulo exercises
        try:
            from src import exercises
            q_fns = [exercises.q1, exercises.q2, exercises.q3, exercises.q4, exercises.q5,
                     exercises.q6, exercises.q7, exercises.q8, exercises.q9, exercises.q10]
        except Exception:
            q_fns = []

        # Perguntas curtas (apenas rótulos) — podem ser ajustadas conforme necessidade
        q_texts = [
            '1. Qual não faz parte da hierarquia?',
            '2. Qual modelo reconhece linguagens regulares?',
            '3. A Máquina de Turing é um modelo de:',
            '4. Qual linguagem não é regular?',
            '5. Qual modelo é mais poderoso?',
            '6. O Autômato com Pilha reconhece:',
            '7. Qual modelo usa uma pilha como memória auxiliar?',
            '8. A hierarquia de Chomsky classifica linguagens por:',
            '9. O autômato finito não pode reconhecer:',
            '10. Objetivo principal de estudar autômatos?'
        ]

        for idx in range(10):
            row = ttk.Frame(self.questions_frame)
            row.pack(fill='x', pady=4)
            # pergunta (com wrap para caber na coluna)
            qlabel = ttk.Label(row, text=q_texts[idx], wraplength=620, justify='left')
            qlabel.pack(side='left', padx=(0, 6), fill='x', expand=True)

            # obter resposta chamando a função, se disponível
            try:
                ans = q_fns[idx]() if q_fns else 'N/A'
            except Exception:
                ans = 'Erro'
            ans_label = ttk.Label(row, text=f'Resposta: {ans}', width=12, anchor='w')
            ans_label.pack(side='left', padx=(0, 6))

            # Botão que executa exemplo relacionado à questão (executa em-thread, em-processo)
            btn = ttk.Button(row, text='Executar exercício', command=(lambda i=idx: self.run_question_demo(i)))
            btn.pack(side='right')
    def populate_test_list(self):
        self.test_listbox.delete(0, tk.END)
        if not TESTS_DIR.exists():
            return
        for p in sorted(TESTS_DIR.glob('test_*.py')):
            self.test_listbox.insert(tk.END, str(p.name))

    def load_description(self):
        """Carrega a descrição de `src.exercises.get_description()` diretamente na info_box (fallback para command_output)."""
        try:
            from src import exercises
            desc = exercises.get_description()
            if not desc:
                desc = 'Nenhuma descrição disponível.'
            try:
                self.info_box.delete('1.0', tk.END)
                self.info_box.insert(tk.END, desc)
                self.info_box.see(tk.END)
            except Exception:
                self.append_output(desc + '\n')
        except Exception as e:
            self.append_output(f'Erro ao obter descrição: {e}\n')

    def append_output(self, text: str):
        def write():
            # manter compatibilidade: escrever também em command_output
            try:
                self.command_output.insert(tk.END, text)
                self.command_output.see(tk.END)
            except Exception:
                pass
        self.after(0, write)

    def clear_output(self):
        try:
            self.command_output.delete('1.0', tk.END)
        except Exception:
            pass

    def run_in_thread(self, cmd, cwd=None):
        def target():
            try:
                # Forçar saída não bufferizada para Python e pytest (-u for python; -s for pytest)
                env = os.environ.copy()
                env.setdefault('PYTHONUNBUFFERED', '1')
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, cwd=cwd, env=env)
            except Exception as e:
                self.append_output(f'Erro ao iniciar processo: {e}\n')
                return
            # Ler linha a linha e encaminhar para a saída em tempo real
            for line in proc.stdout:
                self.append_output(line)
            proc.wait()
            self.append_output(f'Processo finalizado com código {proc.returncode}\n')

        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    def run_selected_tests(self):
        sel = [self.test_listbox.get(i) for i in self.test_listbox.curselection()]
        if not sel:
            messagebox.showinfo('Informação', 'Nenhum teste selecionado')
            return
        paths = [str(TESTS_DIR / s) for s in sel]
        cmd = [sys.executable, '-m', 'pytest', '-q', *paths]
        self.append_output(f'Executando: {" ".join(cmd)}\n')
        self.run_in_thread(cmd, cwd=str(ROOT))
    

    def run_all_tests(self):
        cmd = [sys.executable, '-m', 'pytest', '-q']
        self.append_output(f'Executando: {" ".join(cmd)}\n')
        self.run_in_thread(cmd, cwd=str(ROOT))

    def run_exercises(self):
        cmd = [sys.executable, '-m', 'src.exercises']
        self.append_output(f'Executando exercícios: {" ".join(cmd)}\n')
        self.run_in_thread(cmd, cwd=str(ROOT))
    

    def open_tests_folder(self):
        folder = ROOT / 'tests'
        if not folder.exists():
            messagebox.showerror('Erro', f'Pasta não encontrada: {folder}')
            return
        try:
            if hasattr(os, 'startfile'):
                os.startfile(str(folder))
                return
        except Exception:
            pass
        try:
            if sys.platform == 'darwin':
                subprocess.Popen(['open', str(folder)])
            else:
                subprocess.Popen(['xdg-open', str(folder)])
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível abrir a pasta: {e}')

    def run_question_demo(self, idx: int):
        """Executa o demo associado à questão `idx` em uma thread e envia saída para o widget."""
        def target():
            try:
                from src import exercises
            except Exception as e:
                self.append_output(f'Erro ao importar src.exercises: {e}\n')
                return

            try:
                self.append_output(f'--- Executando exercício {idx+1} ---\n')
                # mapa de demos por índice (0-based)
                if idx == 3:
                    # Q4: PDA a^n b^n
                    examples = ['', 'ab', 'aabb', 'aaabbb', 'aba']
                    for s in examples:
                        self.append_output(f"'{s}': {exercises.pda_an_bn(s)}\n")
                elif idx == 8:
                    # Q9: DFA par de 'a'
                    examples = ['', 'a', 'aa', 'aba', 'aab']
                    for s in examples:
                        self.append_output(f"'{s}': {exercises.dfa_even_a(s)}\n")
                elif idx in (2, 4):
                    # Q3 ou Q5: Máquina de Turing (descrição + incremento)
                    desc = exercises.get_description()
                    if desc:
                        self.append_output(desc + '\n')
                    for s in ['0', '1', '1011', '111']:
                        try:
                            res = exercises.tm_increment_binary(s)
                        except Exception as e:
                            res = f'Erro: {e}'
                        self.append_output(f"{s} -> {res}\n")
                else:
                    # default: print resposta e descrição
                    try:
                        ans = getattr(exercises, f'q{idx+1}')()
                    except Exception:
                        ans = 'Erro'
                    self.append_output(f'Questao {idx+1} - Resposta: {ans}\n')
                    desc = exercises.get_description()
                    if desc:
                        self.append_output(desc + '\n')

                self.append_output(f'--- Fim exercício {idx+1} ---\n')
            except Exception as e:
                self.append_output(f'Erro ao executar demo da questão {idx+1}: {e}\n')

        thread = threading.Thread(target=target, daemon=True)
        thread.start()


def main():
    app = TestRunnerGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
