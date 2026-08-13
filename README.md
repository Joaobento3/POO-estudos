# 🎓 Simulador de Faculdade de Tecnologia e Inovação

Este projeto é um ambiente simulado de uma faculdade, onde alunos podem visualizar seus cursos e materiais de estudo, e professores podem gerenciar a criação de cursos, materiais e a matrícula de alunos.

## 📋 Pré-requisitos

Para rodar este projeto, você precisará ter o **Python** instalado em sua máquina.
- Versão recomendada: **Python 3.8 ou superior**.

## 🛠️ Instalação

1. Clone ou baixe os arquivos do projeto para sua máquina.
2. Abra o terminal ou prompt de comando na pasta raiz do projeto.
3. Instale a dependência necessária (Flask) utilizando o comando abaixo:

```bash
pip install flask
```

## 🚀 Como Rodar o Servidor

Para iniciar o sistema, siga estes passos:

1. **(Opcional) Popular o Banco de Dados**: 
   Se você quiser começar com dados de teste (usuários, cursos e materiais já criados), execute o script de semente:
   ```bash
   python seed.py
   ```

2. **Iniciar o Servidor**:
   Execute o arquivo principal da aplicação:
   ```bash
   python app.py
   ```

3. **Acessar o Sistema**:
   Abra o seu navegador e acesse o seguinte endereço:
   👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📂 Estrutura do Projeto

Aqui está uma explicação simples de cada arquivo e pasta:

- `app.py`: É o "coração" do projeto. Aqui ficam as rotas (os endereços do site) e a lógica que decide o que acontece quando você clica em um botão ou acessa uma página.
- `models.py`: Responsável por toda a parte de dados. Ele cria o banco de dados (SQLite) e define como as informações de Usuários, Cursos e Materiais são organizadas.
- `seed.py`: Um script auxiliar usado apenas para preencher o banco de dados com informações iniciais, facilitando os testes.
- `static/`: Pasta onde ficam arquivos que não mudam, como arquivos de estilo (CSS) para deixar o site bonito.
- `templates/`: Pasta que contém os arquivos HTML. O Flask usa esses arquivos para montar as páginas que você vê no navegador.

## 🔑 Logins de Teste

Se você executou o `seed.py`, pode usar as seguintes contas para testar:

| Tipo | Email | Senha |
| :--- | :--- | :--- |
| **Aluno 1** | `joao@aluno.com` | `123` |
| **Aluno 2** | `maria@aluno.com` | `123` |
| **Professor** | `professor@facultech.com` | `123` |

---
*Projeto desenvolvido para fins de estudo de Programação Orientada a Objetos (POO).*
