# 🎯 Exercícios Práticos - Branch code-study

Esta branch é dedicada ao **ESTUDO DO CÓDIGO**. Aqui você pode modificar, quebrar, testar e aprender sem medo! 🚀

---

## 🎓 Propósito desta Branch

- ✅ **Experimentar** modificações sem afetar o código principal
- ✅ **Fazer exercícios** práticos
- ✅ **Adicionar comentários** para entender melhor
- ✅ **Quebrar o código** de propósito para ver os erros
- ✅ **Testar ideias** novas

---

## 📝 Lista de Exercícios

### 🟢 Nível 1: Modificações Simples (Iniciante)

#### Exercício 1.1: Mudar Cores
**Arquivo:** `main.py`  
**Linha:** 123

**Tarefa:** Mude a cor do botão "Copiar" de roxo para laranja.

**Antes:**
```python
btn_copiar = tk.Button(row, text="📋", 
                       bg="#9b59b6",  # ← Roxo
                       ...)
```

**Depois:**
```python
btn_copiar = tk.Button(row, text="📋", 
                       bg="#e67e22",  # ← Laranja
                       ...)
```

**Como testar:** Rode `python main.py` e veja se o botão ficou laranja!

---

#### Exercício 1.2: Adicionar Fornecedor
**Arquivo:** `main.py`  
**Linha:** 11

**Tarefa:** Adicione "Fornecedor 7" na lista de empresas padrão.

**Antes:**
```python
self.empresas_padrao = ["Fornecedor 1", "Fornecedor 2", "Fornecedor 3", 
                        "Fornecedor 4", "Fornecedor 5", "Fornecedor 6"]
```

**Depois:**
```python
self.empresas_padrao = ["Fornecedor 1", "Fornecedor 2", "Fornecedor 3", 
                        "Fornecedor 4", "Fornecedor 5", "Fornecedor 6",
                        "Fornecedor 7"]  # ← NOVO
```

**Como testar:** Abra o programa e verifique se aparece uma 7ª linha!

---

#### Exercício 1.3: Mudar Texto do Título
**Arquivo:** `main.py`  
**Linha:** 23

**Tarefa:** Mude o título para incluir seu nome.

**Antes:**
```python
tk.Label(frame_top, text="Calculadora de Preço Médio Ponderado (PMPV)", ...)
```

**Depois:**
```python
tk.Label(frame_top, text="Calculadora PMPV - Feito por [SEU NOME]", ...)
```

---

### 🟡 Nível 2: Lógica e Cálculos (Intermediário)

#### Exercício 2.1: Adicionar Validação
**Arquivo:** `main.py`  
**Linha:** 142-147

**Tarefa:** Faça a função `_get_val()` não aceitar números negativos.

**Antes:**
```python
def _get_val(self, entry):
    try:
        v = entry.get().replace(',', '.')
        return float(v) if v else 0.0
    except: 
        return 0.0
```

**Depois:**
```python
def _get_val(self, entry):
    try:
        v = entry.get().replace(',', '.')
        valor = float(v) if v else 0.0
        # Validação: não aceita negativo
        if valor < 0:
            return 0.0
        return valor
    except: 
        return 0.0
```

**Como testar:** Digite `-10` em um campo. O Preço Final deve mostrar 0!

---

#### Exercício 2.2: Adicionar Coluna "Desconto"
**Arquivo:** `main.py`

**Tarefa:** Adicione uma coluna "Desconto (%)" entre Logística e Preço Final.

**Passos:**

1. **Linha 62:** Adicione na lista de títulos:
```python
titles = [("Empresa / Contrato", 27), ("Molécula", 13), ("Transporte", 13), 
          ("Logística", 13), ("Desconto (%)", 10),  # ← NOVO
          ("Preço Final", 16), ("Volume (m³/dia)", 17), ("Ações", 10)]
```

2. **Linha 106:** Crie o Entry do desconto:
```python
e_desc = tk.Entry(row, width=11, justify="center", font=("Segoe UI", 10), 
                  relief="solid", bd=1, highlightthickness=0)
e_desc.pack(side="left", padx=3, ipady=4)
```

