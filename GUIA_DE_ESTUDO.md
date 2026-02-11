# 📚 Guia de Estudo - Calculadora PMPV

Este guia explica **COMO** o código funciona, linha por linha, para você entender e poder modificar!

---

## 📋 Índice

1. [Estrutura Geral](#estrutura-geral)
2. [Classe Principal](#classe-principal)
3. [Sistema de Abas](#sistema-de-abas)
4. [Criação de Linhas](#criação-de-linhas)
5. [Botões e Ações](#botões-e-ações)
6. [Cálculo do PMPV](#cálculo-do-pmpv)
7. [Fluxo de Dados](#fluxo-de-dados)
8. [Conceitos Importantes](#conceitos-importantes)

---

## 🏗️ Estrutura Geral

### Arquitetura do Código

```
main.py
│
├── Imports (tkinter, messagebox, ttk)
│
└── class CalculadoraTrimestralPMPV
    │
    ├── __init__()              # Construtor - inicializa tudo
    ├── _setup_ui()             # Monta a interface gráfica
    │
    ├── _criar_area_mes()       # Cria uma aba (Mês 1, 2 ou 3)
    ├── _adicionar_linha_tabela() # Cria uma linha de empresa
    │
    ├── _update_row_total()     # Atualiza Preço Final (tempo real)
    ├── _get_val()              # Pega valor de um Entry
    │
    ├── _adicionar_nova_linha() # Adiciona nova empresa
    ├── _remover_linha()        # Remove uma empresa
    │
    ├── _copiar_linha_para_outro_mes()  # Abre janela de seleção
    ├── _executar_copia_linha() # Executa a cópia
    │
    └── calcular_trimestre()    # Calcula PMPV trimestral
```

---

## 🎯 Classe Principal

### Linha 4-17: O Construtor

```python
def __init__(self, root):
    self.root = root
    self.root.title("Sistema de Gestão PMPV - Visão Trimestral")
    self.root.geometry("1200x750")
    self.root.configure(bg="#ecf0f1")
    
    self.empresas_padrao = ["Fornecedor 1", "Fornecedor 2", ...]
    
    # Dicionário que guarda TODAS as linhas de TODOS os meses
    self.dados_por_mes = {}
    
    self._setup_ui()
```

**O que acontece aqui:**

1. `self.root = root`: Guarda referência da janela principal
2. `.title()`: Define o título da janela
3. `.geometry()`: Define tamanho (1200x750 pixels)
4. `.configure()`: Define cor de fundo
5. `self.empresas_padrao`: Lista com nomes padrão
6. `self.dados_por_mes = {}`: **IMPORTANTE!** Dicionário que vai guardar:
   ```python
   {
       "Mês 1": [linha1, linha2, linha3, ...],
       "Mês 2": [linha1, linha2, linha3, ...],
       "Mês 3": [linha1, linha2, linha3, ...]
   }
   ```

---

## 📑 Sistema de Abas

### Linha 19-51: _setup_ui()

```python
def _setup_ui(self):
    # 1. Título no topo
    frame_top = tk.Frame(self.root, bg="#2c3e50", pady=18)
    frame_top.pack(fill="x")
    
    # 2. Sistema de abas
    self.notebook = ttk.Notebook(self.root)
    self.notebook.pack(fill="both", expand=True, padx=15, pady=10)
    
    # 3. Cria 3 abas (Mês 1, 2, 3)
    for i in range(1, 4):
        nome_mes = f"Mês {i}"
        aba = tk.Frame(self.notebook, bg="#fafafa")
        self.notebook.add(aba, text=f"  {nome_mes}  ")
        
        # CHAMA a função que cria o conteúdo da aba
        self.dados_por_mes[nome_mes] = self._criar_area_mes(aba, nome_mes)
    
    # 4. Rodapé (botão calcular + resultado)
    # ...
```

**Conceitos:**

- **Frame**: Caixa retangular que agrupa widgets
- **pack()**: Organiza widgets verticalmente (um embaixo do outro)
- **Notebook**: Componente de abas do tkinter
- **Loop for**: Cria as 3 abas dinamicamente

---

## 🏭 Criação de Linhas

### Linha 53-85: _criar_area_mes()

```python
def _criar_area_mes(self, parent, nome_mes_atual):
    # 1. Cabeçalho da tabela
    header_bg = "#34495e"
    h_frame = tk.Frame(parent, bg=header_bg, ...)
    
    titles = [("Empresa / Contrato", 27), ("Molécula", 13), ...]
    for txt, w in titles:
        tk.Label(h_frame, text=txt, width=w, ...).pack(side="left")
    
    # 2. Área de scroll
    canvas = tk.Canvas(parent, ...)
    scroll = ttk.Scrollbar(parent, ...)
    scroll_frame = tk.Frame(canvas, ...)
    
    # 3. Gerar linhas para cada empresa padrão
    lista_entries_mes = []
    for emp in self.empresas_padrao:
        entry_dict = self._adicionar_linha_tabela(scroll_frame, emp, lista_entries_mes)
        lista_entries_mes.append(entry_dict)
    
    # 4. Botão "Adicionar Nova Empresa"
    # ...
    
    return lista_entries_mes  # Retorna a lista de linhas
```

**O que retorna:**

Uma **lista de dicionários**, onde cada dicionário é uma linha:

```python
[
    {'nome': Entry, 'mol': Entry, 'trans': Entry, ...},
    {'nome': Entry, 'mol': Entry, 'trans': Entry, ...},
    ...
]
```

---

## 📝 Linha Individual

### Linha 87-136: _adicionar_linha_tabela()

Esta é a função **MAIS IMPORTANTE** - ela cria UMA linha da tabela.

```python
def _adicionar_linha_tabela(self, parent, nome, lista_referencia):
    idx = len(lista_referencia)
    bg_color = "#ffffff" if idx % 2 == 0 else "#f8f9fa"  # Linhas alternadas
    
    row = tk.Frame(parent, bg=bg_color, pady=8, padx=15)
    row.pack(fill="x", expand=True)
```

**1. Criando os campos de entrada:**

```python
    # Campo NOME
    e_nome = tk.Entry(row, width=29, font=("Segoe UI", 10), ...)
    e_nome.insert(0, nome)  # Coloca o nome padrão
    e_nome.pack(side="left", padx=3, ipady=4)
    
    # Campo MOLÉCULA
    e_mol = tk.Entry(row, width=14, justify="center", ...)
    e_mol.pack(side="left", padx=3, ipady=4)
    
    # ... mesma coisa para Transporte, Logística, Volume
```

**2. Campo calculado (Preço Final):**

```python
    # Label (não é Entry, é só para mostrar)
    lbl_soma = tk.Label(row, text="0.0000", width=17, 
                       bg="#e3f2fd", fg="#1976d2", ...)
    lbl_soma.pack(side="left", ...)
```

**3. Botões de ação:**

```python
    # Botão COPIAR (roxo)
    btn_copiar = tk.Button(row, text="📋", 
                          command=lambda: self._copiar_linha_para_outro_mes(dados),
                          bg="#9b59b6", ...)
    
    # Botão REMOVER (vermelho)
    btn_remove = tk.Button(row, text="🗑️", 
                          command=lambda: self._remover_linha(row, dados, lista_referencia),
                          bg="#e74c3c", ...)
```

**4. Guardando tudo num dicionário:**

```python
    dados = {
        'nome': e_nome,      # Referência ao Entry
        'mol': e_mol,        # Referência ao Entry
        'trans': e_trans,    # Referência ao Entry
        'log': e_log,        # Referência ao Entry
        'lbl_soma': lbl_soma,# Referência ao Label
        'vol': e_vol,        # Referência ao Entry
        'row': row,          # Referência ao Frame da linha
        'btn_copiar': btn_copiar,
        'btn_remove': btn_remove
    }
```

**5. Atualização em tempo real:**

```python
    for e in [e_mol, e_trans, e_log]:
        e.bind("<KeyRelease>", lambda event, d=dados: self._update_row_total(d))
```

**O que isso faz:**
- Quando você **solta uma tecla** em qualquer campo (Molécula, Transporte ou Logística)
- Chama `_update_row_total(dados)`
- Que recalcula e atualiza o **Preço Final**

---

## ⚡ Atualização em Tempo Real

### Linha 138-140: _update_row_total()

```python
def _update_row_total(self, d):
    total = self._get_val(d['mol']) + self._get_val(d['trans']) + self._get_val(d['log'])
    d['lbl_soma'].config(text=f"{total:.4f}")
```

**Passo a passo:**

1. `d['mol']`: Pega o Entry widget da molécula
2. `self._get_val(d['mol'])`: Converte o texto do Entry para número float
3. Soma os 3 valores
4. `d['lbl_soma'].config(text=...)`: Atualiza o texto do Label

### Linha 142-147: _get_val()

```python
def _get_val(self, entry):
    try:
        v = entry.get().replace(',', '.')  # Aceita vírgula E ponto
        return float(v) if v else 0.0
    except: 
        return 0.0
```

**Tratamento de erros:**
- Se o campo estiver vazio → retorna 0.0
- Se o usuário digitou "abc" → retorna 0.0
- Aceita tanto `10,50` quanto `10.50`

---

## ➕ Adicionar Nova Linha

### Linha 149-154: _adicionar_nova_linha()

```python
def _adicionar_nova_linha(self, parent_frame, lista_referencia):
    # Cria uma nova linha
    entry_dict = self._adicionar_linha_tabela(parent_frame, "Nova Empresa", lista_referencia)
    
    # Adiciona na lista
    lista_referencia.append(entry_dict)
    
    # Coloca o cursor no campo de nome
    entry_dict['nome'].focus_set()
    entry_dict['nome'].select_range(0, tk.END)  # Seleciona todo o texto
```

**Por que isso funciona:**
- `lista_referencia` é uma **referência** (não cópia)
- Quando você faz `.append()`, está modificando a lista original
- A lista original está dentro de `self.dados_por_mes`

---

## 🗑️ Remover Linha

### Linha 156-168: _remover_linha()

```python
def _remover_linha(self, row_frame, dados, lista_referencia):
    empresa = dados['nome'].get()
    
    # Janela de confirmação
    confirmacao = messagebox.askyesno(
        "Confirmar Remoção",
        f"Tem certeza que deseja remover a empresa:\n'{empresa}'?"
    )
    
    if confirmacao:
        row_frame.destroy()  # Remove da TELA
        if dados in lista_referencia:
            lista_referencia.remove(dados)  # Remove da LISTA
```

**CRÍTICO:**

Você precisa fazer **os dois**:
1. `row_frame.destroy()`: Remove visualmente (some da tela)
2. `lista_referencia.remove(dados)`: Remove da lista Python

Se esquecer o passo 2, a linha vai sumir da tela mas ainda vai entrar no cálculo do PMPV!

---

## 📋 Copiar Linha

### Linha 170-205: _copiar_linha_para_outro_mes()

```python
def _copiar_linha_para_outro_mes(self, dados_origem):
    # 1. Descobre em qual mês estamos
    mes_atual = None
    for nome_mes, linhas in self.dados_por_mes.items():
        if dados_origem in linhas:
            mes_atual = nome_mes
            break
```

**Como funciona:**
- Percorre `self.dados_por_mes` (que é um dicionário)
- `.items()` retorna pares `(chave, valor)` = `(nome_mes, linhas)`
- `if dados_origem in linhas`: Verifica se o dicionário `dados_origem` está nessa lista

**2. Criar janela popup:**

```python
    janela = tk.Toplevel(self.root)
    janela.title("Copiar Linha")
    janela.geometry("350x250")
    
    # Tornar MODAL (bloqueia a janela principal)
    janela.transient(self.root)
    janela.grab_set()
```

**Modal** significa que você **não consegue** clicar na janela principal enquanto o popup está aberto.

**3. Botões para cada mês:**

```python
    for nome_mes in ["Mês 1", "Mês 2", "Mês 3"]:
        if nome_mes != mes_atual:  # Não mostra o mês atual
            btn = tk.Button(janela, text=f"➡️ {nome_mes}", 
                           command=lambda m=nome_mes: self._executar_copia_linha(...),
                           ...)
```

**Lambda com parâmetro padrão:**

```python
lambda m=nome_mes: self._executar_copia_linha(dados_origem, m, janela)
```

Isso é necessário porque, sem `m=nome_mes`, todas as lambdas usariam o **último valor** de `nome_mes` do loop.

---

## 🔄 Executar Cópia

### Linha 207-269: _executar_copia_linha()

```python
def _executar_copia_linha(self, dados_origem, mes_destino, janela_selecao):
    empresa = dados_origem['nome'].get()
    janela_selecao.destroy()  # Fecha o popup
    
    dados_destino = self.dados_por_mes[mes_destino]
```

**1. Procurar se já existe:**

```python
    linha_existente = None
    for d in dados_destino:
        if d['nome'].get() == empresa:
            linha_existente = d
            break
```

**2. Se existe, perguntar:**

```python
    if linha_existente:
        confirmacao = messagebox.askyesno(...)
        if not confirmacao:
            return
        destino = linha_existente
```

**3. Se não existe, procurar linha vazia:**

```python
    else:
        destino = None
        for d in dados_destino:
            if not d['nome'].get() or d['nome'].get().startswith("Fornecedor"):
                destino = d
                break
```

**4. Copiar os valores:**

```python
    destino['nome'].delete(0, tk.END)       # Limpa
    destino['nome'].insert(0, dados_origem['nome'].get())  # Insere
    
    destino['mol'].delete(0, tk.END)
    destino['mol'].insert(0, dados_origem['mol'].get())
    
    # ... mesma coisa para os outros campos
```

**5. Atualizar Preço Final:**

```python
    self._update_row_total(destino)
```

---

## 🧮 Cálculo do PMPV

### Linha 271-308: calcular_trimestre()

```python
def calcular_trimestre(self):
    custo_total_trimestre = 0.0
    volume_total_trimestre = 0.0
    
    # Percorrer os 3 meses
    for mes, linhas in self.dados_por_mes.items():
        for l in linhas:
            vol = self._get_val(l['vol'])
            if vol > 0:  # Só considera se tiver volume
                preco = self._get_val(l['mol']) + self._get_val(l['trans']) + self._get_val(l['log'])
                custo_total_trimestre += (preco * vol)
                volume_total_trimestre += vol
```

**Fórmula:**

```
custo_total_trimestre = ∑ (preço_unitário × volume)
volume_total_trimestre = ∑ volume

PMPV = custo_total_trimestre / volume_total_trimestre
```

**Por que funciona:**

```
Mês 1:
  Fornecedor A: 10.50 × 100 = 1050
  Fornecedor B: 11.20 × 80 = 896
  
Mês 2:
  Fornecedor A: 10.50 × 100 = 1050
  Fornecedor C: 9.80 × 50 = 490
  
Custo Total = 1050 + 896 + 1050 + 490 = 3486
Volume Total = 100 + 80 + 100 + 50 = 330

PMPV = 3486 / 330 = 10,56
```

---

## 🔄 Fluxo de Dados

### Diagrama de Fluxo:

```
1. INICIALIZAÇÃO
   ↓
   __init__() cria self.dados_por_mes = {}
   ↓
   _setup_ui() cria as 3 abas
   ↓
   Para cada aba, chama _criar_area_mes()
   ↓
   _criar_area_mes() cria 6 linhas padrão
   ↓
   Cada linha criada com _adicionar_linha_tabela()
   ↓
   Retorna lista de dicionários
   ↓
   Guarda em self.dados_por_mes["Mês X"]

2. USUÁRIO DIGITA
   ↓
   Entry widget dispara evento "<KeyRelease>"
   ↓
   Chama _update_row_total()
   ↓
   Atualiza lbl_soma (Preço Final)

3. USUÁRIO CLICA "CALCULAR"
   ↓
   calcular_trimestre()
   ↓
   Percorre self.dados_por_mes
   ↓
   Para cada linha, pega valores com _get_val()
   ↓
   Faz a conta: custo_total / volume_total
   ↓
   Mostra resultado no Label + MessageBox

4. USUÁRIO CLICA "COPIAR" (📋)
   ↓
   _copiar_linha_para_outro_mes()
   ↓
   Abre popup com opções de mês
   ↓
   Usuário escolhe mês destino
   ↓
   _executar_copia_linha()
   ↓
   Copia valores de um Entry para outro
   ↓
   Atualiza Preço Final
```

---

## 🧠 Conceitos Importantes

### 1. **Widgets são Objetos**

```python
e_nome = tk.Entry(...)  # Cria objeto Entry
e_nome.get()            # Método para pegar texto
e_nome.insert(0, "texto")  # Método para inserir
e_nome.delete(0, tk.END)   # Método para deletar
```

### 2. **Referências vs Cópias**

```python
lista_original = [1, 2, 3]

# REFERÊNCIA (aponta para o mesmo lugar)
lista_ref = lista_original
lista_ref.append(4)
print(lista_original)  # [1, 2, 3, 4]

# CÓPIA (cria nova lista)
lista_copia = lista_original.copy()
lista_copia.append(5)
print(lista_original)  # [1, 2, 3, 4]
```

No nosso código, usamos **referências**:

```python
def _adicionar_nova_linha(self, parent_frame, lista_referencia):
    lista_referencia.append(entry_dict)  # Modifica a lista original
```

### 3. **Lambda com Captura de Variável**

**ERRADO:**

```python
for i in range(3):
    btn = tk.Button(text=f"Botão {i}", 
                   command=lambda: print(i))  # ❌ Sempre imprime 2
```

**CERTO:**

```python
for i in range(3):
    btn = tk.Button(text=f"Botão {i}", 
                   command=lambda x=i: print(x))  # ✅ Captura o valor atual
```

### 4. **Bind de Eventos**

```python
entry.bind("<KeyRelease>", funcao)  # Quando solta uma tecla
entry.bind("<Return>", funcao)      # Quando aperta Enter
entry.bind("<FocusOut>", funcao)    # Quando sai do campo
```

### 5. **Pack, Grid, Place**

Três formas de posicionar widgets:

- **pack()**: Empilha verticalmente ou horizontalmente (usamos esse)
- **grid()**: Organiza em grade (linhas × colunas)
- **place()**: Posicionamento absoluto (x, y)

---

## 🎓 Exercícios para Praticar

### Nível Iniciante:

1. **Mudar cores:**
   - Linha 123: Mude a cor do botão copiar de `#9b59b6` para `#e67e22` (laranja)
   - Linha 108: Mude a cor do Preço Final de `#e3f2fd` para `#ffebee`

2. **Mudar textos:**
   - Linha 11: Adicione mais um fornecedor na lista `empresas_padrao`
   - Linha 26: Mude o subtítulo do cabeçalho

### Nível Intermediário:

3. **Adicionar validação:**
   - Na função `_get_val()`, faça ela não aceitar números negativos

4. **Adicionar campo:**
   - Adicione uma coluna "Desconto (%)" na tabela
   - Calcule: `Preço Final = (Molécula + Transporte + Logística) × (1 - Desconto/100)`

### Nível Avançado:

5. **Exportar para Excel:**
   - Crie um botão que salva os dados em CSV
   - Use o módulo `csv` do Python

6. **Gráfico:**
   - Crie um botão que mostra um gráfico comparando os 3 meses
   - Use `matplotlib`

---

## 🔍 Debugging (Como Encontrar Erros)

### 1. **Print estratégico:**

```python
def _executar_copia_linha(self, dados_origem, mes_destino, janela_selecao):
    print(f"DEBUG: Copiando para {mes_destino}")
    empresa = dados_origem['nome'].get()
    print(f"DEBUG: Empresa = {empresa}")
    # ...
```

### 2. **Try-Except:**

```python
try:
    resultado = calcular_trimestre()
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()  # Mostra onde deu erro
```

### 3. **Verificar tipo:**

```python
print(type(self.dados_por_mes))  # <class 'dict'>
print(type(dados_origem))        # <class 'dict'>
```

---

## 📖 Próximos Passos

Agora que você entendeu como funciona:

1. **Experimente modificar** valores no código
2. **Quebre o código** de propósito para ver os erros
3. **Adicione funcionalidades** novas
4. **Otimize** partes que achar lentas

**Lembre-se:** A melhor forma de aprender é **fazendo**! 💪

---

**Dúvidas? Releia este guia ou teste o código linha por linha!** 🚀
