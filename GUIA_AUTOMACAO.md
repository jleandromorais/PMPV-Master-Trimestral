# 🤖 Guia de Automação - Banco de Dados e Excel

Este guia explica como usar o **Banco de Dados SQLite** e **Excel** para automatizar o trabalho com o PMPV.

---

## 📦 O que foi adicionado

### 1. **database.py** - Banco de Dados SQLite
Permite salvar e carregar dados entre sessões do programa.

### 2. **excel_handler.py** - Integração com Excel
Permite importar/exportar dados em formato Excel formatado.

---

## 🗄️ Banco de Dados

### Como funciona

O banco de dados SQLite armazena:
- ✅ Sessões (trimestres salvos)
- ✅ Dados de cada mês
- ✅ Resultados calculados
- ✅ Histórico de modificações

### Estrutura do Banco

```
pmpv_data.db
├── sessoes
│   ├── id
│   ├── nome
│   ├── data_criacao
│   ├── data_modificacao
│   └── observacoes
│
├── dados_mes
│   ├── id
│   ├── sessao_id
│   ├── mes (1, 2 ou 3)
│   ├── empresa
│   ├── molecula
│   ├── transporte
│   ├── logistica
│   └── volume
│
└── resultados
    ├── id
    ├── sessao_id
    ├── volume_total
    ├── pmpv_trimestral
    ├── custo_total
    └── data_calculo
```

---

## 💻 Exemplos de Uso - Banco de Dados

### Exemplo 1: Salvar uma Sessão

```python
from database import DatabasePMPV

# Conectar ao banco
db = DatabasePMPV("pmpv_data.db")

# Criar uma nova sessão
sessao_id = db.criar_sessao(
    nome="Trimestre Q1 2026",
    observacoes="Dados de janeiro a março"
)

print(f"Sessão criada com ID: {sessao_id}")
```

### Exemplo 2: Salvar Dados de um Mês

```python
# Dados do Mês 1
dados_mes1 = [
    {
        'empresa': 'Fornecedor 1',
        'molecula': 10.50,
        'transporte': 0.50,
        'logistica': 0.30,
        'volume': 100000
    },
    {
        'empresa': 'Fornecedor 2',
        'molecula': 11.20,
        'transporte': 0.45,
        'logistica': 0.25,
        'volume': 80000
    }
]

# Salvar no banco
db.salvar_dados_mes(sessao_id, mes=1, dados=dados_mes1)
print("Dados do Mês 1 salvos!")
```

### Exemplo 3: Carregar Dados Salvos

```python
# Carregar dados do Mês 1
dados_carregados = db.carregar_dados_mes(sessao_id, mes=1)

for linha in dados_carregados:
    print(f"Empresa: {linha['empresa']}")
    print(f"Molécula: {linha['molecula']}")
    print(f"Volume: {linha['volume']}")
    print("---")
```

### Exemplo 4: Listar Sessões Salvas

```python
# Ver todas as sessões
sessoes = db.listar_sessoes()

for sessao in sessoes:
    print(f"ID: {sessao['id']}")
    print(f"Nome: {sessao['nome']}")
    print(f"Data: {sessao['data_criacao']}")
    print(f"PMPV: {sessao['pmpv_trimestral']}")
    print("---")
```

### Exemplo 5: Salvar Resultado do Cálculo

```python
# Após calcular o PMPV
db.salvar_resultado(
    sessao_id=sessao_id,
    volume_total=280000,
    pmpv=11.41,
    custo_total=3196000
)
```

### Exemplo 6: Criar Backup

```python
from database import criar_backup

# Criar backup automático
arquivo_backup = criar_backup("pmpv_data.db")
print(f"Backup criado: {arquivo_backup}")
# Saída: Backup criado: pmpv_backup_20260210_153045.db
```

---

## 📊 Exemplos de Uso - Excel

### Exemplo 1: Exportar para Excel

