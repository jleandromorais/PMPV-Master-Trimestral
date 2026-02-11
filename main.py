import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from database import DatabasePMPV
from excel_handler import ExcelHandlerPMPV
from datetime import datetime

class CalculadoraTrimestralPMPV:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão PMPV - Visão Trimestral")
        self.root.geometry("1280x850")
        self.root.configure(bg="#ecf0f1")
        
        # Inicializar Banco de Dados
        self.db = DatabasePMPV()
        
        self.empresas_padrao = ["PETROBRAS", "GALP", "PETRORECONCAVO", "BRAVA", "ENEVA", "ORIZON"]
        
        # Configuração de Dias Padrão
        self.mapa_dias_padrao = {
            "Janeiro": 31, "Fevereiro": 28, "Março": 31, "Abril": 30,
            "Maio": 31, "Junho": 30, "Julho": 31, "Agosto": 31,
            "Setembro": 30, "Outubro": 31, "Novembro": 30, "Dezembro": 31
        }
        self.lista_meses = list(self.mapa_dias_padrao.keys())
        
        # Estado atual dos dias (será atualizado dinamicamente)
        self.dias_mes_config = {
            "Mês 1": 30, 
            "Mês 2": 30, 
            "Mês 3": 30
        }
        
        self.dados_por_mes = {} # Mês 1, Mês 2, Mês 3

        self._setup_ui()

    def _setup_ui(self):
        # --- Título Superior ---
        frame_top = tk.Frame(self.root, bg="#2c3e50", pady=15)
        frame_top.pack(fill="x")
        
        tk.Label(frame_top, text="Calculadora de Preço Médio Ponderado (PMPV)", 
                 font=("Segoe UI", 18, "bold"), bg="#2c3e50", fg="white").pack()
        
        # --- Frame de Configuração do Trimestre ---
        frame_config = tk.Frame(self.root, bg="#bdc3c7", pady=8, padx=10)
        frame_config.pack(fill="x")
        
        tk.Label(frame_config, text="📅 Configuração do Trimestre:", 
                 font=("Segoe UI", 11, "bold"), bg="#bdc3c7", fg="#2c3e50").pack(side="left")
        
        tk.Label(frame_config, text="Mês Inicial:", 
                 font=("Segoe UI", 10), bg="#bdc3c7").pack(side="left", padx=(20, 5))
        
        # Combobox para escolher o mês
        self.combo_mes_inicio = ttk.Combobox(frame_config, values=self.lista_meses, 
                                            state="readonly", width=15, font=("Segoe UI", 10))
        self.combo_mes_inicio.set("Novembro") # Padrão conforme nota técnica
        self.combo_mes_inicio.pack(side="left")
        self.combo_mes_inicio.bind("<<ComboboxSelected>>", self._atualizar_trimestre)
        
        # Checkbox para Ano Bissexto (para Fevereiro)
        self.var_bissexto = tk.BooleanVar()
        self.chk_bissexto = tk.Checkbutton(frame_config, text="Ano Bissexto (Fev=29)?", 
                                          variable=self.var_bissexto, bg="#bdc3c7", 
                                          command=self._atualizar_trimestre, font=("Segoe UI", 9))
        self.chk_bissexto.pack(side="left", padx=15)

        # --- Sistema de Abas (Notebook) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Criar 3 abas para os meses (internamente ainda usamos "Mês 1", "Mês 2"...)
        for i in range(1, 4):
            key_mes = f"Mês {i}"
            aba = tk.Frame(self.notebook, bg="#fafafa")
            self.notebook.add(aba, text=f" {key_mes} ") # Texto provisório
            self.dados_por_mes[key_mes] = self._criar_area_mes(aba)

        # Atualizar os títulos das abas com base no padrão inicial
        self._atualizar_trimestre()

        # --- Frame de Ações (Salvar/Exportar) ---
        frame_acoes = tk.Frame(self.root, bg="#ecf0f1", pady=5)
        frame_acoes.pack(fill="x", side="bottom")

        # --- Rodapé de Resultados ---
        self.frame_footer = tk.Frame(self.root, bg="#34495e", pady=20)
        self.frame_footer.pack(fill="x", side="bottom")

        # Área de Conta Gráfica e Botão Calcular
        frame_calc = tk.Frame(self.frame_footer, bg="#34495e")
        frame_calc.pack()

        tk.Label(frame_calc, text="Conta Gráfica / Recuperação (R$):", 
                 font=("Segoe UI", 10, "bold"), bg="#34495e", fg="#bdc3c7").pack(side="left", padx=5)
        
        self.entry_conta_grafica = tk.Entry(frame_calc, width=12, font=("Segoe UI", 11), justify="center")
        self.entry_conta_grafica.insert(0, "-0.0210") 
        self.entry_conta_grafica.pack(side="left", padx=5)

        btn_calc_trimestre = tk.Button(frame_calc, text="⚡ GERAR FECHAMENTO", 
                                       command=self.calcular_trimestre, bg="#27ae60", fg="white",
                                       font=("Segoe UI", 11, "bold"), padx=20, pady=8, 
                                       relief="flat", cursor="hand2", activebackground="#229954")
        btn_calc_trimestre.pack(side="left", padx=20)

        # Labels de Resultado
        self.lbl_pmpv = tk.Label(self.frame_footer, 
                                      text="PMPV: ...", 
                                      font=("Segoe UI", 14), fg="#ecf0f1", bg="#34495e")
        self.lbl_pmpv.pack(pady=(10, 2))
        
        self.lbl_final = tk.Label(self.frame_footer, 
                                      text="PREÇO FINAL (PV): ...", 
                                      font=("Segoe UI", 16, "bold"), fg="#f1c40f", bg="#34495e")
        self.lbl_final.pack(pady=(0, 10))

        # Botões de Ações
        btn_save = tk.Button(frame_acoes, text="💾 Salvar Sessão (DB)", 
                             command=self.salvar_sessao, bg="#8e44ad", fg="white",
                             font=("Segoe UI", 10, "bold"), padx=15, pady=5, relief="flat", cursor="hand2")
        btn_save.pack(side="right", padx=15, pady=5)
        
        btn_export = tk.Button(frame_acoes, text="📊 Exportar Excel", 
                               command=self.exportar_excel, bg="#2980b9", fg="white",
                               font=("Segoe UI", 10, "bold"), padx=15, pady=5, relief="flat", cursor="hand2")
        btn_export.pack(side="right", padx=5, pady=5)

    def _atualizar_trimestre(self, event=None):
        """Atualiza os nomes e dias dos meses com base na seleção inicial"""
        mes_inicio = self.combo_mes_inicio.get()
        if not mes_inicio: return

        try:
            idx_inicio = self.lista_meses.index(mes_inicio)
        except ValueError:
            return

        eh_bissexto = self.var_bissexto.get()

        # Calcular os 3 meses sequenciais
        for i in range(3):
            idx_atual = (idx_inicio + i) % 12
            nome_mes = self.lista_meses[idx_atual]
            
            # Definir dias
            dias = self.mapa_dias_padrao[nome_mes]
            if nome_mes == "Fevereiro" and eh_bissexto:
                dias = 29
            
            # Atualizar config interna
            key_mes = f"Mês {i+1}"
            self.dias_mes_config[key_mes] = dias
            
            # Atualizar Título da Aba
            self.notebook.tab(i, text=f"  {nome_mes} ({dias}d)  ")

    def _criar_area_mes(self, parent):
        # Cabeçalho interno da aba
        header_bg = "#34495e"
        h_frame = tk.Frame(parent, bg=header_bg, padx=15, pady=12)
        h_frame.pack(fill="x")

        titles = [("Empresa / Contrato", 27), ("Molécula", 13), ("Transporte", 13), 
                  ("Logística", 13), ("Preço Final", 16), ("QDC (m³/dia)", 17), ("Ações", 10)]
        
        for txt, w in titles:
            tk.Label(h_frame, text=txt, width=w, font=("Segoe UI", 9, "bold"), 
                     bg=header_bg, fg="white", anchor="center").pack(side="left", padx=3)

        # Scroll Area
        canvas = tk.Canvas(parent, bg="#fafafa", highlightthickness=0, bd=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#fafafa")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5)
        scroll.pack(side="right", fill="y")

        # Gerar linhas iniciais
        lista_entries_mes = []
        for emp in self.empresas_padrao:
            entry_dict = self._adicionar_linha_tabela(scroll_frame, emp, lista_entries_mes)
            lista_entries_mes.append(entry_dict)

        # Botão de Adicionar Empresa
        btn_frame = tk.Frame(parent, bg="#fafafa", pady=10)
        btn_frame.pack(fill="x")
        
        btn_add = tk.Button(btn_frame, text="➕ Adicionar Nova Empresa", 
                           command=lambda: self._adicionar_nova_linha(scroll_frame, lista_entries_mes),
                           bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"),
                           padx=15, pady=8, relief="flat", cursor="hand2")
        btn_add.pack()

        return lista_entries_mes

    def _adicionar_linha_tabela(self, parent, nome, lista_referencia):
        idx = len(lista_referencia)
        bg_color = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
        
        row = tk.Frame(parent, bg=bg_color, pady=8, padx=15)
        row.pack(fill="x", expand=True)

        # Widgets
        e_nome = tk.Entry(row, width=29, font=("Segoe UI", 10), relief="solid", bd=1)
        e_nome.insert(0, nome)
        e_nome.pack(side="left", padx=3, ipady=4)

        e_mol = tk.Entry(row, width=14, justify="center", font=("Segoe UI", 10), relief="solid", bd=1)
        e_mol.pack(side="left", padx=3, ipady=4)

        e_trans = tk.Entry(row, width=14, justify="center", font=("Segoe UI", 10), relief="solid", bd=1)
        e_trans.pack(side="left", padx=3, ipady=4)

        e_log = tk.Entry(row, width=14, justify="center", font=("Segoe UI", 10), relief="solid", bd=1)
        e_log.pack(side="left", padx=3, ipady=4)

        lbl_soma = tk.Label(row, text="0.0000", width=17, font=("Segoe UI", 10, "bold"), 
                           bg="#e3f2fd", fg="#1976d2", relief="solid", bd=1, anchor="center")
        lbl_soma.pack(side="left", padx=3, ipady=4)

        e_vol = tk.Entry(row, width=19, justify="center", font=("Segoe UI", 10, "bold"), 
                        bg="#fff9c4", relief="solid", bd=1, fg="#f57c00")
        e_vol.pack(side="left", padx=3, ipady=4)

        # Botões de Ação na Linha
        btn_copiar = tk.Button(row, text="📋", 
                               command=lambda: self._copiar_linha_para_outro_mes(dados),
                               bg="#9b59b6", fg="white", font=("Segoe UI", 10, "bold"),
                               width=3, relief="flat", cursor="hand2")
        btn_copiar.pack(side="left", padx=2, ipady=2)

        btn_remove = tk.Button(row, text="🗑️", 
                               command=lambda: self._remover_linha(row, dados, lista_referencia),
                               bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"),
                               width=3, relief="flat", cursor="hand2")
        btn_remove.pack(side="left", padx=2, ipady=2)

        dados = {'nome': e_nome, 'mol': e_mol, 'trans': e_trans, 'log': e_log, 
                 'lbl_soma': lbl_soma, 'vol': e_vol, 'row': row, 
                 'btn_copiar': btn_copiar, 'btn_remove': btn_remove}
        
        # Bind para cálculo
        for e in [e_mol, e_trans, e_log]:
            e.bind("<KeyRelease>", lambda event, d=dados: self._update_row_total(d))
            
        return dados

    def _update_row_total(self, d):
        total = self._get_val(d['mol']) + self._get_val(d['trans']) + self._get_val(d['log'])
        d['lbl_soma'].config(text=f"{total:.4f}")

    def _get_val(self, entry):
        try:
            if isinstance(entry, tk.Entry):
                v = entry.get().replace(',', '.')
            else:
                v = str(entry).replace(',', '.')
            return float(v) if v else 0.0
        except: return 0.0

    def _adicionar_nova_linha(self, parent_frame, lista_referencia):
        entry_dict = self._adicionar_linha_tabela(parent_frame, "Nova Empresa", lista_referencia)
        lista_referencia.append(entry_dict)
        entry_dict['nome'].focus_set()
        entry_dict['nome'].select_range(0, tk.END)
    
    def _remover_linha(self, row_frame, dados, lista_referencia):
        empresa = dados['nome'].get()
        if messagebox.askyesno("Confirmar", f"Remover '{empresa}'?"):
            row_frame.destroy()
            if dados in lista_referencia:
                lista_referencia.remove(dados)
    
    def _copiar_linha_para_outro_mes(self, dados_origem):
        # Descobre qual "Mês X" estamos com base na lista de dados
        mes_atual_key = None
        for key, linhas in self.dados_por_mes.items():
            if dados_origem in linhas:
                mes_atual_key = key
                break
        
        if not mes_atual_key: return
        
        # Pega o nome real do mês para exibir na UI
        try:
            idx_aba = int(mes_atual_key.split()[-1]) - 1
            nome_mes_origem = self.notebook.tab(idx_aba, "text").strip()
        except:
            nome_mes_origem = mes_atual_key

        janela = tk.Toplevel(self.root)
        janela.title("Copiar Linha")
        janela.geometry("300x280")
        janela.transient(self.root)
        janela.grab_set()
        janela.configure(bg="#ecf0f1")
        
        tk.Label(janela, text=f"Copiar '{dados_origem['nome'].get()}'\n(de {nome_mes_origem}) para:", 
                 font=("Segoe UI", 11, "bold"), bg="#ecf0f1").pack(pady=15)
        
        # Botões para os outros meses
        for i in range(3):
            key_destino = f"Mês {i+1}"
            if key_destino != mes_atual_key:
                # Pega o nome real do destino
                nome_destino = self.notebook.tab(i, "text").strip()
                
                tk.Button(janela, text=f"➡️ {nome_destino}", 
                          command=lambda k=key_destino: self._executar_copia_linha(dados_origem, k, janela),
                          bg="#9b59b6", fg="white", font=("Segoe UI", 10),
                          padx=20, pady=8, relief="flat", cursor="hand2", width=20).pack(pady=5)
    
    def _executar_copia_linha(self, dados_origem, mes_destino_key, janela):
        janela.destroy()
        dados_destino = self.dados_por_mes[mes_destino_key]
        
        # Procura linha vazia ou cria nova se necessário
        destino = None
        for d in dados_destino:
            if d['nome'].get() == "Nova Empresa" or d['nome'].get() == "":
                destino = d
                break
        
        if not destino:
             # Pega o nome amigável para o aviso
             idx = int(mes_destino_key.split()[-1]) - 1
             nome_amigavel = self.notebook.tab(idx, "text").strip()
             messagebox.showinfo("Aviso", f"Adicione uma linha vazia em '{nome_amigavel}' antes de copiar.")
             return

        # Copia valores
        campos = ['nome', 'mol', 'trans', 'log', 'vol']
        for campo in campos:
            destino[campo].delete(0, tk.END)
            destino[campo].insert(0, dados_origem[campo].get())
        
        self._update_row_total(destino)
        
        # Feedback visual
        nome_empresa = dados_origem['nome'].get()
        idx = int(mes_destino_key.split()[-1]) - 1
        nome_destino_amigavel = self.notebook.tab(idx, "text").strip()
        messagebox.showinfo("Sucesso", f"Empresa '{nome_empresa}' copiada para {nome_destino_amigavel}!")

    # --- LÓGICA DE CÁLCULO ---
    def calcular_trimestre(self):
        custo_total_trimestre = 0.0
        volume_total_trimestre = 0.0
        
        try:
            conta_grafica = self._get_val(self.entry_conta_grafica)
        except:
            conta_grafica = 0.0

        # Percorrer os 3 meses
        for key_mes, linhas in self.dados_por_mes.items():
            # Recupera quantos dias tem aquele mês (da config dinâmica)
            dias_no_mes = self.dias_mes_config.get(key_mes, 30)
            
            for l in linhas:
                qdc = self._get_val(l['vol']) # Volume Diário
                
                if qdc > 0:
                    vol_mensal = qdc * dias_no_mes
                    
                    preco_unit = self._get_val(l['mol']) + self._get_val(l['trans']) + self._get_val(l['log'])
                    
                    custo_total_trimestre += (preco_unit * vol_mensal)
                    volume_total_trimestre += vol_mensal

        if volume_total_trimestre == 0:
            messagebox.showwarning("Dados Insuficientes", "Preencha o volume em pelo menos um mês.")
            return

        pmpv = custo_total_trimestre / volume_total_trimestre
        preco_final = pmpv + conta_grafica
        
        # Atualiza Interface
        self.lbl_pmpv.config(text=f"PMPV Calculado: R$ {pmpv:.4f}")
        self.lbl_final.config(text=f"PREÇO FINAL (PV): R$ {preco_final:.4f}")
        
        self.ultimo_resultado = {
            'volume_total': volume_total_trimestre,
            'custo_total': custo_total_trimestre,
            'pmpv': pmpv,
            'conta_grafica': conta_grafica,
            'preco_final': preco_final
        }

        messagebox.showinfo("Cálculo Realizado", 
                            f"Volume Total (com dias): {volume_total_trimestre:,.0f} m³\n"
                            f"PMPV: R$ {pmpv:.4f}\n"
                            f"PV Final: R$ {preco_final:.4f}")

    # --- INTEGRAÇÃO ---
    def _extrair_dados_dict(self):
        dados_export = {}
        for key_mes, linhas in self.dados_por_mes.items():
            # Usa o nome amigável (Janeiro, Fevereiro...) para o Excel ficar bonito
            idx = int(key_mes.split()[-1]) - 1
            nome_real = self.notebook.tab(idx, "text").strip().split(" ")[0] # Pega só "Janeiro"
            
            lista_mes = []
            for l in linhas:
                if l['nome'].get():
                    lista_mes.append({
                        'empresa': l['nome'].get(),
                        'molecula': self._get_val(l['mol']),
                        'transporte': self._get_val(l['trans']),
                        'logistica': self._get_val(l['log']),
                        'volume': self._get_val(l['vol'])
                    })
            dados_export[nome_real] = lista_mes # Salva com nome real ("Janeiro")
        return dados_export

    def salvar_sessao(self):
        nome = simpledialog.askstring("Salvar Sessão", "Nome do Trimestre (ex: Q1 2026):")
        if not nome: return
        
        sessao_id = self.db.criar_sessao(nome)
        dados_ui = self._extrair_dados_dict()
        
        # Salva usando índice 1, 2, 3 (a ordem importa, não o nome)
        idx = 1
        for nome_mes, dados in dados_ui.items():
            self.db.salvar_dados_mes(sessao_id, idx, dados)
            idx += 1
            
        if hasattr(self, 'ultimo_resultado'):
            self.db.salvar_resultado(
                sessao_id, 
                self.ultimo_resultado['volume_total'],
                self.ultimo_resultado['pmpv'],
                self.ultimo_resultado['custo_total']
            )
            
        messagebox.showinfo("Salvo", f"Sessão '{nome}' salva com sucesso!")

    def exportar_excel(self):
        if not hasattr(self, 'ultimo_resultado'):
            messagebox.showwarning("Aviso", "Calcule o trimestre antes de exportar.")
            return
            
        dados_ui = self._extrair_dados_dict() # Agora vem com nomes reais (Janeiro...)
        
        try:
            # Precisamos converter de volta para "Mês 1", "Mês 2" pro ExcelHandler entender
            # Ou ajustar o ExcelHandler. Vamos ajustar os dados aqui rápido:
            dados_formatados = {}
            i = 1
            for nome_real, dados in dados_ui.items():
                dados_formatados[f"Mês {i}"] = dados
                i += 1

            arquivo = ExcelHandlerPMPV.exportar_trimestre(dados_formatados, self.ultimo_resultado)
            messagebox.showinfo("Excel", f"Gerado: {arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook", background="#ecf0f1", borderwidth=0)
    style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[20, 10], background="#bdc3c7")
    style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "white"), ("!selected", "#34495e")])
    
    app = CalculadoraTrimestralPMPV(root)
    root.mainloop()