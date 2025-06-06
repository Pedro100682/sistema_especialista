from flask import Flask, render_template, request
import threading
import webbrowser

app = Flask(__name__)  # Definido antes do uso

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/avaliar', methods=['POST'])
def avaliar():
    # Captura das respostas
    p1 = request.form['p1']  # Está chovendo muito forte hoje ou nos três últimos dias?
    p2 = request.form['p2']  # Você viu/ouviu falar que o rio, arroio ou córrego da sua região está subindo ou transbordando?
    p3 = request.form['p3']  # Mesmo sem rio por perto, a sua rua já alagou quando chove muito?
    p4 = request.form['p4']  # A água da chuva acumula rápido na sua rua ou no seu quintal?
    p5 = request.form['p5']  # Está fazendo muito calor nos últimos dias?
    p6 = request.form['p6']  # Está ventando muito forte ou houve tempestade recente?
    p7 = request.form['p7']  # Está há muitos dias sem chover (mais de 30 dias) e a vegetação está secando?
    p8 = request.form['p8']  # Sua casa está próxima de rio, arroio, córrego ou barranco?
    p9 = request.form['p9']  # Sua casa está em área mais baixa do que as casas vizinhas?
    p10 = request.form['p10']  # Sua casa está localizada em morro ou encosta?
    p11 = request.form['p11']  # Há muita pavimentação (asfalto/concreto) e pouca vegetação na sua área de moradia?
    p12 = request.form['p12']  # Há pessoas com mobilidade reduzida na residência?
    p13 = request.form['p13']  # Há idosos, crianças pequenas ou pessoas com doenças na residência?
    p14 = request.form['p14']  # Você já recebeu algum aviso da Defesa Civil, prefeitura, rádio, TV ou celular sobre riscos climáticos?
    p15 = request.form['p15']  # Você e sua família sabem para onde ir em caso de emergência?
    p16 = request.form['p16']  # Você tem  uma mochila de emergência preparada com documentos, remédios e itens essenciais?

     # Variáveis de contagem
    risco_alto = 0
    risco_moderado = 0
    risco_leve = 0

    # Lógica baseada na árvore e contexto
    if p1 == 'Sim' and p2 == 'Sim' and p8 == 'Sim' and p9 == 'Sim':
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
        # Avaliação combinada com outras respostas
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