```python
from excel_handler import ExcelHandlerPMPV

# Preparar dados
dados_por_mes = {
    'Mês 1': [
        {'empresa': 'Fornecedor 1', 'molecula': 10.50, 'transporte': 0.50, 
         'logistica': 0.30, 'volume': 100000},
        {'empresa': 'Fornecedor 2', 'molecula': 11.20, 'transporte': 0.45, 
         'logistica': 0.25, 'volume': 80000}
    ],
    'Mês 2': [...],
    'Mês 3': [...]
}

resultado = {
    'volume_total': 280000,
    'custo_total': 3196000,
    'pmpv': 11.41
}

# Exportar
arquivo = ExcelHandlerPMPV.exportar_trimestre(
    dados_por_mes, 
    resultado, 
    "Relatorio_Q1_2026.xlsx"
)

print(f"Excel criado: {arquivo}")
```

### Exemplo 2: Criar Template Vazio

```python
# Criar um template para preencher manualmente no Excel
template = ExcelHandlerPMPV.criar_template("Meu_Template.xlsx")

print(f"Template criado: {template}")
# Agora você pode abrir no Excel e preencher manualmente!
```

### Exemplo 3: Importar do Excel

```python
# Importar dados de um Excel preenchido
dados_importados = ExcelHandlerPMPV.importar_excel("Dados_Preenchidos.xlsx")

# Usar os dados importados
for mes, dados in dados_importados.items():
    print(f"\n{mes}:")
    for linha in dados:
        print(f"  {linha['empresa']}: R$ {linha['molecula']}")
```

---

## 🚀 Automação Completa - Fluxo de Trabalho

### Cenário 1: Trabalhar com Dados Recorrentes

```python
from database import DatabasePMPV
from excel_handler import ExcelHandlerPMPV

# 1. Carregar dados do mês anterior (já salvos)
db = DatabasePMPV()
sessao_anterior = 123  # ID de dezembro
dados_dez = db.carregar_dados_mes(sessao_anterior, mes=1)

# 2. Criar nova sessão para janeiro
nova_sessao = db.criar_sessao("Janeiro 2026")

# 3. Copiar e ajustar apenas o que mudou
for linha in dados_dez:
    # Ajusta apenas o volume (preços mantêm)
    linha['volume'] = linha['volume'] * 1.05  # +5%

# 4. Salvar
db.salvar_dados_mes(nova_sessao, mes=1, dados=dados_dez)

# 5. Exportar para Excel
dados_completos = {'Mês 1': dados_dez, 'Mês 2': [], 'Mês 3': []}
ExcelHandlerPMPV.exportar_trimestre(dados_completos, {}, "Jan_2026.xlsx")

db.fechar()
```

### Cenário 2: Receber Excel e Importar

```python
# 1. Fornecedor envia Excel com dados
dados_excel = ExcelHandlerPMPV.importar_excel("Dados_Fornecedor.xlsx")

# 2. Salvar no banco de dados
db = DatabasePMPV()
sessao_id = db.criar_sessao("Dados do Fornecedor - Q1")

for i, mes in enumerate(['Mês 1', 'Mês 2', 'Mês 3'], start=1):
    if mes in dados_excel:
        db.salvar_dados_mes(sessao_id, i, dados_excel[mes])

db.fechar()
print("Dados importados e salvos no banco!")
```

### Cenário 3: Histórico e Comparação

```python
db = DatabasePMPV()

# Carregar trimestre atual e anterior
atual = db.exportar_para_dict(sessao_id=150)
anterior = db.exportar_para_dict(sessao_id=149)

# Comparar PMPVs
pmpv_atual = atual['resultado']['pmpv_trimestral']
pmpv_anterior = anterior['resultado']['pmpv_trimestral']

variacao = ((pmpv_atual - pmpv_anterior) / pmpv_anterior) * 100

print(f"PMPV Anterior: R$ {pmpv_anterior:.4f}")
print(f"PMPV Atual: R$ {pmpv_atual:.4f}")
print(f"Variação: {variacao:+.2f}%")

db.fechar()
```

---

## 🔄 Integração com o main.py

Para integrar com a interface gráfica, você precisaria adicionar botões como:

### Botão "Salvar Sessão"

