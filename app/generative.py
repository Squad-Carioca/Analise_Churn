import google.generativeai as genai 
import os 
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF


# Carregar a chave de API do arquivo .env 
load_dotenv() 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=GOOGLE_API_KEY)

def gerar_pdf(conteudo_relatorio, nome_arquivo):

    # 1. Cria uma instância da classe FPDF
    pdf = FPDF('P', 'mm', 'A4')  # 'P' de Portrait (retrato), 'mm' (milímetros), 'A4'
       # 2. Adiciona uma página
    pdf.add_page()
    # 3. Define a fonte (ex: Arial, Bold, tamanho 16)
    pdf.set_font("Arial", size=12)
    # 4. Adiciona um título (opcional)
    pdf.write(5, "Relatório Gerado\n\n") 
    # 5. Adiciona o conteúdo da sua variável ao PDF
    # '5' é a altura de linha em mm
    pdf.write(5, conteudo_relatorio)
    # 6. Salva o PDF no sistema de arquivos
    try:
        pdf.output(nome_arquivo)
        print(f"Relatório PDF '{nome_arquivo}' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")

def criar_prompt_marketing_telecom(dados_cliente):
    return f"""
Aja como um Analista de Marketing Sênior especializado em Retenção de Clientes
no setor de Telecomunicações. Sua missão é gerar relatórios estratégicos, claros
e profissionais em três parágrafos, usando exclusivamente os dados abaixo.

Dados do Cliente
Predicao: {dados_cliente.get('predicao', 'N/A')}
Probabilidade_churn: {dados_cliente.get('probabilidade_churn', 'N/A')}
Explicacao: {dados_cliente.get('explicacao', 'N/A')}


Com base exclusivamente nesses dados, gere um relatório:

Primeiro parágrafo:
risco: alto, médio ou baixo (justifique com dados),
quais variáveis mais influenciam esse risco,
destaque padrões relevantes (ex.: alto uso internacional, uso diurno elevado, muitas ligações ao suporte).

Segundo parágrafo:
Recomendações de Ação para Marketing:
Indique pelo menos 3 ações práticas, como:
ofertas específicas personalizadas,
upgrades de plano alinhados ao padrão de uso,
ações de retenção segmentadas,
redução de atritos operacionais,
comunicação direcionada (ex.: campanhas educativas ou preventivas),
qualquer outra recomendação estratégica baseada nos dados.

Terceiro parágrafo:
Conclusão
"""

def gerar_relatorio(dados_cliente): 
    """ 
    Gera um relatório usando o LLM com base nos dados e no tipo de projeto. 
    """ 
    print("\n--- Gerando Relatório com IA Generativa ---")

    # Obtém data no formato desejado
    data_atual = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"data\Relatotio_retencao_{data_atual}.pdf" 

    prompt = criar_prompt_marketing_telecom(dados_cliente)


    try: 
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt) 
        print("Relatório gerado com sucesso!") 
        
        gerar_pdf(response.text, nome_arquivo)
        
        return response.text

    except Exception as e: 
        print(f"Erro ao chamar a API do Gemini: {e}") 
        return "Erro na geração do relatório."

