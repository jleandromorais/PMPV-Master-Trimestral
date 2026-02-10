# Calculadora de PMPV - Sistema Trimestral 📊

Sistema profissional em Python com interface gráfica para cálculo de **PMPV (Preço Médio Ponderado de Venda)** com gestão trimestral e decomposição de preços em três parcelas: **Molécula**, **Transporte** e **Logística**.

Desenvolvido para facilitar o cálculo de contratos de gás natural com múltiplos fornecedores.

---

## 🎯 Funcionalidades Principais

### ✅ Interface com Abas (Mês 1, Mês 2, Mês 3)
- Gestão separada de cada mês do trimestre
- Navegação intuitiva entre períodos
- Dados independentes por mês

### ✅ Tríade de Preços
Para cada contrato/fornecedor, você informa:
- **Molécula**: Custo do produto gás em si (R$/m³)
- **Transporte**: Custo de transporte/TAG (R$/m³)
- **Logística**: Custos operacionais (R$/m³)
- **Preço Final**: Calculado automaticamente em tempo real

### ✅ Adicionar e Remover Empresas Dinamicamente
- **Botão ➕**: Adiciona novas empresas/contratos
- **Botão 🗑️**: Remove empresas com confirmação de segurança
- Sem limite de quantidade de empresas por mês

### ✅ Cálculo Automático em Tempo Real
- Ao digitar as três parcelas, o **Preço Final** atualiza instantaneamente
- Validação automática de valores
- Facilita conferência e evita erros

### ✅ Cálculo Trimestral Consolidado
- Soma todos os volumes e custos dos 3 meses
- Gera o **PMPV final do trimestre**
- Fórmula: `PMPV = (∑ custo_total) / (∑ volume_total)`
- Exibe relatório completo com volume total e custo estimado

### ✅ Design Profissional
- Cores organizadas por função:
  - **Azul**: Preço Final (calculado automaticamente)
  - **Amarelo**: Volume (campo obrigatório)
  - **Vermelho**: Botão remover
  - **Verde**: Botão calcular
- Cabeçalhos escuros e linhas alternadas para melhor leitura
- Scrollbar automática para muitos contratos

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Tkinter (já incluído na maioria das instalações Python)

### Execução

No diretório do projeto, execute:

```bash
python main.py
```

---

## 📖 Como Usar

### Passo 1: Preencher os Meses

1. A janela abrirá com 3 abas: **Mês 1**, **Mês 2**, **Mês 3**
2. Para cada mês:
   - Digite os valores de **Molécula** (ex: 10.50)
   - Digite os valores de **Transporte** (ex: 0.50)
   - Digite os valores de **Logística** (ex: 0.30)
   - O **Preço Final** aparecerá automaticamente em azul
   - Informe o **Volume (m³/dia)** na coluna amarela

### Passo 2: Adicionar/Remover Empresas

- **Para adicionar:** Clique no botão **➕ Adicionar Nova Empresa** (azul) no final da lista
- **Para remover:** Clique no botão **🗑️** (vermelho) ao lado da empresa desejada
- Aparecerá uma confirmação antes de remover

### Passo 3: Calcular o PMPV Trimestral

1. Após preencher os 3 meses, clique em **"⚡ GERAR FECHAMENTO TRIMESTRAL"** (botão verde)
2. O sistema calculará:
   - Volume total acumulado dos 3 meses
   - Custo total estimado
   - **PMPV final do trimestre**
3. Uma janela popup mostrará o relatório detalhado

---

## 📁 Estrutura do Projeto

```
Conta-Grafica-Automacao/
├── main.py                  # Aplicação principal (223 linhas)
├── README.md                # Este arquivo
├── requirements.txt         # Dependências
└── TUTORIAL_FUNCOES.md      # Tutorial técnico (opcional)
```

---

## ⚙️ Personalização

### 1. Adicionar Fornecedores Pré-Cadastrados

Edite a **linha 11** de `main.py`:

```python
self.empresas_padrao = ["Fornecedor 1", "Fornecedor 2", "Fornecedor 3", 
                        "Fornecedor 4", "Fornecedor 5", "Seu Fornecedor"]
```

### 2. Alterar Número de Meses (Trimestre → Semestre)

Por padrão são 3 meses (trimestre). Para mudar para **6 meses** (semestre), edite a **linha 33**:

```python
for i in range(1, 7):  # 6 meses
```

### 3. Personalizar a Fórmula do PMPV

Se houver regras regulatórias específicas (ANP/ANEEL), edite a função `calcular_trimestre()` na **linha 162**:

```python
def calcular_trimestre(self):
    # Seu código personalizado aqui
    preco = self._get_val(l['mol']) + self._get_val(l['trans']) + self._get_val(l['log'])
    # Adicione tributos, descontos, etc.
```

---

## 🧮 Fórmula do PMPV

Para cada contrato:

```
Preço Unitário = Molécula + Transporte + Logística
Custo Contrato = Preço Unitário × Volume
```

Para o trimestre:

```
PMPV Trimestral = (∑ Custos de todos os contratos nos 3 meses) / (∑ Volumes totais)
```

---

## 🐛 Resolução de Problemas

### Problema: "Tkinter não encontrado"

**Solução (Windows):**
```bash
# Reinstale Python marcando a opção "tcl/tk and IDLE"
```

**Solução (Linux):**
```bash
sudo apt-get install python3-tk
```

### Problema: Caracteres estranhos ou emojis não aparecem

**Solução:** Use uma fonte que suporte Unicode (Segoe UI, Arial, etc.). O código já usa Segoe UI por padrão.

### Problema: Botão "Calcular" não responde

**Solução:** Verifique se pelo menos 1 linha tem volume preenchido em qualquer um dos 3 meses.

---

## 📝 Exemplo de Uso

### Entrada (Mês 1):

| Fornecedor   | Molécula | Transporte | Logística | Preço Final | Volume  |
|--------------|----------|------------|-----------|-------------|---------|
| Fornecedor 1 | 10.50    | 0.50       | 0.30      | 11.30       | 100.000 |
| Fornecedor 2 | 11.20    | 0.45       | 0.25      | 11.90       | 80.000  |
| Fornecedor 3 | 9.80     | 0.00       | 1.65      | 11.45       | 50.000  |

### Saída (Trimestre):

```
✓ FECHAMENTO TRIMESTRAL
📊 Volume Total: 690.000 m³
💰 Custo Total: R$ 7.851.500,00
📈 PMPV: R$ 11,38 /m³
```

---

## 💡 Dicas de Uso

- **Use vírgula ou ponto:** O sistema aceita ambos (ex: `10,50` ou `10.50`)
- **Deixe campos vazios:** Se um fornecedor não opera em determinado mês, simplesmente não preencha o volume
- **Nomes descritivos:** Use nomes como "Fornecedor A - Contrato 123" para facilitar identificação
- **Conferência visual:** O Preço Final em azul ajuda a conferir se os valores estão corretos

---

## 📄 Licença

Este projeto foi desenvolvido para uso interno. Sem licença pública definida.

---

## 👤 Autor

Desenvolvido para auxiliar no cálculo de contratos de gás natural.

---

**Versão:** 1.0  
**Data:** Fevereiro 2026  
**Python:** 3.8+
