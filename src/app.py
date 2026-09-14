import json
import pandas as pd
import requests
import streamlit as st

## CONFIGS ##
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

## Load Data ##
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))


## Creating Contet ## 
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R${perfil['patrimonio_total']} | RESERVA: R${perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

## SYSTEM PROMPT ##
SYSTEM_PROMPT = """Você é GIO, um agente financeiro inteligente especializado em auxiliar o usuário a entender melhor o mundo financeiro.
OBJETIVO:
ensinar o usuário sobre conceitos básicos de educação financeira e economia e recomendar tipos de investimento que estejam dentro do perfil dele.

REGRAS:
- JAMAIS responda sobre assuntos fora do tema de ensino de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Sempre baseie suas respostas nos dados fornecidos;
- Nunca invente informações financeiras;
- Sempre pergunte o perfil cliente antes de recomendar investimentos;
- Sempre que recomendar um investimento, explique todos os riscos envolvidos e os retornos.
- Nunca recomende um tipo de investimento fora do perfil de investidor do usuário/cliente;
- Se não souber algo, admita e ofereça alternativas;
"""

## Call Ollama ##
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}
    
    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model" : MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']


## INTERFACE ##
st.title("Olá, sou o GIO, o que posso lhe ensinar hoje?")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))