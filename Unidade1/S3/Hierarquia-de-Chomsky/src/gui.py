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

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=8, pady=8)

        left = ttk.Frame(frame)
        left.pack(side='left', fill='y')

        ttk.Label(left, text='Arquivos de teste:').pack(anchor='nw')
        self.test_listbox = tk.Listbox(left, selectmode='extended', width=40, height=20)
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
        ttk.Button(scrollable_frame, text='Mostrar descrição', command=self.show_description).pack(fill='x', pady=2)
        ttk.Button(scrollable_frame, text='Limpar saída', command=self.clear_output).pack(fill='x', pady=2)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=6)
        ttk.Button(scrollable_frame, text='Executar exercícios', command=self.run_exercises).pack(fill='x', pady=2)
        ttk.Button(scrollable_frame, text='Abrir arquivo de exercícios', command=self.open_exercises_file).pack(fill='x', pady=2)
        ttk.Button(scrollable_frame, text='Abrir pasta de testes', command=self.open_tests_folder).pack(fill='x', pady=2)

        right = ttk.Frame(frame)
        right.pack(side='right', fill='both', expand=True)

        ttk.Label(right, text='Saída:').pack(anchor='nw')
        self.output = scrolledtext.ScrolledText(right, wrap='word')
        self.output.pack(fill='both', expand=True)

    def populate_test_list(self):
        self.test_listbox.delete(0, tk.END)
        if not TESTS_DIR.exists():
            return
        for p in sorted(TESTS_DIR.glob('test_*.py')):
            self.test_listbox.insert(tk.END, str(p.name))

    def append_output(self, text: str):
        def write():
            self.output.insert(tk.END, text)
            self.output.see(tk.END)
        self.after(0, write)

    def clear_output(self):
        self.output.delete('1.0', tk.END)

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

    def show_description(self):
        try:
            from src import exercises
            desc = exercises.get_description()
            if not desc:
                desc = 'Nenhuma descrição disponível.'
            self.append_output(desc + '\n')
        except Exception as e:
            self.append_output(f'Erro ao obter descrição: {e}\n')

    def run_all_tests(self):
        cmd = [sys.executable, '-m', 'pytest', '-q']
        self.append_output(f'Executando: {" ".join(cmd)}\n')
        self.run_in_thread(cmd, cwd=str(ROOT))

    def run_exercises(self):
        cmd = [sys.executable, '-m', 'src.exercises']
        self.append_output(f'Executando exercícios: {" ".join(cmd)}\n')
        self.run_in_thread(cmd, cwd=str(ROOT))

    def open_exercises_file(self):
        path = ROOT / 'src' / 'exercises.py'
        if not path.exists():
            messagebox.showerror('Erro', f'Arquivo não encontrado: {path}')
            return
        # tenta abrir no VS Code via CLI 'code'
        try:
            subprocess.Popen(['code', str(path)])
            return
        except Exception:
            pass

        # Em Windows, usa o app padrão
        if hasattr(os, 'startfile'):
            try:
                os.startfile(str(path))
                return
            except Exception:
                pass

        # Fallback para macOS / Linux
        try:
            if sys.platform == 'darwin':
                subprocess.Popen(['open', str(path)])
            else:
                subprocess.Popen(['xdg-open', str(path)])
            return
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível abrir o arquivo: {e}')

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


def main():
    app = TestRunnerGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
