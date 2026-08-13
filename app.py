from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import DatabaseManager

app = Flask(__name__)
app.secret_key = "chave_secreta_para_estudo"  # Necessário para usar sessões no Flask

db = DatabaseManager()

@app.route('/')
def index():
    """Página inicial com formulário de login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Processa o login do usuário."""
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = db.get_usuario_by_email(email)

    if usuario and usuario.senha == senha:
        session['user_id'] = usuario.id
        session['user_nome'] = usuario.nome
        session['user_tipo'] = usuario.tipo

        if usuario.tipo == 'professor':
            return redirect(url_for('admin'))
        return redirect(url_for('dashboard'))

    flash("Email ou senha incorretos!")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Encerra a sessão do usuário."""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Exibe a lista de cursos em que o aluno está matriculado."""
    if 'user_id' not in session:
        return redirect(url_for('index'))

    aluno_id = session['user_id']
    cursos = db.get_cursos_do_aluno(aluno_id)

    return render_template('dashboard.html', cursos=cursos, nome=session['user_nome'])

@app.route('/curso/<int:curso_id>')
def curso_detalhes(curso_id):
    """Exibe os materiais de um curso específico."""
    if 'user_id' not in session:
        return redirect(url_for('index'))

    curso = db.get_curso_by_id(curso_id)
    if not curso:
        return "Curso não encontrado", 404

    materiais = db.get_materiais_by_curso(curso_id)

    return render_template('curso.html', curso=curso, materiais=materiais)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    Painel simples para criar cursos e materiais.
    Em um sistema real, isso teria permissões rigorosas.
    """
    if 'user_id' not in session or session['user_tipo'] != 'professor':
        return "Acesso negado!", 403

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'criar_curso':
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            area = request.form.get('area')
            db.create_curso(nome, descricao, area)
            flash("Curso criado com sucesso!")

        elif action == 'criar_material':
            titulo = request.form.get('titulo')
            conteudo = request.form.get('conteudo')
            curso_id = request.form.get('curso_id')
            db.create_material(titulo, conteudo, int(curso_id))
            flash("Material criado com sucesso!")

        elif action == 'matricular':
            aluno_id = request.form.get('aluno_id')
            curso_id = request.form.get('curso_id')
            db.matricular_aluno(int(aluno_id), int(curso_id))
            flash("Aluno matriculado com sucesso!")

    cursos = db.get_all_cursos()
    # Para simplificar o admin, pegamos todos os usuários alunos
    with db._get_connection() as conn:
        usuarios_alunos = conn.execute("SELECT * FROM usuarios WHERE tipo = 'aluno'").fetchall()
        alunos = [dict(row) for row in usuarios_alunos]

    return render_template('admin.html', cursos=cursos, alunos=alunos)

if __name__ == '__main__':
    app.run(debug=True)
