from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Tarefa {self.id}: {self.conteudo}>'

@app.route('/')
def index():
    tarefas = Tarefa.query.all()
    return render_template('home.html', tarefas=tarefas)

@app.route('/add', methods=['POST'])
def add():
    conteudo_tarefa = request.form.get('conteudo')
    nova_tarefa = Tarefa(conteudo=conteudo_tarefa)
    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    tarefa = Tarefa.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
