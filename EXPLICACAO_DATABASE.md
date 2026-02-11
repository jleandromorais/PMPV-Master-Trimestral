# 🗄️ Explicação Completa - database.py

## 📚 Índice
1. [O que é um Banco de Dados](#o-que-é-um-banco-de-dados)
2. [Por que SQLite](#por-que-sqlite)
3. [Estrutura do Código](#estrutura-do-código)
4. [Linha por Linha](#linha-por-linha)
5. [Como Funciona na Prática](#como-funciona-na-prática)
6. [Exemplos Visuais](#exemplos-visuais)

---

## 🎯 O que é um Banco de Dados?

### Imagine uma Biblioteca:

```
📚 Biblioteca (Banco de Dados)
│
├── 📖 Prateleira "Sessões" (Tabela sessoes)
│   ├── Livro 1: "Trimestre Q1 2026"
│   ├── Livro 2: "Trimestre Q2 2026"
│   └── Livro 3: "Trimestre Q3 2026"
│
├── 📊 Prateleira "Dados dos Meses" (Tabela dados_mes)
│   ├── Páginas do Trimestre Q1
│   │   ├── Mês 1: Fornecedor A, preços, volumes...
│   │   ├── Mês 2: Fornecedor A, preços, volumes...
│   │   └── Mês 3: Fornecedor A, preços, volumes...
│   └── ...
│
└── 📈 Prateleira "Resultados" (Tabela resultados)
    ├── PMPV do Q1 2026
    ├── PMPV do Q2 2026
    └── ...
```

**Banco de Dados = Lugar organizado para guardar dados permanentemente**

---

## 💡 Por que SQLite?

### Vantagens do SQLite:

✅ **Não precisa de servidor** - Tudo em 1 arquivo (.db)  
✅ **Já vem com Python** - Não precisa instalar nada  
✅ **Rápido** - Perfeito para aplicações desktop  
✅ **Confiável** - Usado em milhões de apps  
✅ **Portátil** - Pode copiar o arquivo .db entre computadores  

### Alternativas (mais complexas):

- PostgreSQL - Precisa servidor
- MySQL - Precisa servidor
- MongoDB - Mais complexo
- Excel/CSV - Não é um banco de dados real

---

## 🏗️ Estrutura do Código

### Organização do `database.py`:

```python
database.py
│
├── Imports (linha 1-9)
│
├── Classe DatabasePMPV (linha 12-313)
│   │
│   ├── __init__() ...................... Inicializa conexão
│   ├── _conectar() ..................... Conecta ao arquivo .db
│   ├── _criar_tabelas() ................ Cria estrutura do banco
│   │
│   ├── criar_sessao() .................. Nova sessão
│   ├── salvar_dados_mes() .............. Salva dados de 1 mês
│   ├── carregar_dados_mes() ............ Carrega dados de 1 mês
│   │
│   ├── salvar_resultado() .............. Salva PMPV calculado
│   ├── listar_sessoes() ................ Lista tudo salvo
│   ├── deletar_sessao() ................ Apaga uma sessão
│   │
│   ├── exportar_para_dict() ............ Exporta para dicionário
│   ├── fechar() ........................ Fecha conexão
│   └── __del__() ....................... Destrutor automático
│
└── Funções auxiliares (linha 316+)
    └── criar_backup() .................. Faz backup do .db
```

---

## 📖 Linha por Linha - Parte 1: Inicialização

### Linhas 1-9: Imports

```python
import sqlite3      # Biblioteca de banco de dados (já vem com Python)
import json         # Para trabalhar com JSON (não usado ainda)
from datetime import datetime  # Para data/hora
from typing import Dict, List, Optional  # Type hints (dicas de tipo)
```

**Type hints** ajudam o editor a auto-completar e encontrar erros:
- `Dict` = dicionário
- `List` = lista
- `Optional` = pode ser None

---

### Linhas 18-27: O Construtor `__init__`

```python
def __init__(self, db_path: str = "pmpv_data.db"):
    """
    Inicializa a conexão com o banco de dados.
    
    Args:
        db_path: Caminho para o arquivo do banco de dados
    """
    self.db_path = db_path
    self.conn = None
    self.cursor = None
    self._conectar()
    self._criar_tabelas()
```

**O que acontece:**

1. `db_path = "pmpv_data.db"`: Nome padrão do arquivo
2. `self.db_path = db_path`: Guarda o caminho
3. `self.conn = None`: Vai guardar a conexão
4. `self.cursor = None`: Vai guardar o cursor (executor de comandos SQL)
5. `self._conectar()`: Conecta ao banco
6. `self._criar_tabelas()`: Cria as tabelas (se não existirem)

**Analogia:**
```
__init__ é como ABRIR a biblioteca:
1. Pega a chave (db_path)
2. Abre a porta (conn)
3. Pega a caneta para anotar (cursor)
4. Verifica se as prateleiras existem (_criar_tabelas)
```

---

### Linhas 29-35: Conectar `_conectar()`

```python
def _conectar(self):
    """Estabelece conexão com o banco de dados"""
    self.conn = sqlite3.connect(self.db_path)
    self.cursor = self.conn.cursor()
    # Permite acessar colunas por nome
    self.conn.row_factory = sqlite3.Row
```

**O que faz:**

1. `sqlite3.connect()`: Abre ou cria o arquivo .db
2. `.cursor()`: Cria um "ponteiro" para executar comandos SQL
3. `row_factory = sqlite3.Row`: Permite usar `row['nome']` em vez de `row[0]`

**Sem row_factory:**
```python
row = cursor.fetchone()
nome = row[0]      # Tem que lembrar que nome é coluna 0
id = row[1]        # Tem que lembrar que id é coluna 1
```

**Com row_factory:**
```python
row = cursor.fetchone()
nome = row['nome']  # Mais claro!
id = row['id']      # Mais claro!
```

---

## 📊 Linha por Linha - Parte 2: Criação de Tabelas

### Linhas 37-70: `_criar_tabelas()`

Essa função cria 3 tabelas no banco. Vamos ver cada uma:

#### **Tabela 1: sessoes**

```python
self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        observacoes TEXT
    )
""")
```

**Traduzindo:**

```
Crie uma TABELA chamada "sessoes" SE NÃO EXISTIR com as colunas:

┌────────────────────┬──────────┬─────────────────────────────┐
│ Coluna             │ Tipo     │ O que significa             │
├────────────────────┼──────────┼─────────────────────────────┤
│ id                 │ INTEGER  │ Número único (1, 2, 3...)  │
│                    │ PRIMARY  │ Chave principal (não repete)│
│                    │ AUTO..   │ Incrementa sozinho         │
│                    │          │                             │
│ nome               │ TEXT     │ Nome do trimestre          │
│                    │ NOT NULL │ Obrigatório (não pode vazio)│
│                    │          │                             │
│ data_criacao       │ TIMESTAMP│ Quando foi criado          │
│                    │ DEFAULT  │ Preenche automaticamente   │
│                    │          │                             │
│ data_modificacao   │ TIMESTAMP│ Última modificação         │
│                    │          │                             │
│ observacoes        │ TEXT     │ Comentários opcionais      │
└────────────────────┴──────────┴─────────────────────────────┘
```

**Exemplo de dados:**

| id | nome | data_criacao | data_modificacao | observacoes |
|----|------|--------------|------------------|-------------|
| 1 | Q1 2026 | 2026-01-15 10:30 | 2026-01-20 14:00 | Dados revisados |
| 2 | Q2 2026 | 2026-04-10 09:15 | 2026-04-10 09:15 | NULL |

---

#### **Tabela 2: dados_mes**

```python
self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados_mes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sessao_id INTEGER NOT NULL,
        mes INTEGER NOT NULL,  -- 1, 2 ou 3
        empresa TEXT NOT NULL,
        molecula REAL,
        transporte REAL,
        logistica REAL,
        volume REAL,
        FOREIGN KEY (sessao_id) REFERENCES sessoes (id) ON DELETE CASCADE
    )
""")
```

**Traduzindo:**

```
┌────────────┬──────────┬─────────────────────────────────────┐
│ Coluna     │ Tipo     │ O que significa                     │
├────────────┼──────────┼─────────────────────────────────────┤
│ id         │ INTEGER  │ Número único da linha              │
│ sessao_id  │ INTEGER  │ A qual sessão pertence (1, 2, 3...) │
│ mes        │ INTEGER  │ Qual mês (1, 2 ou 3)               │
│ empresa    │ TEXT     │ Nome do fornecedor                 │
│ molecula   │ REAL     │ Preço da molécula (float)          │
│ transporte │ REAL     │ Preço do transporte (float)        │
│ logistica  │ REAL     │ Preço da logística (float)         │
│ volume     │ REAL     │ Volume (float)                     │
└────────────┴──────────┴─────────────────────────────────────┘

FOREIGN KEY: Liga sessao_id com sessoes(id)
ON DELETE CASCADE: Se apagar a sessão, apaga esses dados também
```

**Exemplo de dados:**

| id | sessao_id | mes | empresa | molecula | transporte | logistica | volume |
|----|-----------|-----|---------|----------|------------|-----------|---------|
| 1 | 1 | 1 | Fornecedor 1 | 10.50 | 0.50 | 0.30 | 100000 |
| 2 | 1 | 1 | Fornecedor 2 | 11.20 | 0.45 | 0.25 | 80000 |
| 3 | 1 | 2 | Fornecedor 1 | 10.50 | 0.50 | 0.30 | 105000 |

---

#### **Tabela 3: resultados**

```python
self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sessao_id INTEGER NOT NULL,
        volume_total REAL,
        pmpv_trimestral REAL,
        custo_total REAL,
        data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sessao_id) REFERENCES sessoes (id) ON DELETE CASCADE
    )
""")
```

**Exemplo de dados:**

| id | sessao_id | volume_total | pmpv_trimestral | custo_total | data_calculo |
|----|-----------|--------------|-----------------|-------------|--------------|
| 1 | 1 | 280000 | 11.41 | 3196000 | 2026-01-20 15:30 |

---

## 💾 Linha por Linha - Parte 3: Salvando Dados

### Linhas 74-83: `criar_sessao()`

```python
def criar_sessao(self, nome: str, observacoes: str = "") -> int:
    """
    Cria uma nova sessão (trimestre).
    
    Args:
        nome: Nome da sessão (ex: "Trimestre Q1 2026")
        observacoes: Observações opcionais
        
    Returns:
        ID da sessão criada
    """
    self.cursor.execute(
        "INSERT INTO sessoes (nome, observacoes) VALUES (?, ?)",
        (nome, observacoes)
    )
    self.conn.commit()
    return self.cursor.lastrowid
```

**Passo a passo:**

1. **`INSERT INTO sessoes`**: Insere na tabela sessoes
2. **`(nome, observacoes)`**: Colunas que vamos preencher
3. **`VALUES (?, ?)`**: Placeholders (evita SQL injection)
4. **`(nome, observacoes)`**: Os valores reais
5. **`.commit()`**: CONFIRMA a operação (salva de verdade)
6. **`.lastrowid`**: Retorna o ID gerado automaticamente

**Por que usar `?` (placeholders)?**

❌ **ERRADO (inseguro):**
```python
nome = "Q1 2026'; DROP TABLE sessoes; --"  # Ataque SQL injection!
query = f"INSERT INTO sessoes (nome) VALUES ('{nome}')"
# Isso pode deletar sua tabela!
```

✅ **CERTO (seguro):**
```python
nome = "Q1 2026'; DROP TABLE sessoes; --"
cursor.execute("INSERT INTO sessoes (nome) VALUES (?)", (nome,))
# O "?" trata como texto literal, não como SQL
```

---

### Linhas 85-134: `salvar_dados_mes()`

```python
def salvar_dados_mes(self, sessao_id: int, mes: int, dados: List[Dict]) -> bool:
    """
    Salva os dados de um mês específico.
    
    Args:
        sessao_id: ID da sessão
        mes: Número do mês (1, 2 ou 3)
        dados: Lista de dicionários com os dados das empresas
        
    Returns:
        True se salvou com sucesso
    """
    try:
        # Remove dados anteriores deste mês
        self.cursor.execute(
            "DELETE FROM dados_mes WHERE sessao_id = ? AND mes = ?",
            (sessao_id, mes)
        )
        
        # Insere novos dados
        for linha in dados:
            self.cursor.execute("""
                INSERT INTO dados_mes 
                (sessao_id, mes, empresa, molecula, transporte, logistica, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                sessao_id,
                mes,
                linha.get('empresa', ''),
                linha.get('molecula', 0.0),
                linha.get('transporte', 0.0),
                linha.get('logistica', 0.0),
                linha.get('volume', 0.0)
            ))
        
        # Atualiza data de modificação
        self.cursor.execute(
            "UPDATE sessoes SET data_modificacao = CURRENT_TIMESTAMP WHERE id = ?",
            (sessao_id,)
        )
        
        self.conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        self.conn.rollback()  # Desfaz se deu erro
        return False
```

**Fluxo:**

```
1. DELETE os dados antigos do mês
   ↓
2. Para cada linha de dados:
   INSERT INTO dados_mes
   ↓
3. UPDATE data_modificacao da sessão
   ↓
4. COMMIT (salva tudo)
   ↓
5. Se der erro: ROLLBACK (desfaz tudo)
```

**Por que deletar antes?**

Para evitar duplicatas! Se você salvar Mês 1 duas vezes, sem o DELETE teria dados duplicados.

---

## 📂 Como Funciona na Prática

### Fluxo Completo:

```python
# 1. ABRIR O BANCO
db = DatabasePMPV("meu_banco.db")
# Cria arquivo meu_banco.db (se não existir)
# Cria tabelas (se não existirem)

# 2. CRIAR SESSÃO
sessao_id = db.criar_sessao("Trimestre Q1 2026", "Dados de janeiro a março")
# Retorna: 1 (primeiro ID)

# 3. PREPARAR DADOS
dados_mes1 = [
    {'empresa': 'Fornecedor 1', 'molecula': 10.50, 'transporte': 0.50, 'logistica': 0.30, 'volume': 100000},
    {'empresa': 'Fornecedor 2', 'molecula': 11.20, 'transporte': 0.45, 'logistica': 0.25, 'volume': 80000}
]

# 4. SALVAR
db.salvar_dados_mes(sessao_id=1, mes=1, dados=dados_mes1)
# Insere 2 linhas na tabela dados_mes

# 5. CARREGAR DE VOLTA
dados = db.carregar_dados_mes(sessao_id=1, mes=1)
print(dados)
# [{'empresa': 'Fornecedor 1', 'molecula': 10.50, ...}, ...]

# 6. FECHAR
db.fechar()
```

---

## 🎨 Exemplos Visuais

### Estado do Banco Após Operações:

#### **Após criar_sessao():**

**Tabela sessoes:**
```
┌────┬────────────┬─────────────────────┬─────────────────────┬─────────────┐
│ id │ nome       │ data_criacao        │ data_modificacao    │ observacoes │
├────┼────────────┼─────────────────────┼─────────────────────┼─────────────┤
│ 1  │ Q1 2026    │ 2026-02-11 10:00:00 │ 2026-02-11 10:00:00 │ NULL        │
└────┴────────────┴─────────────────────┴─────────────────────┴─────────────┘
```

#### **Após salvar_dados_mes(1, 1, dados):**

**Tabela dados_mes:**
```
┌────┬───────────┬─────┬──────────────┬──────────┬────────────┬───────────┬────────┐
│ id │ sessao_id │ mes │ empresa      │ molecula │ transporte │ logistica │ volume │
├────┼───────────┼─────┼──────────────┼──────────┼────────────┼───────────┼────────┤
│ 1  │ 1         │ 1   │ Fornecedor 1 │ 10.50    │ 0.50       │ 0.30      │ 100000 │
│ 2  │ 1         │ 1   │ Fornecedor 2 │ 11.20    │ 0.45       │ 0.25      │ 80000  │
└────┴───────────┴─────┴──────────────┴──────────┴────────────┴───────────┴────────┘
```

---

## 🤔 Perguntas Frequentes

### 1. **O que é COMMIT?**

Imagine um carrinho de compras:
- Você coloca itens no carrinho (INSERT, UPDATE, DELETE)
- Mas só paga no caixa (COMMIT)
- Se desistir, deixa o carrinho (ROLLBACK)

### 2. **Por que fechar a conexão?**

Como fechar um arquivo:
- Se não fechar, pode corromper dados
- Libera recursos do sistema
- Outras aplicações podem não conseguir acessar

### 3. **O que é CASCADE?**

```
Sessão 1 (Q1 2026)
├── Dados do Mês 1
├── Dados do Mês 2
└── Dados do Mês 3

Se você deletar a Sessão 1:
❌ SEM CASCADE: Dados dos meses ficam órfãos no banco
✅ COM CASCADE: Deleta tudo junto automaticamente
```

---

## 🎯 Exercícios para Praticar

### Exercício 1: Criar e Salvar

```python
db = DatabasePMPV("teste.db")

# Sua tarefa:
# 1. Crie uma sessão chamada "Meu Teste"
# 2. Salve dados do Mês 1 com 3 fornecedores
# 3. Carregue de volta e imprima

# Solução:
sessao_id = db.criar_sessao("Meu Teste")
dados = [
    {'empresa': 'A', 'molecula': 10, 'transporte': 1, 'logistica': 0.5, 'volume': 1000},
    {'empresa': 'B', 'molecula': 11, 'transporte': 1, 'logistica': 0.5, 'volume': 2000},
    {'empresa': 'C', 'molecula': 9, 'transporte': 1, 'logistica': 0.5, 'volume': 1500}
]
db.salvar_dados_mes(sessao_id, 1, dados)
resultado = db.carregar_dados_mes(sessao_id, 1)
print(resultado)

db.fechar()
```

### Exercício 2: Listar Tudo

```python
db = DatabasePMPV("teste.db")

# Liste todas as sessões salvas
sessoes = db.listar_sessoes()
for s in sessoes:
    print(f"ID: {s['id']}, Nome: {s['nome']}")

db.fechar()
```

---

**Agora você entende TODO o database.py! 🎉**

**Próximo passo:** Tente modificar e adicionar suas próprias funcionalidades!
