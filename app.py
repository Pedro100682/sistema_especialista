from flask import Flask, render_template, request
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/avaliar', methods=['POST'])
def avaliar():
    # Captura das respostas
    p1 = request.form['p1']
    p2 = request.form['p2']
    p3 = request.form['p3']
    p4 = request.form['p4']
    p5 = request.form['p5']
    p6 = request.form['p6']
    p7 = request.form['p7']
    p8 = request.form['p8']
    p9 = request.form['p9']
    p10 = request.form['p10']
    p11 = request.form['p11']
    p12 = request.form['p12']
    p13 = request.form['p13']
    p14 = request.form['p14']
    p15 = request.form['p15']
    p16 = request.form['p16']

    # Variáveis de contagem
    risco_alto = 0
    risco_moderado = 0
    risco_leve = 0

    # 🌟 Lógica especial para novas opções de resposta
    if p2 == 'Não há rio por perto':
        risco = "Nenhum risco hídrico direto"
        recomendacao = """- Apesar da ausência de rios ou córregos por perto, monitore chuvas fortes.<br>
                          - Continue atento a alagamentos e outros sinais de risco."""
    elif p9 == 'Não sei':
        risco = "Risco Potencial (incerteza sobre o relevo)"
        recomendacao = """- É importante saber se sua casa está em área de risco.<br>
                          - Reforce a preparação e monitore alertas oficiais."""
    # 🌟 Regras principais
    elif p1 == 'Sim' and p2 == 'Sim' and p8 == 'Sim' and p9 == 'Sim':
        risco = "Inundação Fluvial"
        risco_alto += 1
        recomendacao = """- Saia de casa antes da água subir e vá para um local seguro.<br>
                          - Leve documentos, remédios, roupas e água.<br>
                          - Não tente atravessar áreas alagadas."""
    elif p1 == 'Sim' and p3 == 'Sim' and p4 == 'Sim' and p11 == 'Sim':
        risco = "Inundação Pluvial"
        risco_alto += 1
        recomendacao = """- Saia imediatamente se sua rua costuma alagar.<br>
                          - Feche gás e desligue energia antes de sair.<br>
                          - Ajude vizinhos com dificuldades."""
    elif p1 == 'Sim' and p10 == 'Sim' and p11 == 'Sim':
        risco = "Deslizamento de Terra"
        risco_alto += 1
        recomendacao = """- Saia da casa se chover forte por horas.<br>
                          - Evacue ao menor sinal de instabilidade.<br>
                          - Vá para um abrigo seguro."""
    elif p6 == 'Sim':
        risco = "Tempestade com Ventos Fortes"
        risco_moderado += 1
        recomendacao = """- Fique longe de árvores, postes e janelas.<br>
                          - Desligue aparelhos elétricos.<br>
                          - Busque abrigo seguro."""
    elif p5 == 'Sim' and p13 == 'Sim':
        risco = "Onda de Calor"
        risco_moderado += 1
        recomendacao = """- Beba muita água.<br>
                          - Evite sair no horário de pico de calor.<br>
                          - Cuide especialmente de idosos e crianças."""
    elif p7 == 'Sim' and p11 == 'Sim':
        risco = "Seca Prolongada"
        risco_leve += 1
        recomendacao = """- Economize água.<br>
                          - Proteja plantas e animais.<br>
                          - Informe-se sobre rodízios de abastecimento."""
    else:
        vulnerabilidades = [p12, p13, p14]
        exposicao = [p3, p4, p9, p10, p11]

        if vulnerabilidades.count("Sim") >= 2:
            risco = "Risco Leve (pessoas vulneráveis)"
            risco_leve += 1
            recomendacao = """- Tenha um plano de evacuação.<br>
                              - Organize uma mochila de emergência.<br>
                              - Fique atento aos alertas oficiais."""
        elif p14 == 'Sim' and p15 == 'Sim':
            risco = "Risco Leve (alerta recebido)"
            risco_leve += 1
            recomendacao = """- Reforce os cuidados com moradores vulneráveis.<br>
                              - Revise seus planos de emergência."""
        else:
            risco = "Nenhum risco imediato"
            recomendacao = """- Mantenha-se atento às previsões do tempo.<br>
                              - Mantenha a mochila de emergência preparada.<br>
                              - Saiba onde buscar abrigo em caso de necessidade."""

    return render_template('resultado.html', risco=risco, recomendacao=recomendacao)

# Abre o navegador automaticamente
def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1, abrir_navegador).start()
    app.run(debug=True, use_reloader=False)
