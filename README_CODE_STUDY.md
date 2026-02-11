# 🎓 Branch CODE-STUDY

## 📌 Você está na branch de ESTUDO!

Esta branch foi criada especialmente para você **aprender, experimentar e modificar** o código sem preocupações! 🚀

---

## 🎯 Propósito desta Branch

| Main Branch | Code-Study Branch |
|-------------|-------------------|
| ✅ Código funcional e estável | 🧪 Área de experimentação |
| ✅ Sem bugs | ✅ Pode quebrar à vontade! |
| ✅ Versão oficial | 📚 Versão para aprender |
| ❌ Não modificar sem cuidado | ✅ Modifique sem medo! |

---

## 📚 Materiais Disponíveis

### 1. **GUIA_DE_ESTUDO.md** 📖
- Explicação **linha por linha** do código
- Diagramas e fluxogramas
- Conceitos importantes (Widgets, Lambda, Bind, etc.)
- Seção de debugging

**Como usar:** Leia junto com o `main.py` aberto lado a lado.

---

### 2. **EXERCICIOS_PRATICOS.md** 🎯
- **15+ exercícios práticos** divididos por níveis:
  - 🟢 Nível 1: Iniciante (mudar cores, textos)
  - 🟡 Nível 2: Intermediário (validações, nova coluna)
  - 🔴 Nível 3: Avançado (exportar CSV, gráficos)
- Experimentos guiados
- Desafio final

**Como usar:** Escolha um exercício e tente implementar!

---

### 3. **TUTORIAL_FUNCOES.md** 🔧
- Tutorial técnico detalhado
- Foco em funções específicas
- Exemplos práticos

---

### 4. **README.md** 📄
- Documentação oficial do projeto
- Como usar o programa

---

## 🚀 Como Começar a Estudar

### Passo 1: Certifique-se que está na branch correta

```bash
git branch
# Deve mostrar: * code-study
```

### Passo 2: Abra os arquivos

1. `main.py` (código principal)
2. `GUIA_DE_ESTUDO.md` (explicações)
3. `EXERCICIOS_PRATICOS.md` (exercícios)

### Passo 3: Escolha um caminho

**Caminho A - Leitura:**
1. Leia o `GUIA_DE_ESTUDO.md` do início ao fim
2. Vá seguindo no `main.py` para ver o código
3. Teste modificações pequenas

**Caminho B - Prática:**
1. Abra `EXERCICIOS_PRATICOS.md`
2. Comece pelo Exercício 1.1
3. Implemente cada exercício
4. Teste cada um

**Caminho C - Exploração:**
1. Abra `main.py`
2. Escolha uma função aleatória
3. Leia a explicação no guia
4. Tente modificar algo

---

## ⚙️ Comandos Git Úteis

### Ver em qual branch você está
```bash
git branch
```

### Ver suas modificações
```bash
git status
git diff
```

### Salvar suas modificações (commit)
```bash
git add .
git commit -m "minha modificação de estudo"
```

### Voltar para a branch principal
```bash
git checkout main
```

### Voltar para a branch de estudo
```bash
git checkout code-study
```

### Ver histórico de commits
```bash
git log --oneline
```

### Desfazer modificações (CUIDADO!)
```bash
git restore main.py  # Volta ao último commit
```

---

## 🧪 Experimentos Sugeridos

### 1. **Modificação Visual** (Fácil)
- Mude todas as cores para um esquema diferente
- Troque os emojis dos botões
- Mude fontes e tamanhos

### 2. **Nova Funcionalidade** (Médio)
- Adicione uma coluna "Observações" (texto livre)
- Crie um botão "Duplicar Linha"
- Adicione um contador de linhas preenchidas

### 3. **Otimização** (Difícil)
- Melhore a performance do cálculo
- Adicione cache para evitar recalcular
- Implemente undo/redo

---

## 💡 Dicas de Estudo

### ✅ FAÇA:
- Leia o código devagar
- Teste cada modificação
- Use `print()` para debugar
- Quebre o código de propósito
- Anote suas dúvidas

