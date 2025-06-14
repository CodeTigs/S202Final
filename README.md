# 🧪 S202Final

**S202Final** é o projeto final da disciplina S202. Este repositório contém todo o código, documentação e recursos necessários para entender, executar e estender o projeto.
Foi criado por Tiago Rodrigues Plum Ferreira e Lucas Caetano Reis, visa fornecer uma ferramenta útil para análise de itens do jogo Counters Strike 2 no marketplace da plataforma Steam.
Utilizamos os bancos de dados Neo4j e MongoDB para gravar as informações fornecidas pela API da Steam.
Com esta ferramenta você pode ver o nome, preço, raridade e outras informações de diversos itens no mercado de CS2.
---

## 🛠️ Tecnologias utilizadas

- **Python 3.x** – principal linguagem  
- **Pandas**, **NumPy**, **scikit-learn** – manipulação e modelagem de dados   
- Outros: `requirements.txt`, etc.

---

## ⚙️ Instalação e execução

Siga os passos abaixo para rodar o projeto localmente:

```bash
# 1. Clone o repositório
git clone https://github.com/CodeTigs/S202Final.git
cd S202Final

# 2. Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o projeto
python main.py  # ou: flask run, streamlit run app.py, etc.