3. **Linha 133:** Adicione no dicionário:
```python
dados = {'nome': e_nome, 'mol': e_mol, 'trans': e_trans, 'log': e_log,
         'desc': e_desc,  # ← NOVO
         'lbl_soma': lbl_soma, 'vol': e_vol, ...}
```

4. **Linha 138-140:** Modifique o cálculo:
```python
def _update_row_total(self, d):
    subtotal = self._get_val(d['mol']) + self._get_val(d['trans']) + self._get_val(d['log'])
    desconto = self._get_val(d['desc']) / 100  # Converte % para decimal
    total = subtotal * (1 - desconto)
    d['lbl_soma'].config(text=f"{total:.4f}")
```

**Como testar:** 
- Molécula: 10.00
- Transporte: 1.00
- Logística: 0.50
- Desconto: 10
- Preço Final deve ser: (10+1+0.5) × (1-0.10) = 10.35

---

#### Exercício 2.3: Arredondar para 2 Casas Decimais
**Arquivo:** `main.py`  
**Linha:** 140

**Tarefa:** O Preço Final mostra 4 casas decimais. Mude para 2.

**Antes:**
```python
d['lbl_soma'].config(text=f"{total:.4f}")
```

**Depois:**
```python
d['lbl_soma'].config(text=f"{total:.2f}")
```

---

### 🔴 Nível 3: Funcionalidades Novas (Avançado)

#### Exercício 3.1: Botão "Limpar Tudo"
**Arquivo:** `main.py`

**Tarefa:** Adicione um botão que limpa TODOS os campos de um mês.

**Onde adicionar:** No final de `_criar_area_mes()`, antes do `return`.

```python
def _limpar_mes(lista_entries):
    confirmacao = messagebox.askyesno(
        "Confirmar",
        "Deseja limpar TODOS os campos deste mês?"
    )
    if confirmacao:
        for linha in lista_entries:
            linha['mol'].delete(0, tk.END)
            linha['trans'].delete(0, tk.END)
            linha['log'].delete(0, tk.END)
            linha['vol'].delete(0, tk.END)
            linha['lbl_soma'].config(text="0.0000")

# Botão
btn_limpar = tk.Button(parent, text="🗑️ Limpar Tudo", 
                      command=lambda: _limpar_mes(lista_entries_mes),
                      bg="#e74c3c", fg="white", ...)
btn_limpar.pack(pady=5)
```

---

#### Exercício 3.2: Exportar para CSV
**Arquivo:** Crie `exportar.py` (novo arquivo)

**Tarefa:** Crie uma função que exporta os dados para um arquivo CSV.

```python
import csv

def exportar_para_csv(dados_por_mes, nome_arquivo="dados_pmpv.csv"):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        
        # Cabeçalho
        writer.writerow(['Mês', 'Empresa', 'Molécula', 'Transporte', 
                        'Logística', 'Preço Final', 'Volume'])
        
        # Dados
        for mes, linhas in dados_por_mes.items():
            for linha in linhas:
                nome = linha['nome'].get()
                mol = linha['mol'].get()
                trans = linha['trans'].get()
                log = linha['log'].get()
                vol = linha['vol'].get()
                preco_final = linha['lbl_soma'].cget('text')
                
                if vol:  # Só exporta se tiver volume
                    writer.writerow([mes, nome, mol, trans, log, preco_final, vol])
    
    print(f"Arquivo {nome_arquivo} criado com sucesso!")
```

**Como usar:** No `main.py`, adicione um botão que chama essa função.

---

#### Exercício 3.3: Gráfico de Barras
**Tarefa:** Crie um gráfico mostrando o PMPV de cada mês separadamente.

**Bibliotecas necessárias:**
```bash
pip install matplotlib
```

