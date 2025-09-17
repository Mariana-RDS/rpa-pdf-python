# 🧾 RPA - Extração de Dados de Faturas em PDF

Este projeto faz parte de uma **série de tutoriais do canal [RPA Hour](https://www.youtube.com/watch?v=IjKOw02wOhg&t=237s)**.  
O objetivo é implementar um **robô de automação de processos (RPA)** em Python para realizar a extração automática de informações de faturas em formato **PDF**, armazenar os resultados em um **banco de dados MySQL** e gerar um **relatório em Excel**.

---

## 🚀 Funcionalidades
- Varredura automática de todos os arquivos **PDF** em um diretório.
- Extração de informações chave:
  - **Número da fatura**
  - **Data da fatura**
  - **Nome do arquivo**
- Registro dos resultados em:
  - **Banco de dados MySQL**
  - **Arquivo Excel (.xlsx)**, com status do processamento.
- Tratamento de erros:
  - Caso alguma informação não seja encontrada, o robô registra o erro no Excel e no banco de dados.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **Bibliotecas**:
  - [`pdfplumber`](https://github.com/jsvine/pdfplumber) → extração de texto de arquivos PDF
  - [`openpyxl`](https://openpyxl.readthedocs.io/) → geração de relatórios em Excel
  - [`mysql-connector-python`](https://dev.mysql.com/doc/connector-python/en/) → integração com MySQL
  - [`pathlib`](https://docs.python.org/3/library/pathlib.html) → manipulação de diretórios
  - [`re`](https://docs.python.org/3/library/re.html) → expressões regulares para localizar dados
- **MySQL** para persistência dos registros.

---

## ⚙️ Configuração e Uso

### 1. Clone o repositório
```bash
git clone https://github.com/Mariana-RDS/rpa-pdf-python.git
cd rpa-pdf-python
```

### 4. Configure o banco de dados MySQL
Crie o banco e a tabela:

```sql
CREATE DATABASE process_invoice;

USE process_invoice;

create table invoice_records(
	id INT PRIMARY KEY AUTO_INCREMENT,
    invoice_number varchar(255),
    invoice_date varchar(255),
    file_name varchar(255),
    status varchar(255),
    process_at timestamp default current_timestamp
);

```
