import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class RoboControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle do Braço Robótico")
        
        self.arduino = None
        self.selected_port = tk.StringVar()
        self.filename = ""

        self.janela_selecao_serial()  # Inicia com a seleção da serial

    def janela_selecao_serial(self):
        """Tela inicial para selecionar a porta serial antes do menu principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_serial = ttk.LabelFrame(self.root, text="Seleção da Porta Serial")
        frame_serial.pack(padx=20, pady=20, fill="both", expand=True)

        self.serial_ports = self.listar_portas()
        if not self.serial_ports:
            messagebox.showerror("Erro", "Nenhuma porta serial encontrada! Conecte o Arduino e reinicie o programa.")
            self.root.quit()
            return

        self.selected_port.set(self.serial_ports[0])

        ttk.Label(frame_serial, text="Selecione a porta:", font=("Arial", 12)).pack(pady=5)

        self.port_menu = ttk.Combobox(frame_serial, textvariable=self.selected_port, values=self.serial_ports, state="readonly")
        self.port_menu.pack(pady=5)

        ttk.Button(frame_serial, text="Conectar", command=self.conectar_serial).pack(pady=10)

    def conectar_serial(self):
        """Conecta ao Arduino e avança para o menu principal."""
        try:
            self.arduino = serial.Serial(self.selected_port.get(), 115200, timeout=1)
            time.sleep(2)
            messagebox.showinfo("Sucesso", f"Conectado a {self.selected_port.get()}")
            self.main_menu()  # Avança para o menu principal
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar: {str(e)}")

    def main_menu(self):
        """Tela inicial do menu principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_menu = ttk.LabelFrame(self.root, text="Menu Principal")
        frame_menu.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Label(frame_menu, text="Selecione uma opção:", font=("Arial", 12)).pack(pady=10)

        ttk.Button(frame_menu, text="Controle Manual", command=self.janela_controle_manual).pack(pady=5)
        ttk.Button(frame_menu, text="Executar Arquivo de Comandos", command=self.janela_arquivo_comandos).pack(pady=5)
        ttk.Button(frame_menu, text="Desconectar e Sair", command=self.desconectar_serial).pack(pady=5)

    def janela_controle_manual(self):
        """Janela para controle manual dos servos."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_manual = ttk.LabelFrame(self.root, text="Controle Manual")
        frame_manual.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Label(frame_manual, text="Movimente os servos:", font=("Arial", 12)).pack(pady=10)

        self.add_botao_movimento(frame_manual, "Base Esquerda", "B180")
        self.add_botao_movimento(frame_manual, "Base Direita", "B0")
        self.add_botao_movimento(frame_manual, "Eixo Medio Cima", "M0")
        self.add_botao_movimento(frame_manual, "Eixo Medio Baixo", "M180")
        self.add_botao_movimento(frame_manual, "Eixo Superior Cima", "S0")
        self.add_botao_movimento(frame_manual, "Eixo Superior Baixo", "S180")
        self.add_botao_movimento(frame_manual, "Abrir Garra", "G180")
        self.add_botao_movimento(frame_manual, "Fechar Garra", "G0")

        ttk.Button(frame_manual, text="Voltar ao Menu", command=self.main_menu).pack(pady=10)

    def add_botao_movimento(self, parent, texto, comando):
        """Cria um botão para enviar um comando manual."""
        ttk.Button(parent, text=texto, command=lambda: self.enviar_comando(comando)).pack(pady=3)

    def janela_arquivo_comandos(self):
        """Janela para carregar e executar arquivo de comandos."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_arquivo = ttk.LabelFrame(self.root, text="Carregar Arquivo de Comandos")
        frame_arquivo.pack(padx=20, pady=20, fill="both", expand=True)

        self.file_label = ttk.Label(frame_arquivo, text="Nenhum arquivo selecionado")
        self.file_label.pack(pady=5)

        self.browse_button = ttk.Button(frame_arquivo, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.browse_button.pack(pady=5)

        self.send_button = ttk.Button(frame_arquivo, text="Enviar Comandos", command=self.enviar_comandos, state="disabled")
        self.send_button.pack(pady=5)

        ttk.Button(self.root, text="Voltar ao Menu", command=self.main_menu).pack(pady=10)

    def listar_portas(self):
        """Lista todas as portas seriais disponíveis."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def selecionar_arquivo(self):
        """Abre um seletor de arquivos para escolher o arquivo de comandos."""
        self.filename = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if self.filename:
            self.file_label.config(text=self.filename)
            self.send_button.config(state="normal")

    def enviar_comandos(self):
        """Lê o arquivo e envia os comandos via serial."""
        if not self.filename:
            messagebox.showerror("Erro", "Selecione um arquivo primeiro!")
            return

        try:
            with open(self.filename, 'r') as arquivo:
                for linha in arquivo:
                    comando = linha.strip()
                    if comando:
                        self.enviar_comando(comando)
                        time.sleep(1)
            messagebox.showinfo("Sucesso", "Comandos enviados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar comandos: {str(e)}")

    def enviar_comando(self, comando):
        """Envia um comando via serial."""
        if self.arduino:
            self.arduino.write(f"{comando}\n".encode())
            print(f"Enviado: {comando}")
        else:
            messagebox.showerror("Erro", "Conecte primeiro ao Arduino!")

    def desconectar_serial(self):
        """Fecha a conexão serial e sai do programa."""
        if self.arduino:
            self.arduino.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboControlApp(root)
    root.mainloop()
