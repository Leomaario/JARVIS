import customtkinter as ctk


class JarvisGUI(ctk.CTk):

    def __init__(self, on_command_callback=None):
        super().__init__()

        self.on_command_callback = on_command_callback

        # ===== CONFIG WINDOW =====
        self.title("JARVIS AI System")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ===== GRID =====
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ===== FRAME PRINCIPAL =====
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # ===== TITULO =====
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="JARVIS SYSTEM",
            font=("Arial", 28, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=10)

        # ===== TERMINAL =====
        self.output_box = ctk.CTkTextbox(
            self.main_frame,
            height=400,
            font=("Consolas", 14)
        )
        self.output_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.output_box.insert("end", "Sistema iniciado...\n")
        self.output_box.configure(state="disabled")

        # ===== INPUT =====
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Digite um comando..."
        )
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=5)
        self.input_entry.bind("<Return>", self._send_command)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Enviar",
            command=self._send_command
        )
        self.send_button.grid(row=0, column=1, padx=5)

    # ===== PRINT NA TELA =====
    def log(self, text):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    # ===== ENVIA COMANDO =====
    def _send_command(self, event=None):
        command = self.input_entry.get().strip()

        if not command:
            return

        self.log(f"> {command}")
        self.input_entry.delete(0, "end")

        if self.on_command_callback:
            response = self.on_command_callback(command)
            if response:
                self.log(response)

    def run(self):
        self.mainloop()