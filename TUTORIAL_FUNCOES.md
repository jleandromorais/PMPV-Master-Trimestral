# 📘 Tutorial: Criando Funções de Adicionar e Remover (SEM INTERFACE)

## 🎯 O que você vai aprender

Vou te ensinar a criar **apenas as funções lógicas** para:
1. Adicionar uma nova empresa dinamicamente
2. Remover uma empresa da lista

**SEM mexer na parte visual** (sem criar botões, colunas, etc.)

---

## 📍 Onde você vai digitar

Abra o arquivo `main.py` e procure por esta linha (aproximadamente linha ~133):

```python
# ========================================
# AQUI VOCÊ VAI ADICIONAR AS FUNÇÕES
# Veja o arquivo TUTORIAL_FUNCOES.md
# ========================================
```

**É logo abaixo dessa marcação que você vai digitar!**

---

## 🔧 FUNÇÃO 1: Adicionar Nova Linha

### 📝 O que essa função faz?

Cria uma nova linha na tabela (com campos de Molécula, Transporte, etc.) programaticamente.

### 🖊️ O que você deve digitar:

```python
def _adicionar_nova_linha(self, parent_frame, lista_referencia):
    """
    Adiciona uma nova linha em branco para o usuário preencher.
    
    Parâmetros:
        parent_frame: O frame onde as linhas ficam (o scroll_frame)
        lista_referencia: A lista que guarda todos os dados das empresas
    """
    # Chama a função que já existe para criar uma linha
    entry_dict = self._adicionar_linha_tabela(parent_frame, "Nova Empresa", lista_referencia)
    
    # Adiciona o dicionário retornado na lista
    lista_referencia.append(entry_dict)
    
    # OPCIONAL: Dar foco automático no campo de nome
    entry_dict['nome'].focus_set()
    entry_dict['nome'].select_range(0, tk.END)
```

### 📚 Explicação linha por linha:

**Linha 1-2:** Definição da função
- `self`: Porque é uma função da classe
- `parent_frame`: Onde a linha vai aparecer (o frame de scroll)
- `lista_referencia`: A lista Python que guarda os dados

**Linha 8:** Chama `_adicionar_linha_tabela()`
- Essa função **já existe** no código (linha ~87)
- Ela cria todos os widgets (Entry, Label, etc.)
- Retorna um **dicionário** com referências dos campos

**Linha 11:** Adiciona na lista
- `lista_referencia.append(entry_dict)`: Guarda os dados
- Isso é IMPORTANTE para o cálculo funcionar

**Linhas 14-15:** Foco automático (OPCIONAL)
- `.focus_set()`: Coloca o cursor no campo
- `.select_range(0, tk.END)`: Seleciona todo o texto "Nova Empresa"

---

## 🗑️ FUNÇÃO 2: Remover Linha

### 📝 O que essa função faz?

Remove uma empresa específica da tabela e da lista interna.

### 🖊️ O que você deve digitar:

```python
def _remover_linha(self, row_frame, dados, lista_referencia):
    """
    Remove uma linha específica da interface e da lista interna.
    
    Parâmetros:
        row_frame: O Frame visual que contém a linha inteira
        dados: O dicionário com os widgets dessa linha
        lista_referencia: A lista que guarda todas as empresas
    """
    # Pega o nome da empresa para mostrar na confirmação
    empresa = dados['nome'].get()
    
    # Mostra uma janela de confirmação
    confirmacao = messagebox.askyesno(
        "Confirmar Remoção",
        f"Tem certeza que deseja remover a empresa:\n'{empresa}'?"
    )
    
    # Se o usuário clicar "Sim"
    if confirmacao:
        # Remove da interface visual
        row_frame.destroy()
        
        # Remove da lista Python
        if dados in lista_referencia:
            lista_referencia.remove(dados)
```

### 📚 Explicação linha por linha:

**Linha 10:** Pega o nome da empresa
- `dados['nome']`: É o Entry widget do nome
- `.get()`: Retorna o texto digitado

**Linhas 13-16:** Janela de confirmação
- `messagebox.askyesno()`: Mostra uma janela com "Sim" e "Não"
- Retorna `True` se clicar "Sim", `False` se clicar "Não"

**Linha 22:** Remove visualmente
- `row_frame.destroy()`: Deleta o Frame inteiro da tela
- Todos os widgets dentro somem automaticamente

**Linhas 25-26:** Remove dos dados internos
- `if dados in lista_referencia`: Verifica se existe
- `.remove(dados)`: Remove da lista Python
- **IMPORTANTE:** Se não remover daqui, a empresa ainda vai aparecer no cálculo!

---

## 🧪 Como Testar as Funções (SEM BOTÕES)

