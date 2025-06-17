from flask import Flask, render_template, request, make_response
from weasyprint import HTML
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntas')
def perguntas():
    return render_template('perguntas.html')

@app.route('/fim')
def fim():
    return render_template('fim.html')

@app.route('/avaliar', methods=['POST'])
def avaliar():
    try:
        p = {f'p{i}': request.form.get(f'p{i}', '') for i in range(1, 18)}

        if p['p2'] == 'Não há rio por perto':
            risco = "Nenhum risco hídrico direto"
            recomendacao = """- Monitore chuvas intensas mesmo sem rios por perto.<br>
- Fique atento a sinais de alagamento ou solo encharcado.<br>
- Mantenha caminhos de escoamento desobstruídos."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif p['p9'] == 'Não sei':
            risco = "Risco Potencial (incerteza sobre o relevo)"
            recomendacao = """- Busque informações com a Defesa Civil sobre o relevo do local.<br>
- Evite permanecer em áreas baixas ou inclinadas durante chuvas.<br>
- Mantenha rota de evacuação planejada."""
            cor_alerta = "laranja"
            texto_alerta = "ALERTA ALTO: Esteja preparado"

        elif p['p1'] == 'Sim' and p['p2'] == 'Sim' and p['p8'] == 'Sim' and p['p9'] == 'Sim':
            risco = "Inundação Fluvial"
            recomendacao = """- Saia imediatamente para local alto e seguro.<br>
- Leve sua mochila de emergência com itens essenciais.<br>
- Não atravesse áreas alagadas — busque rotas alternativas seguras.<br>
- Informe vizinhos e acompanhe alertas oficiais."""
            cor_alerta = "vermelho"
            texto_alerta = "ALERTA MUITO ALTO: Tome uma atitude"

        elif p['p1'] == 'Sim' and p['p3'] == 'Sim' and p['p4'] == 'Sim' and p['p11'] == 'Sim':
            risco = "Inundação Pluvial"
            recomendacao = """- Abandone a residência caso o alagamento avance.<br>
- Desligue energia e gás antes de sair.<br>
- Use rotas seguras e evite contato com a água contaminada.<br>
- Auxilie crianças, idosos ou pessoas com dificuldades de locomoção."""
            cor_alerta = "vermelho"
            texto_alerta = "ALERTA MUITO ALTO: Tome uma atitude"

        elif (p['p1'] == 'Sim' and p['p10'] == 'Sim') or (p['p1'] == 'Sim' and p['p9'] == 'Sim' and 'encosta' in p['p9'].lower()):
            risco = "Deslizamento de Terra"
            recomendacao = """- Ao menor sinal de rachaduras ou inclinação no terreno, evacue a casa.<br>
- Busque abrigo em local seguro, longe de encostas.<br>
- Nunca durma em áreas de risco durante chuvas prolongadas.<br>
- Mantenha sacos de areia para contenção de água se necessário."""
            cor_alerta = "vermelho"
            texto_alerta = "ALERTA MUITO ALTO: Tome uma atitude"

        elif p['p6'] == 'Sim':
            risco = "Tempestade com Ventos Fortes"
            recomendacao = """- Abrigue-se longe de janelas, árvores e postes.<br>
- Desligue aparelhos elétricos e fique longe de tomadas.<br>
- Não use celular conectado à tomada.<br>
- Após a tempestade, verifique estruturas danificadas com cuidado."""
            cor_alerta = "laranja"
            texto_alerta = "ALERTA ALTO: Esteja preparado"

        elif p['p5'] == 'Sim' and p['p13'] == 'Sim':
            risco = "Onda de Calor"
            recomendacao = """- Beba água regularmente, mesmo sem sede.<br>
- Evite atividades físicas nos horários mais quentes (11h–16h).<br>
- Refresque o ambiente com ventilação natural ou panos molhados.<br>
- Observe sinais de insolação: tontura, pele seca, febre alta."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif p['p7'] == 'Sim' and p['p11'] == 'Sim':
            risco = "Seca Prolongada"
            recomendacao = """- Economize água e reutilize sempre que possível.<br>
- Armazene água potável de forma segura.<br>
- Evite queimadas: o solo seco propaga fogo rapidamente.<br>
- Proteja áreas verdes com cobertura vegetal e irrigação controlada."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif [p['p12'], p['p13'], p['p14']].count("Sim") >= 2:
            risco = "Risco Leve (pessoas vulneráveis)"
            recomendacao = """- Mantenha um plano de evacuação visível e acessível para todos.<br>
- Prepare mochila de emergência com itens de saúde e higiene.<br>
- Combine pontos de encontro e contatos de emergência.<br>
- Auxilie quem tem mais dificuldade de locomoção ou informação."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        elif p['p14'] == 'Sim' and p['p15'] == 'Sim':
            risco = "Risco Leve (alerta recebido)"
            recomendacao = """- Siga rigorosamente as instruções da Defesa Civil.<br>
- Confirme que todos os membros da família conhecem os planos de emergência.<br>
- Revise documentos importantes e deixe-os prontos para evacuação.<br>
- Acompanhe atualizações pelos canais oficiais e rádio."""
            cor_alerta = "amarelo"
            texto_alerta = "ALERTA MODERADO: Esteja atento"

        else:
            risco = "Nenhum risco imediato"
            recomendacao = """- Continue acompanhando as previsões do tempo.<br>
- Mantenha a mochila de emergência abastecida.<br>
- Faça exercícios de evacuação com a família.<br>
- Saiba onde estão os abrigos e contatos de emergência."""
            cor_alerta = "verde"
            texto_alerta = "NORMALIDADE"

        return render_template('resultado.html', risco=risco, recomendacao=recomendacao,
                               cor_alerta=cor_alerta, texto_alerta=texto_alerta)

    except Exception as e:
        return f"Erro na avaliação: {e}", 400

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    risco = request.form['risco']
    recomendacao = request.form['recomendacao'].replace('<br>', '\n')  # substitui <br> por quebra de linha
    cor_alerta = request.form['cor_alerta']
    texto_alerta = request.form['texto_alerta']

    html = render_template('resultado_pdf.html',
                           risco=risco,
                           recomendacao=recomendacao,
                           cor_alerta=cor_alerta,
                           texto_alerta=texto_alerta)

    pdf = HTML(string=html, base_url=request.base_url).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resultado.pdf'
    return response

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1, abrir_navegador).start()
    app.run(debug=True, use_reloader=False)