**Código:**
```python
import matplotlib.pyplot as plt

def mostrar_grafico(dados_por_mes):
    meses = []
    pmpvs = []
    
    for mes, linhas in dados_por_mes.items():
        custo = 0.0
        volume = 0.0
        
        for l in linhas:
            vol = float(l['vol'].get() or 0)
            if vol > 0:
                mol = float(l['mol'].get() or 0)
                trans = float(l['trans'].get() or 0)
                log = float(l['log'].get() or 0)
                preco = mol + trans + log
                custo += preco * vol
                volume += vol
        
        if volume > 0:
            pmpv = custo / volume
            meses.append(mes)
            pmpvs.append(pmpv)
    
    plt.bar(meses, pmpvs, color=['#3498db', '#9b59b6', '#e74c3c'])
    plt.xlabel('Mês')
    plt.ylabel('PMPV (R$/m³)')
    plt.title('PMPV por Mês')
    plt.show()
```

---

## 🧪 Experimentos para Fazer

### Experimento 1: Quebrar de Propósito

1. Comente a linha que adiciona a empresa na lista:
```python
# lista_referencia.append(entry_dict)  # ← Comentado
```

2. Rode o programa e clique em "Calcular"
3. **O que acontece?** A nova empresa não entra no cálculo!

---

### Experimento 2: Mudar a Fórmula

Mude o cálculo do PMPV para usar **média simples** em vez de ponderada:

**Antes:**
```python
pmpv = custo_total / volume_total
```

**Depois:**
```python
# Média simples (sem considerar volume)
precos = []
for l in linhas:
    preco = self._get_val(l['mol']) + self._get_val(l['trans']) + self._get_val(l['log'])
    if preco > 0:
        precos.append(preco)

pmpv = sum(precos) / len(precos) if precos else 0
```

**Compare os resultados!** Qual faz mais sentido?

---

### Experimento 3: Adicionar Limite Máximo

Adicione uma validação: Volume não pode ser maior que 1.000.000

```python
def _get_val(self, entry):
    try:
        v = entry.get().replace(',', '.')
        valor = float(v) if v else 0.0
        
        # Limite máximo
        if entry == self.algum_campo_volume and valor > 1000000:
            messagebox.showwarning("Limite", "Volume máximo: 1.000.000")
            return 0.0
        
        return valor
    except: 
        return 0.0
```

---

## 📊 Checklist de Aprendizado

Marque o que você já consegue fazer:

- [ ] Modificar cores de botões
- [ ] Adicionar novos fornecedores padrão
- [ ] Mudar textos da interface
- [ ] Entender como `_get_val()` funciona
- [ ] Adicionar validações simples
- [ ] Criar novos campos (Entry)
- [ ] Modificar a fórmula do PMPV
- [ ] Criar novas funções
- [ ] Adicionar novos botões
- [ ] Exportar dados para CSV
- [ ] Criar gráficos
- [ ] Debugar erros sozinho

---

## 🎯 Desafio Final

**Crie uma funcionalidade completa do zero:**

**Desafio:** Sistema de "Favoritos"
- Botão ⭐ em cada linha
- Ao clicar, salva os dados daquela empresa em um arquivo JSON
- Botão "Carregar Favorito" que preenche os campos automaticamente

**Arquivos a criar:**
- `favoritos.json` (armazena os dados)
- Funções: `salvar_favorito()`, `carregar_favorito()`, `listar_favoritos()`

---

## 💡 Dicas para Estudar

1. **Leia o código devagar** - Não tente entender tudo de uma vez
2. **Teste cada modificação** - Rode o programa após cada mudança
3. **Use prints** - Adicione `print()` para ver o que está acontecendo
4. **Quebre e conserte** - Aprenda errando!
5. **Compare com o original** - Use `git diff` para ver suas mudanças

---

## 🔄 Como Voltar para a Branch Principal

Quando terminar de estudar:

```bash
git checkout main
```

Suas modificações ficam salvas na branch `code-study`!

---

## 📚 Recursos Adicionais

- **Guia de Estudo:** `GUIA_DE_ESTUDO.md`
- **README:** `README.md`
- **Tutorial de Funções:** `TUTORIAL_FUNCOES.md`

---

**Boa sorte nos estudos! 🚀📚**
