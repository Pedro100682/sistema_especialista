from flask import Flask, render_template, request
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('perguntas.html')

@app.route('/avaliar', methods=['POST'])
def avaliar():
    try:
        # Captura das respostas do formulário (17 perguntas)
        p = {f'p{i}': request.form.get(f'p{i}', '') for i in range(1, 18)}

        # Regras de decisão para avaliação de risco
        if p['p2'] == 'Não há rio por perto':
            risco = "Nenhum risco hídrico direto"
            recomendacao = """- Apesar da ausência de rios ou córregos por perto, monitore chuvas fortes.<br>
                              - Continue atento a alagamentos e outros sinais de risco."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif p['p9'] == 'Não sei':
            risco = "Risco Potencial (incerteza sobre o relevo)"
            recomendacao = """- É importante saber se sua casa está em área de risco.<br>
                              - Reforce a preparação e monitore alertas oficiais."""
            cor_alerta = "laranja"
            texto_alerta = "ALERTA ALTO: Esteja preparado"

        elif p['p1'] == 'Sim' and p['p2'] == 'Sim' and p['p8'] == 'Sim' and p['p9'] == 'Sim':
            risco = "Inundação Fluvial"
            recomendacao = """- Saia de casa antes da água subir e vá para um local seguro.<br>
                              - Leve documentos, remédios, roupas e água.<br>
                              - Não tente atravessar áreas alagadas."""
            cor_alerta = "vermelho"
            texto_alerta = "ALERTA MUITO ALTO: Tome uma atitude"

        elif p['p1'] == 'Sim' and p['p3'] == 'Sim' and p['p4'] == 'Sim' and p['p11'] == 'Sim':
            risco = "Inundação Pluvial"
            recomendacao = """- Saia imediatamente se sua rua costuma alagar.<br>
                              - Feche gás e desligue energia antes de sair.<br>
                              - Ajude vizinhos com dificuldades."""
            cor_alerta = "vermelho"
            texto_alerta = "ALERTA MUITO ALTO: Tome uma atitude"

        elif (p['p1'] == 'Sim' and p['p10'] == 'Sim') or (p['p1'] == 'Sim' and p['p9'] == 'Sim' and 'encosta' in p['p9'].lower()):
            risco = "Deslizamento de Terra"
            recomendacao = """- Saia da casa se chover forte por horas ou houver risco em encostas.<br>
                              - Evacue ao menor sinal de rachaduras ou trincas no solo.<br>
                              - Vá para um abrigo seguro imediatamente."""
            cor_alerta = "vermelho"
            texto_alerta = "ALERTA MUITO ALTO: Tome uma atitude"

        elif p['p6'] == 'Sim':
            risco = "Tempestade com Ventos Fortes"
            recomendacao = """- Fique longe de árvores, postes e janelas.<br>
                              - Desligue aparelhos elétricos.<br>
                              - Busque abrigo seguro."""
            cor_alerta = "laranja"
            texto_alerta = "ALERTA ALTO: Esteja preparado"

        elif p['p5'] == 'Sim' and p['p13'] == 'Sim':
            risco = "Onda de Calor"
            recomendacao = """- Beba muita água.<br>
                              - Evite sair no horário de pico de calor.<br>
                              - Cuide especialmente de idosos e crianças."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif p['p7'] == 'Sim' and p['p11'] == 'Sim':
            risco = "Seca Prolongada"
            recomendacao = """- Economize água.<br>
                              - Proteja plantas e animais.<br>
                              - Informe-se sobre rodízios de abastecimento."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif [p['p12'], p['p13'], p['p14']].count("Sim") >= 2:
            risco = "Risco Leve (pessoas vulneráveis)"
            recomendacao = """- Tenha um plano de evacuação.<br>
                              - Organize uma mochila de emergência.<br>
                              - Fique atento aos alertas oficiais."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif p['p14'] == 'Sim' and p['p15'] == 'Sim':
            risco = "Risco Leve (alerta recebido)"
            recomendacao = """- Reforce os cuidados com moradores vulneráveis.<br>
                              - Revise seus planos de emergência."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        else:
            risco = "Nenhum risco imediato"
            recomendacao = """- Mantenha-se atento às previsões do tempo.<br>
                              - Mantenha a mochila de emergência preparada.<br>
                              - Saiba onde buscar abrigo em caso de necessidade."""
            cor_alerta = "verde"
            texto_alerta = "NORMALIDADE"

        return render_template('resultado.html', risco=risco, recomendacao=recomendacao,
                               cor_alerta=cor_alerta, texto_alerta=texto_alerta)

    except Exception as e:
        return f"Erro na avaliação: {e}", 400

# Abre o navegador automaticamente
def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1, abrir_navegador).start()
    app.run(debug=True, use_reloader=False)