Você pode testar as funções **via código Python interativo** ou criando um botão temporário.

### Opção 1: Botão temporário na janela

No método `_criar_area_mes()`, adicione TEMPORARIAMENTE (só pra testar):

```python
# TESTE TEMPORÁRIO - Adicione antes do "return lista_entries_mes"
btn_teste = tk.Button(parent, text="TESTAR ADICIONAR", 
                     command=lambda: self._adicionar_nova_linha(scroll_frame, lista_entries_mes))
btn_teste.pack()
```

### Opção 2: Testar no console Python

Depois de rodar o programa, abra o terminal Python e chame:

```python
# Supondo que 'app' é sua instância
app._adicionar_nova_linha(scroll_frame, lista_entries_mes)
```

---

## 🔍 Entendendo a Estrutura de Dados

### O que é `lista_referencia`?

É uma **lista Python** que guarda dicionários. Cada dicionário representa uma linha:

```python
lista_referencia = [
    {
        'nome': <Entry widget>,
        'mol': <Entry widget>,
        'trans': <Entry widget>,
        'log': <Entry widget>,
        'lbl_soma': <Label widget>,
        'vol': <Entry widget>
    },
    {
        'nome': <Entry widget>,
        'mol': <Entry widget>,
        # ... etc
    },
    # ... mais empresas
]
```

### Por que isso importa?

Quando você faz o **cálculo do PMPV trimestral**, o código percorre essa lista:

```python
for l in linhas:
    vol = self._get_val(l['vol'])        # Pega o volume
    preco = self._get_val(l['mol']) + ... # Calcula o preço
    # ... faz a conta
```

Se você **não remover** da lista, a empresa deletada ainda entra no cálculo!

---

## 🎓 Conceitos Importantes

### 1. **Passagem de Referência**

Quando você faz:
```python
lista_referencia.append(entry_dict)
```

Você não está copiando os dados, está guardando uma **referência** (ponteiro) para o dicionário.

### 2. **Widgets são Objetos**

```python
dados['nome']  # Isso é um objeto Entry
dados['nome'].get()  # Isso retorna o texto (string)
```

### 3. **Destroy vs Remove**

```python
row_frame.destroy()  # Remove da TELA (visual)
lista_referencia.remove(dados)  # Remove da LISTA (lógica)
```

Você precisa fazer **os dois** para uma remoção completa!

---

## ✅ Checklist Final

Depois de digitar as funções, verifique:

- [ ] A função `_adicionar_nova_linha` está **indentada corretamente** (mesma indentação de `_get_val`)
- [ ] A função `_remover_linha` está **indentada corretamente**
- [ ] Você usou `self` como primeiro parâmetro
- [ ] Você importou `messagebox` no topo do arquivo (já deve estar lá)
- [ ] As aspas e parênteses estão fechados

---

## 🐛 Erros Comuns

### Erro: `IndentationError`

**Causa:** A função não está alinhada com as outras.

**Solução:** Use **4 espaços** (1 Tab) de indentação. Veja como `_get_val()` está indentado e faça igual.

### Erro: `NameError: name 'messagebox' is not defined`

**Causa:** Faltou importar o `messagebox`.

**Solução:** Linha 2 do arquivo deve ter:
```python
from tkinter import messagebox, ttk
```

### Erro: `AttributeError: 'dict' object has no attribute 'destroy'`

**Causa:** Você está tentando fazer `dados.destroy()` em vez de `row_frame.destroy()`.

**Solução:** Use o parâmetro `row_frame`, não o `dados`.

---

## 🚀 Próximo Passo (OPCIONAL)

Depois de criar as funções, se quiser **conectá-las a botões**, você vai:

1. Adicionar uma coluna "Ações" no cabeçalho
2. Criar um botão em cada linha que chama `_remover_linha()`
3. Criar um botão no final que chama `_adicionar_nova_linha()`

Mas isso é **outra aula**! Por enquanto, foque em entender a **lógica** das funções.

---

## 📞 Dúvidas?

- **"Por que preciso passar `lista_referencia`?"**
  - Porque Python não modifica listas automaticamente. Você precisa explicitamente adicionar/remover.

- **"Posso chamar qualquer nome de empresa?"**
  - Sim! Mude `"Nova Empresa"` para qualquer string.

- **"E se eu quiser adicionar 10 empresas de uma vez?"**
  - Use um loop:
    ```python
    for i in range(10):
        self._adicionar_nova_linha(parent_frame, lista_referencia)
    ```

---

**Agora é com você! Abre o `main.py`, encontra a marcação e digita as funções.** ✍️

**Quando terminar, me fala que eu te ajudo a testar!** 🎉