```python
def salvar_sessao_atual(self):
    """Salva os dados atuais no banco"""
    from database import DatabasePMPV
    
    db = DatabasePMPV()
    
    # Pedir nome para a sessão
    nome = tk.simpledialog.askstring("Salvar", "Nome da sessão:")
    if not nome:
        return
    
    # Criar sessão
    sessao_id = db.criar_sessao(nome)
    
    # Salvar dados dos 3 meses
    for i, (mes_nome, linhas) in enumerate(self.dados_por_mes.items(), start=1):
        dados_mes = []
        for linha in linhas:
            vol = self._get_val(linha['vol'])
            if vol > 0:  # Só salva se tiver volume
                dados_mes.append({
                    'empresa': linha['nome'].get(),
                    'molecula': self._get_val(linha['mol']),
                    'transporte': self._get_val(linha['trans']),
                    'logistica': self._get_val(linha['log']),
                    'volume': vol
                })
        db.salvar_dados_mes(sessao_id, i, dados_mes)
    
    db.fechar()
    messagebox.showinfo("Sucesso", f"Sessão '{nome}' salva!")
```

### Botão "Carregar Sessão"

```python
def carregar_sessao(self):
    """Carrega dados de uma sessão salva"""
    from database import DatabasePMPV
    
    db = DatabasePMPV()
    
    # Listar sessões
    sessoes = db.listar_sessoes()
    
    # Criar janela de seleção
    # ... (código para mostrar lista e selecionar)
    
    # Carregar dados
    for i in range(1, 4):
        mes_nome = f"Mês {i}"
        dados = db.carregar_dados_mes(sessao_id, i)
        
        # Preencher interface
        linhas_gui = self.dados_por_mes[mes_nome]
        for j, dado in enumerate(dados):
            if j < len(linhas_gui):
                linha = linhas_gui[j]
                linha['nome'].delete(0, tk.END)
                linha['nome'].insert(0, dado['empresa'])
                # ... preencher outros campos
    
    db.fechar()
    messagebox.showinfo("Sucesso", "Sessão carregada!")
```

### Botão "Exportar Excel"

```python
def exportar_para_excel(self):
    """Exporta dados atuais para Excel"""
    from excel_handler import ExcelHandlerPMPV
    from tkinter import filedialog
    
    # Pedir nome do arquivo
    nome_arquivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel", "*.xlsx")]
    )
    
    if not nome_arquivo:
        return
    
    # Coletar dados
    dados_por_mes = {}
    for mes_nome, linhas in self.dados_por_mes.items():
        dados_mes = []
        for linha in linhas:
            vol = self._get_val(linha['vol'])
            if vol > 0:
                dados_mes.append({
                    'empresa': linha['nome'].get(),
                    'molecula': self._get_val(linha['mol']),
                    'transporte': self._get_val(linha['trans']),
                    'logistica': self._get_val(linha['log']),
                    'volume': vol
                })
        dados_por_mes[mes_nome] = dados_mes
    
    # Resultado (se já calculou)
    resultado = {
        'volume_total': 0,  # Pegar do cálculo
        'pmpv': 0,          # Pegar do cálculo
        'custo_total': 0    # Pegar do cálculo
    }
    
    # Exportar
    ExcelHandlerPMPV.exportar_trimestre(dados_por_mes, resultado, nome_arquivo)
    messagebox.showinfo("Sucesso", f"Excel criado:\n{nome_arquivo}")
```

---

## 📋 Checklist de Instalação

Antes de usar, certifique-se:

- [ ] Python 3.8+ instalado
- [ ] Instalar dependências:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Testar módulo database:
  ```bash
  python database.py
  ```
- [ ] Testar módulo excel:
  ```bash
  python excel_handler.py
  ```

---

## 🐛 Troubleshooting

### Erro: "No module named 'openpyxl'"

**Solução:**
```bash
pip install openpyxl
```

### Erro: "database is locked"

**Solução:**
- Feche outras instâncias do programa
- Use `db.fechar()` sempre que terminar

### Excel não abre

**Solução:**
- Verifique se tem Excel/LibreOffice instalado
- Tente abrir manualmente o arquivo .xlsx

---

## 🎯 Próximas Automações Possíveis

1. **API REST** - Receber dados via HTTP
2. **Agendamento** - Executar cálculos automaticamente
3. **Email** - Enviar relatórios por email
4. **Dashboard Web** - Visualização online
5. **Integração ERP** - Conectar com sistema da empresa

---

## 📚 Referências

- **SQLite:** https://www.sqlite.org/docs.html
- **OpenPyXL:** https://openpyxl.readthedocs.io/
- **Python DB-API:** https://peps.python.org/pep-0249/

---

**Automação configurada! Agora é só usar! 🤖✨**
