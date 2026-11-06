# 💡 Painel e Rastreador de Finanças Pessoais

Aplicação web Full-Stack desenvolvida para auxiliar no gerenciamento e controle das finanças pessoais. O sistema permite registrar receitas e despesas, acompanhar saldos automaticamente, filtrar transações por período e visualizar graficamente a distribuição dos gastos por categoria.

A aplicação conta com uma API REST desenvolvida em Python com Flask, banco de dados SQLite para persistência das informações e uma interface dinâmica construída com HTML5, CSS3 e JavaScript.

## 🛠️ Tecnologias Utilizadas

**Back-end**
- Python 3
- Flask
- Flask-CORS

**Banco de Dados**
- SQLite3

**Front-end**
- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API

**Visualização de Dados**
- Chart.js (Gráficos de Rosca / Doughnut)

**Versionamento**
- Git
- GitHub

## 📌 Funcionalidades

- [x] **Gestão de transações:** Cadastro de receitas e despesas, incluindo valor, categoria e data.
- [x] **Cálculo automático de saldos:** Atualização dos indicadores de total de entradas, total de saídas e saldo atual.
- [x] **Dashboard gráfico:** Visualização dinâmica da distribuição de despesas por categoria utilizando Chart.js.
- [x] **Filtros por período:** Consulta de transações de acordo com o mês e o ano selecionados.
- [x] **Exportação de relatórios:** Geração de arquivos `.csv` codificados em `UTF-8-SIG`, permitindo abertura dos relatórios diretamente no Microsoft Excel.
- [x] **Exclusão de registros:** Remoção individual de transações com atualização do painel.

## 🔗 Endpoints da API REST

A aplicação disponibiliza os seguintes endpoints para comunicação entre o front-end e o back-end:

| Método HTTP | Rota | Descrição |
|---|---|---|
| `GET` | `/api/transacoes` | Lista as transações cadastradas, permitindo filtros por mês e ano. |
| `POST` | `/api/transacoes` | Registra uma nova transação. |
| `DELETE` | `/api/transacoes/<id>` | Remove uma transação específica pelo ID. |
| `GET` | `/api/resumo` | Retorna os totais de entradas, saídas, saldo e dados para os gráficos. |
| `GET` | `/api/exportar/csv` | Gera e disponibiliza o download do relatório de transações em CSV. |

**Exemplo de filtros por período:**

```text
/api/transacoes?mes=11&ano=2026
```

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Python 3.x
- Git
- Navegador web de sua preferência

### 1. Clonar o Repositório

```bash
git clone https://github.com/WSantiago2003/rastreador-financas.git
```

Acesse a pasta do projeto:

```bash
cd rastreador-financas
```

### 2. Criar o Ambiente Virtual

```bash
python -m venv venv
```

**Ativação no Windows (CMD):**

```bash
venv\Scripts\activate
```

**Ativação no Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Ativação no Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, execute:

```bash
pip install flask flask-cors
```

### 4. Executar o Servidor Back-end

Inicie a aplicação Flask:

```bash
python app.py
```

### 5. Executar o Front-end

Abra o arquivo `index.html` no navegador de sua preferência.

Com o servidor Flask em execução, a interface estará pronta para realizar as operações de gerenciamento financeiro e consultar os dados armazenados.

## 👨‍💻 Autor

Projeto desenvolvido como prática de desenvolvimento Full-Stack, aplicando conceitos de programação em Python, criação de APIs RESTful, integração entre front-end e back-end, persistência de dados e visualização gráfica de informações.