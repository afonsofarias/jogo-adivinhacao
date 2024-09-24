from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Função para iniciar o jogo
def iniciar_jogo():
    session['numero_secreto'] = random.randint(0, 100)
    session['tentativas_restantes'] = 10
    session['mensagem'] = "Adivinhe um número entre 0 e 100"

@app.route("/", methods=["GET", "POST"])
def index():
    if 'numero_secreto' not in session:
        iniciar_jogo()

    if request.method == "POST":
        try:
            chute = int(request.form['chute'])
        except ValueError:
            session['mensagem'] = "Digite um número válido."
            return render_template('index.html', mensagem=session['mensagem'], tentativas=session['tentativas_restantes'])

        if chute < 0 or chute > 100:
            session['mensagem'] = "Por favor, digite um número entre 0 e 100."
        elif chute < session['numero_secreto']:
            session['mensagem'] = f"{chute} é menor que o número secreto."
            session['tentativas_restantes'] -= 1
        elif chute > session['numero_secreto']:
            session['mensagem'] = f"{chute} é maior que o número secreto."
            session['tentativas_restantes'] -= 1
        else:
            session['mensagem'] = f"Parabéns! {chute} é o número correto!"
            session['tentativas_restantes'] = 0

        if session['tentativas_restantes'] == 0 and chute != session['numero_secreto']:
            session['mensagem'] = f"Fim de jogo! O número era {session['numero_secreto']}."

    return render_template('index.html', mensagem=session['mensagem'], tentativas=session['tentativas_restantes'])

@app.route("/novo_jogo")
def novo_jogo():
    iniciar_jogo()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