### ❌ NÃO FAÇA:
- Tentar entender tudo de uma vez
- Copiar código sem entender
- Desistir no primeiro erro
- Pular exercícios difíceis

---

## 🎯 Checklist de Progresso

Marque o que você já completou:

### Semana 1: Fundamentos
- [ ] Li o README completo
- [ ] Li o GUIA_DE_ESTUDO até a seção "Sistema de Abas"
- [ ] Fiz o Exercício 1.1 (mudar cores)
- [ ] Fiz o Exercício 1.2 (adicionar fornecedor)
- [ ] Fiz o Exercício 1.3 (mudar título)
- [ ] Entendi como funciona `_setup_ui()`

### Semana 2: Criação de Linhas
- [ ] Li a seção "Criação de Linhas" do guia
- [ ] Entendi `_criar_area_mes()`
- [ ] Entendi `_adicionar_linha_tabela()`
- [ ] Fiz o Exercício 2.1 (validação)
- [ ] Entendi como funciona o dicionário `dados`

### Semana 3: Botões e Ações
- [ ] Entendi `_update_row_total()`
- [ ] Entendi `_get_val()`
- [ ] Fiz o Exercício 2.2 (coluna desconto)
- [ ] Entendi `_adicionar_nova_linha()`
- [ ] Entendi `_remover_linha()`

### Semana 4: Cópia e Cálculo
- [ ] Entendi `_copiar_linha_para_outro_mes()`
- [ ] Entendi `_executar_copia_linha()`
- [ ] Entendi `calcular_trimestre()`
- [ ] Fiz o Exercício 3.1 (botão limpar)
- [ ] Entendi a fórmula do PMPV

### Semana 5: Avançado
- [ ] Fiz o Exercício 3.2 (exportar CSV)
- [ ] Fiz o Exercício 3.3 (gráfico)
- [ ] Completei o Desafio Final (favoritos)
- [ ] Criei uma funcionalidade própria

---

## 📊 Estrutura de Arquivos

```
code-study/
├── main.py                      # ← Código principal (modifique aqui!)
├── README.md                    # Documentação oficial
├── README_CODE_STUDY.md         # ← Este arquivo
├── GUIA_DE_ESTUDO.md           # Explicações detalhadas
├── EXERCICIOS_PRATICOS.md      # Exercícios para fazer
├── TUTORIAL_FUNCOES.md         # Tutorial técnico
└── requirements.txt            # Dependências
```

---

## 🆘 Problemas Comuns

### "Quebrei tudo e não sei voltar!"

**Solução:**
```bash
git restore main.py
```
Isso volta o arquivo para o último commit (estado original).

---

### "Quero ver minhas modificações lado a lado"

**Solução:**
```bash
git diff main.py
```
Mostra o que você mudou.

---

### "Como volto para a main sem perder minhas mudanças?"

**Solução:**
```bash
# Salvar modificações
git add .
git commit -m "salvando estudos"

# Voltar para main
git checkout main

# Voltar para code-study
git checkout code-study
```

---

## 🎓 Próximos Passos

1. **Complete todos os exercícios** do `EXERCICIOS_PRATICOS.md`
2. **Leia todo o** `GUIA_DE_ESTUDO.md`
3. **Crie algo novo** - uma funcionalidade sua
4. **Compartilhe** o que aprendeu (documente!)

---

## 🏆 Meta Final

**Ao terminar esta branch de estudo, você deve ser capaz de:**

✅ Entender 100% do código do `main.py`  
✅ Modificar qualquer parte sem medo  
✅ Adicionar novas funcionalidades  
✅ Debugar erros sozinho  
✅ Explicar o código para outra pessoa  

---

## 🚀 Boa Sorte!

**Esta branch é SUA área de experimentação. Divirta-se aprendendo!** 🎉

---

**Última atualização:** Fevereiro 2026  
**Mantido por:** Você! 😊
