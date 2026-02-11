import tkinter as tk
from tkinter import messagebox, ttk

class CalculadoraTrimestralPMPV:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão PMPV - Visão Trimestral")
        self.root.geometry("1200x750")
        self.root.configure(bg="#ecf0f1")
        
        self.empresas_padrao = ["PETROBRAS", "GALP", "PETRORECONCAVO", "BRAVA", "ENEVA", "ORIZON"]
        
        # Dicionário para armazenar as referências de cada mês
        # Estrutura: self.meses['Mês 1'] = [lista_de_entradas]
        self.dados_por_mes = {}

        self._setup_ui()

    def _setup_ui(self):
        # --- Título Superior ---
        frame_top = tk.Frame(self.root, bg="#2c3e50", pady=18)
        frame_top.pack(fill="x")
        tk.Label(frame_top, text="Calculadora de Preço Médio Ponderado (PMPV)", 
                 font=("Segoe UI", 18, "bold"), bg="#2c3e50", fg="white").pack()
        tk.Label(frame_top, text="Sistema de Gestão Trimestral de Contratos", 
                 font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7").pack()

        # --- Sistema de Abas (Notebook) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Criar 3 abas para os meses
        for i in range(1, 4):
            nome_mes = f"Mês {i}"
            aba = tk.Frame(self.notebook, bg="#fafafa")
            self.notebook.add(aba, text=f"  {nome_mes}  ")
            self.dados_por_mes[nome_mes] = self._criar_area_mes(aba, nome_mes)

        # --- Rodapé de Resultados Fixos ---
        self.frame_footer = tk.Frame(self.root, bg="#34495e", pady=25)
        self.frame_footer.pack(fill="x", side="bottom")

        self.lbl_trimestral = tk.Label(self.frame_footer, 
                                      text="RESULTADO TRIMESTRAL: Aguardando dados...", 
                                      font=("Segoe UI", 13, "bold"), fg="#ecf0f1", bg="#34495e")
        self.lbl_trimestral.pack(pady=(0, 12))

        btn_calc_trimestre = tk.Button(self.frame_footer, text="⚡ GERAR FECHAMENTO TRIMESTRAL", 
                                       command=self.calcular_trimestre, bg="#27ae60", fg="white",
                                       font=("Segoe UI", 12, "bold"), padx=30, pady=12, 
                                       relief="flat", cursor="hand2", activebackground="#229954")
        btn_calc_trimestre.pack()

    def _criar_area_mes(self, parent, nome_mes_atual):
        # Cabeçalho interno da aba
        header_bg = "#34495e"
        h_frame = tk.Frame(parent, bg=header_bg, padx=15, pady=12)
        h_frame.pack(fill="x")

        titles = [("Empresa / Contrato", 27), ("Molécula", 13), ("Transporte", 13), 
                  ("Logística", 13), ("Preço Final", 16), ("Volume (m³/dia)", 17), ("Ações", 10)]
        
        for txt, w in titles:
            tk.Label(h_frame, text=txt, width=w, font=("Segoe UI", 9, "bold"), 
                     bg=header_bg, fg="white", anchor="center").pack(side="left", padx=3)

        # Scroll Area com design melhorado
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

        # Botão de Adicionar Empresa no final
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

        # Widgets com design melhorado e alinhamento consistente
        e_nome = tk.Entry(row, width=29, font=("Segoe UI", 10), relief="solid", 
                          bd=1, highlightthickness=0)
        e_nome.insert(0, nome)
        e_nome.pack(side="left", padx=3, ipady=4)

        e_mol = tk.Entry(row, width=14, justify="center", font=("Segoe UI", 10), 
                        relief="solid", bd=1, highlightthickness=0)
        e_mol.pack(side="left", padx=3, ipady=4)

        e_trans = tk.Entry(row, width=14, justify="center", font=("Segoe UI", 10), 
                          relief="solid", bd=1, highlightthickness=0)
        e_trans.pack(side="left", padx=3, ipady=4)

        e_log = tk.Entry(row, width=14, justify="center", font=("Segoe UI", 10), 
                        relief="solid", bd=1, highlightthickness=0)
        e_log.pack(side="left", padx=3, ipady=4)

        lbl_soma = tk.Label(row, text="0.0000", width=17, font=("Segoe UI", 10, "bold"), 
                           bg="#e3f2fd", fg="#1976d2", relief="solid", bd=1, anchor="center")
        lbl_soma.pack(side="left", padx=3, ipady=4)

        e_vol = tk.Entry(row, width=19, justify="center", font=("Segoe UI", 10, "bold"), 
                        bg="#fff9c4", relief="solid", bd=1, highlightthickness=0, fg="#f57c00")
        e_vol.pack(side="left", padx=3, ipady=4)

        # Botão de Copiar (Roxo)
        btn_copiar = tk.Button(row, text="📋", 
                               command=lambda: self._copiar_linha_para_outro_mes(dados),
                               bg="#9b59b6", fg="white", font=("Segoe UI", 10, "bold"),
                               width=3, relief="flat", cursor="hand2")
        btn_copiar.pack(side="left", padx=2, ipady=2)

        # Botão de Remover
        btn_remove = tk.Button(row, text="🗑️", 
                               command=lambda: self._remover_linha(row, dados, lista_referencia),
                               bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"),
                               width=3, relief="flat", cursor="hand2")
        btn_remove.pack(side="left", padx=2, ipady=2)

        dados = {'nome': e_nome, 'mol': e_mol, 'trans': e_trans, 'log': e_log, 
                 'lbl_soma': lbl_soma, 'vol': e_vol, 'row': row, 
                 'btn_copiar': btn_copiar, 'btn_remove': btn_remove}
        
        # Bind para cálculo automático do preço final na linha
        for e in [e_mol, e_trans, e_log]:
            e.bind("<KeyRelease>", lambda event, d=dados: self._update_row_total(d))
            
        return dados

    def _update_row_total(self, d):
        total = self._get_val(d['mol']) + self._get_val(d['trans']) + self._get_val(d['log'])
        d['lbl_soma'].config(text=f"{total:.4f}")

    def _get_val(self, entry):
        try:
            v = entry.get().replace(',', '.')
            return float(v) if v else 0.0
        except: return 0.0

    def _adicionar_nova_linha(self, parent_frame, lista_referencia):
        """Adiciona uma nova linha em branco para o usuário preencher"""
        entry_dict = self._adicionar_linha_tabela(parent_frame, "Nova Empresa", lista_referencia)
        lista_referencia.append(entry_dict)
        entry_dict['nome'].focus_set()
        entry_dict['nome'].select_range(0, tk.END)
    
    def _remover_linha(self, row_frame, dados, lista_referencia):
        """Remove uma linha específica da interface e da lista"""
        empresa = dados['nome'].get()
        confirmacao = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover a empresa:\n'{empresa}'?"
        )
        
        if confirmacao:
            row_frame.destroy()
            if dados in lista_referencia:
                lista_referencia.remove(dados)
    
    def _copiar_linha_para_outro_mes(self, dados_origem):
        """Copia uma linha específica para outro mês"""
        # Descobrir em qual mês estamos
        mes_atual = None
        for nome_mes, linhas in self.dados_por_mes.items():
            if dados_origem in linhas:
                mes_atual = nome_mes
                break
        
        if not mes_atual:
            messagebox.showerror("Erro", "Não foi possível identificar o mês atual.")
            return
        
        # Criar janela de seleção
        janela = tk.Toplevel(self.root)
        janela.title("Copiar Linha")
        janela.geometry("350x250")
        janela.configure(bg="#f0f0f0")
        janela.resizable(False, False)
        
        # Tornar modal
        janela.transient(self.root)
        janela.grab_set()
        
        empresa = dados_origem['nome'].get()
        
        tk.Label(janela, text="📋 Copiar Linha", font=("Segoe UI", 14, "bold"), 
                bg="#f0f0f0", fg="#9b59b6").pack(pady=15)
        
        tk.Label(janela, text=f"Empresa: {empresa}", font=("Segoe UI", 10), 
                bg="#f0f0f0").pack(pady=5)
        
        tk.Label(janela, text="Copiar para qual mês?", font=("Segoe UI", 10, "bold"), 
                bg="#f0f0f0").pack(pady=10)
        
        # Botões para cada mês (exceto o atual)
        for nome_mes in ["Mês 1", "Mês 2", "Mês 3"]:
            if nome_mes != mes_atual:
                btn = tk.Button(janela, text=f"➡️ {nome_mes}", 
                               command=lambda m=nome_mes: self._executar_copia_linha(dados_origem, m, janela),
                               bg="#9b59b6", fg="white", font=("Segoe UI", 11, "bold"),
                               padx=20, pady=10, relief="flat", cursor="hand2", width=15)
                btn.pack(pady=5)
        
        tk.Button(janela, text="Cancelar", command=janela.destroy,
                 bg="#95a5a6", fg="white", font=("Segoe UI", 9),
                 padx=15, pady=5, relief="flat", cursor="hand2").pack(pady=10)
    
    def _executar_copia_linha(self, dados_origem, mes_destino, janela_selecao):
        """Executa a cópia da linha para o mês selecionado"""
        empresa = dados_origem['nome'].get()
        
        # Fechar janela de seleção
        janela_selecao.destroy()
        
        dados_destino = self.dados_por_mes[mes_destino]
        
        # Procurar se já existe uma linha com o mesmo nome
        linha_existente = None
        for d in dados_destino:
            if d['nome'].get() == empresa:
                linha_existente = d
                break
        
        # Se encontrou, perguntar se quer sobrescrever
        if linha_existente:
            confirmacao = messagebox.askyesno(
                "Empresa já existe",
                f"A empresa '{empresa}' já existe no {mes_destino}.\n\n"
                f"Deseja SOBRESCREVER os dados existentes?"
            )
            if not confirmacao:
                return
            destino = linha_existente
        else:
            # Procurar primeira linha vazia
            destino = None
            for d in dados_destino:
                if not d['nome'].get() or d['nome'].get().startswith("Fornecedor") or d['nome'].get() == "Nova Empresa":
                    destino = d
                    break
            
            if not destino:
                messagebox.showwarning(
                    "Sem Espaço",
                    f"Não há linhas vazias no {mes_destino}.\n\n"
                    f"Use o botão ➕ para adicionar uma nova linha primeiro."
                )
                return
        
        # Copiar os dados
        destino['nome'].delete(0, tk.END)
        destino['nome'].insert(0, dados_origem['nome'].get())
        
        destino['mol'].delete(0, tk.END)
        destino['mol'].insert(0, dados_origem['mol'].get())
        
        destino['trans'].delete(0, tk.END)
        destino['trans'].insert(0, dados_origem['trans'].get())
        
        destino['log'].delete(0, tk.END)
        destino['log'].insert(0, dados_origem['log'].get())
        
        destino['vol'].delete(0, tk.END)
        destino['vol'].insert(0, dados_origem['vol'].get())
        
        # Atualizar a soma
        self._update_row_total(destino)
        
        messagebox.showinfo(
            "✓ Linha Copiada",
            f"Empresa '{empresa}' copiada para {mes_destino} com sucesso!"
        )
    _adicionar_nova_linha

    def calcular_trimestre(self):
        custo_total_trimestre = 0.0
        volume_total_trimestre = 0.0
        
        # Percorrer os 3 meses
        for mes, linhas in self.dados_por_mes.items():
            for l in linhas:
                vol = self._get_val(l['vol'])
                if vol > 0:
                    preco = self._get_val(l['mol']) + self._get_val(l['trans']) + self._get_val(l['log'])
                    custo_total_trimestre += (preco * vol)
                    volume_total_trimestre += vol

        if volume_total_trimestre == 0:
            messagebox.showwarning("Dados Insuficientes", "Por favor, preencha o volume em pelo menos um dos meses.")
            return

        pmpv_trimestral = custo_total_trimestre / volume_total_trimestre
        
        self.lbl_trimestral.config(
            text=f"✓ FECHAMENTO TRIMESTRAL | Volume: {volume_total_trimestre:,.0f} m³ | PMPV: R$ {pmpv_trimestral:.4f}",
            fg="#2ecc71"
        )
        
        messagebox.showinfo("✓ Relatório Trimestral", 
                            f"Cálculo Concluído com Sucesso!\n\n"
                            f"📊 Volume Total do Período: {volume_total_trimestre:,.0f} m³\n"
                            f"💰 Custo Total Estimado: R$ {custo_total_trimestre:,.2f}\n"
                            f"📈 PMPV Final do Trimestre: R$ {pmpv_trimestral:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Estilo melhorado para as abas
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook", background="#ecf0f1", borderwidth=0)
    style.configure("TNotebook.Tab", 
                   font=("Segoe UI", 11, "bold"), 
                   padding=[20, 10],
                   background="#bdc3c7")
    style.map("TNotebook.Tab", 
             background=[("selected", "#3498db")],
             foreground=[("selected", "white"), ("!selected", "#34495e")])
    
    app = CalculadoraTrimestralPMPV(root)
    root.mainloop()