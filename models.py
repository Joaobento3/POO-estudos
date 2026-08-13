import sqlite3

class Usuario:
    """Classe que representa um usuário do sistema (Aluno ou Professor)."""
    def __init__(self, id, nome, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo  # 'aluno' ou 'professor'

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.tipo})>"

class Curso:
    """Classe que representa um curso da faculdade."""
    def __init__(self, id, nome, descricao, area):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.area = area

    def __repr__(self):
        return f"<Curso {self.nome}>"

class Material:
    """Classe que representa um material de estudo ou atividade de um curso."""
    def __init__(self, id, titulo, conteudo, curso_id):
        self.id = id
        self.titulo = titulo
        self.conteudo = conteudo
        self.curso_id = curso_id

    def __repr__(self):
        return f"<Material {self.titulo}>"

class DatabaseManager:
    """
    Classe responsável por todas as interações com o banco de dados SQLite.
    Esta classe encapsula a lógica de SQL para que o restante do app use objetos.
    """
    def __init__(self, db_name="faculdade.db"):
        self.db_name = db_name
        self._create_tables()

    def _get_connection(self):
        """Retorna uma conexão com o banco de dados."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
        return conn

    def _create_tables(self):
        """Cria as tabelas iniciais caso elas não existam."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Tabela de Usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    tipo TEXT NOT NULL
                )
            ''')
            # Tabela de Cursos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cursos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    area TEXT
                )
            ''')
            # Tabela de Materiais
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS materiais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    conteudo TEXT,
                    curso_id INTEGER,
                    FOREIGN KEY (curso_id) REFERENCES cursos (id)
                )
            ''')
            # Tabela de Matrículas (Relaciona Alunos a Cursos)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matriculas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER,
                    curso_id INTEGER,
                    FOREIGN KEY (aluno_id) REFERENCES usuarios (id),
                    FOREIGN KEY (curso_id) REFERENCES cursos (id)
                )
            ''')
            conn.commit()

    # --- Métodos de Usuário ---
    def get_usuario_by_email(self, email):
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
            return Usuario(**dict(row)) if row else None

    def create_usuario(self, nome, email, senha, tipo):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                           (nome, email, senha, tipo))
            conn.commit()
            return cursor.lastrowid

    # --- Métodos de Curso ---
    def get_all_cursos(self):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM cursos").fetchall()
            return [Curso(**dict(row)) for row in rows]

    def get_curso_by_id(self, curso_id):
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM cursos WHERE id = ?", (curso_id,)).fetchone()
            return Curso(**dict(row)) if row else None

    def create_curso(self, nome, descricao, area):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cursos (nome, descricao, area) VALUES (?, ?, ?)",
                           (nome, descricao, area))
            conn.commit()
            return cursor.lastrowid

    # --- Métodos de Material ---
    def get_materiais_by_curso(self, curso_id):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM materiais WHERE curso_id = ?", (curso_id,)).fetchall()
            return [Material(**dict(row)) for row in rows]

    def create_material(self, titulo, conteudo, curso_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO materiais (titulo, conteudo, curso_id) VALUES (?, ?, ?)",
                           (titulo, conteudo, curso_id))
            conn.commit()
            return cursor.lastrowid

    # --- Métodos de Matrícula ---
    def matricular_aluno(self, aluno_id, curso_id):
        with self._get_connection() as conn:
            conn.execute("INSERT INTO matriculas (aluno_id, curso_id) VALUES (?, ?)",
                         (aluno_id, curso_id))
            conn.commit()

    def get_cursos_do_aluno(self, aluno_id):
        with self._get_connection() as conn:
            query = '''
                SELECT c.* FROM cursos c
                JOIN matriculas m ON c.id = m.curso_id
                WHERE m.aluno_id = ?
            '''
            rows = conn.execute(query, (aluno_id,)).fetchall()
            return [Curso(**dict(row)) for row in rows]
