import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading


class RoboControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle do Braço Robótico")

        self.arduino = None
        self.selected_port = tk.StringVar()

        # Armazena os ângulos atuais dos motores
        self.angles = {"B": 90, "M": 90, "S": 90, "G": 90}
        self.saved_positions = []  # Lista para armazenar posições salvas

        # Variáveis para auto-incremento (botões e teclado)
        self.increment_active = False
        self.increment_motor = None
        self.increment_value = 0
        self.increment_after_id = None  # ID do after agendado
        self.increment_label = None

        self.janela_selecao_serial()  # Inicia com a seleção da serial

        # Associa eventos de teclado para controle (podem ser ajustados conforme desejado)
        self.bind_teclas()

    def bind_teclas(self):
        # Exemplo: setas para controlar a Base (B) e Eixo Médio (M)
        self.root.bind("<KeyPress-Left>", lambda e: self.start_key_increment("B", -5))
        self.root.bind("<KeyPress-Right>", lambda e: self.start_key_increment("B", 5))
        self.root.bind("<KeyPress-Up>", lambda e: self.start_key_increment("M", 5))
        self.root.bind("<KeyPress-Down>", lambda e: self.start_key_increment("M", -5))
        self.root.bind("<KeyRelease-Left>", lambda e: self.stop_increment(e))
        self.root.bind("<KeyRelease-Right>", lambda e: self.stop_increment(e))
        self.root.bind("<KeyRelease-Up>", lambda e: self.stop_increment(e))
        self.root.bind("<KeyRelease-Down>", lambda e: self.stop_increment(e))

    def start_key_increment(self, motor, step):
        # Para teclas, não temos label para atualizar; apenas usa a lógica de auto-repetição
        if self.increment_active:
            return
        self.increment_active = True
        self.increment_motor = motor
        self.increment_value = step
        self.do_increment()

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
        """Janela para controle manual com botões de incremento contínuo."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Limpa e recria o dicionário de labels para atualização
        self.motor_labels = {}
        
        frame_manual = ttk.LabelFrame(self.root, text="Controle Manual")
        frame_manual.pack(padx=20, pady=20, fill="both", expand=True)
        
        ttk.Label(frame_manual, text="Ajuste os ângulos dos motores:", font=("Arial", 12)).pack(pady=10)
        
        motores = [("Base", "B"), ("Eixo Médio", "M"), ("Eixo Superior", "S"), ("Garra", "G")]
        for nome, codigo in motores:
            frame_motor = ttk.Frame(frame_manual)
            frame_motor.pack(pady=5)
            
            lbl = ttk.Label(frame_motor, text=f"{nome} ({self.angles[codigo]}°)")
            lbl.pack(side="left", padx=5)
            self.motor_labels[codigo] = lbl  # Armazena o label para atualização
            
            # Botão de decremento
            btn_dec = tk.Button(frame_motor, text="-", width=3)
            btn_dec.pack(side="left", padx=5)
            btn_dec.bind("<ButtonPress-1>", lambda e, c=codigo, val=-5: self.start_increment(e, c, val))
            btn_dec.bind("<ButtonRelease-1>", self.stop_increment)
            
            # Botão de incremento
            btn_inc = tk.Button(frame_motor, text="+", width=3)
            btn_inc.pack(side="left", padx=5)
            btn_inc.bind("<ButtonPress-1>", lambda e, c=codigo, val=5: self.start_increment(e, c, val))
            btn_inc.bind("<ButtonRelease-1>", self.stop_increment)
        
        ttk.Button(frame_manual, text="Salvar Posição Atual", command=self.salvar_posicao).pack(pady=10)
        ttk.Button(frame_manual, text="Voltar ao Menu", command=self.main_menu).pack(pady=10)

    def start_increment(self, event, motor, step):
        """Inicia o loop de incremento contínuo enquanto o botão estiver pressionado."""
        if self.increment_active and self.increment_motor == motor:
            return
        self.increment_active = True
        self.increment_motor = motor
        self.increment_value = step
        # Cancela qualquer agendamento pendente antes de iniciar
        if hasattr(self, "increment_after_id") and self.increment_after_id:
            self.root.after_cancel(self.increment_after_id)
            self.increment_after_id = None
        self.do_increment()

    def do_increment(self):
        """Realiza o incremento e agenda a próxima chamada se o botão ainda estiver pressionado."""
        if not self.increment_active:
            return

        current_angle = self.angles[self.increment_motor]
        proposed_angle = current_angle + self.increment_value
        novo_angulo = max(0, min(180, proposed_angle))
        
        if novo_angulo != current_angle:
            self.angles[self.increment_motor] = novo_angulo
            comando = f"{self.increment_motor}{novo_angulo}"
            self.enviar_comando(comando)
            if self.increment_motor in self.motor_labels:
                self.motor_labels[self.increment_motor].config(text=f"{self.increment_motor} ({novo_angulo}°)")
        
        # Se o ângulo atingiu o limite, interrompe o loop
        if novo_angulo != proposed_angle:
            self.increment_active = False
            if hasattr(self, "increment_after_id") and self.increment_after_id:
                self.root.after_cancel(self.increment_after_id)
                self.increment_after_id = None
            return

        # Agenda a próxima chamada após 250 ms e guarda o ID para poder cancelar
        self.increment_after_id = self.root.after(50, self.do_increment)

    def stop_increment(self, event):
        """Interrompe o loop de incremento contínuo."""
        self.increment_active = False
        if hasattr(self, "increment_after_id") and self.increment_after_id:
            self.root.after_cancel(self.increment_after_id)
            self.increment_after_id = None

    def start_key_increment(self, motor, step):
        """Inicia o incremento contínuo via tecla."""
        if self.increment_active and self.increment_motor == motor:
            return
        self.increment_active = True
        self.increment_motor = motor
        self.increment_value = step
        if hasattr(self, "increment_after_id") and self.increment_after_id:
            self.root.after_cancel(self.increment_after_id)
            self.increment_after_id = None
        self.do_increment()

    def bind_teclas(self):
        """Associa teclas do teclado a movimentos."""
        self.root.bind("<KeyPress-Left>", lambda e: self.start_key_increment("B", 5))
        self.root.bind("<KeyPress-Right>", lambda e: self.start_key_increment("B", -5))
        self.root.bind("<KeyPress-Up>", lambda e: self.start_key_increment("M", -5))
        self.root.bind("<KeyPress-Down>", lambda e: self.start_key_increment("M", 5))
        self.root.bind("<KeyRelease-Left>", lambda e: self.stop_increment(e))
        self.root.bind("<KeyRelease-Right>", lambda e: self.stop_increment(e))
        self.root.bind("<KeyRelease-Up>", lambda e: self.stop_increment(e))
        self.root.bind("<KeyRelease-Down>", lambda e: self.stop_increment(e))

    def salvar_posicao(self):
        """Salva a posição atual dos motores em um arquivo."""
        pos_str = f"B{self.angles['B']} M{self.angles['M']} S{self.angles['S']} G{self.angles['G']}\n"
        self.saved_positions.append(pos_str)

        with open("posicoes_salvas.txt", "w") as f:
            f.writelines(self.saved_positions)

        messagebox.showinfo("Sucesso", "Posição salva!")

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

        self.send_button = ttk.Button(frame_arquivo, text="Executar Comandos", command=self.executar_comandos, state="disabled")
        self.send_button.pack(pady=5)

        ttk.Button(self.root, text="Voltar ao Menu", command=self.main_menu).pack(pady=10)

    def selecionar_arquivo(self):
        """Abre um seletor de arquivos para escolher o arquivo de comandos."""
        self.filename = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if self.filename:
            self.file_label.config(text=self.filename)
            self.send_button.config(state="normal")

    def executar_comandos(self):
        """Executa os comandos armazenados em um arquivo em uma thread separada."""
        if not self.filename:
            messagebox.showerror("Erro", "Selecione um arquivo primeiro!")
            return

        threading.Thread(target=self._executar_comandos_thread).start()

    def _executar_comandos_thread(self):
        """Função que executa os comandos do arquivo em uma thread separada."""
        try:
            with open(self.filename, 'r') as arquivo:
                for linha in arquivo:
                    comando = linha.strip()
                    if comando:
                        self.enviar_comando(comando)
                        time.sleep(0.1)
            messagebox.showinfo("Sucesso", "Comandos executados!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar comandos: {str(e)}")


    def listar_portas(self):
        """Lista todas as portas seriais disponíveis."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def enviar_comando(self, comando):
        """Envia um comando via serial em uma thread separada."""
        if self.arduino:
            # Cria uma thread para enviar o comando
            threading.Thread(target=self._send_command_thread, args=(comando,)).start()
        else:
            messagebox.showerror("Erro", "Conecte primeiro ao Arduino!")

    def _send_command_thread(self, comando):
        """Função que realiza o envio do comando via serial."""
        self.arduino.write(f"{comando}\n".encode())
        print(f"Enviado: {comando}")


    def desconectar_serial(self):
        """Fecha a conexão serial e sai do programa."""
        if self.arduino:
            self.arduino.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboControlApp(root)
    root.mainloop()
