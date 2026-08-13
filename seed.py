from models import DatabaseManager

def seed_database():
    db = DatabaseManager()

    # Limpar dados existentes para evitar duplicados se rodar o seed várias vezes
    with db._get_connection() as conn:
        conn.execute("DELETE FROM matriculas")
        conn.execute("DELETE FROM materiais")
        conn.execute("DELETE FROM cursos")
        conn.execute("DELETE FROM usuarios")
        conn.commit()

    print("Limpando banco de dados...")

    # 1. Criar Usuários
    # Professor
    prof_id = db.create_usuario("Prof. Alan Turing", "professor@facultech.com", "123", "professor")

    # Alunos
    aluno1_id = db.create_usuario("João Silva", "joao@aluno.com", "123", "aluno")
    aluno2_id = db.create_usuario("Maria Souza", "maria@aluno.com", "123", "aluno")

    print("Usuários criados!")

    # 2. Criar Cursos
    c1_id = db.create_curso("Ciência da Computação", "Estudo dos fundamentos da computação e algoritmos.", "Tecnologia")
    c2_id = db.create_curso("Engenharia de Software", "Foco em ciclo de vida de software e arquitetura.", "Tecnologia")
    c3_id = db.create_curso("Análise de Dados", "Transformando dados em insights valiosos.", "Inovação")
    c4_id = db.create_curso("Segurança da Informação", "Proteção de dados e sistemas contra ataques.", "Segurança")

    print("Cursos criados!")

    # 3. Criar Materiais
    db.create_material("Introdução a Algoritmos", "PDF com a explicação de complexidade O(n).", c1_id)
    db.create_material("Estruturas de Dados", "Vídeo aula sobre Árvores e Grafos.", c1_id)

    db.create_material("UML e Diagramas", "Guia prático de Diagrama de Classes.", c2_id)
    db.create_material("Metodologias Ágeis", "Texto sobre Scrum e Kanban.", c2_id)

    db.create_material("Python para Dados", "Notebook Jupyter com Pandas e NumPy.", c3_id)

    db.create_material("Criptografia Simétrica", "Material sobre AES e DES.", c4_id)

    print("Materiais criados!")

    # 4. Matricular Alunos
    # João está em CC e Eng Software
    db.matricular_aluno(aluno1_id, c1_id)
    db.matricular_aluno(aluno1_id, c2_id)

    # Maria está em Análise de Dados e Segurança
    db.matricular_aluno(aluno2_id, c3_id)
    db.matricular_aluno(aluno2_id, c4_id)

    print("Matrículas realizadas!")
    print("\n--- Banco de dados populado com sucesso! ---")
    print("Login Aluno 1: joao@aluno.com / 123")
    print("Login Aluno 2: maria@aluno.com / 123")
    print("Login Professor: professor@facultech.com / 123")

if __name__ == "__main__":
    seed_database()
