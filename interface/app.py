import sys
from pathlib import Path
import pandas as pd
import streamlit as st

_APP_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _APP_DIR.parent

if str(_PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROJECT_DIR))

from core.engine import LinguagemIA
from interface.styles import renderizar_painel_teoria, renderizar_veredito_html

MIN_PALAVRAS = 25

st.set_page_config(page_title="Detector de IA", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a2332;
        --border: rgba(99, 102, 241, 0.2);
        --border-glow: rgba(99, 102, 241, 0.4);
        --text: #f1f5f9;
        --text-dim: #94a3b8;
        --cyan: #06b6d4;
        --blue: #3b82f6;
        --violet: #8b5cf6;
        --emerald: #10b981;
        --rose: #f43f5e;
        --gradient-cyan: linear-gradient(135deg, #06b6d4, #3b82f6);
        --gradient-violet: linear-gradient(135deg, #8b5cf6, #ec4899);
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background: var(--bg-primary);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: var(--gradient-cyan);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .stCaption {
        color: var(--text-dim);
        font-size: 0.95rem;
    }
    
    .glass-card {
        background: linear-gradient(135deg, rgba(26, 35, 50, 0.95), rgba(17, 24, 39, 0.98));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    }
    
    .badge {
        line-height: 1.6;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-dim);
    }
    
    [data-testid="stTextArea"] > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    
    [data-testid="stTextArea"] textarea {
        background: transparent;
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button {
        background: var(--gradient-cyan);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(6, 182, 212, 0.5);
    }
    
    [data-testid="stExpanderToggleIcon"] {
        color: var(--cyan);
    }
    
    h3 {
        color: var(--text);
        font-weight: 700;
    }
    
    .streamlit-expanderHeader {
        color: var(--text-dim);
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-title">Detector de IA</h1>', unsafe_allow_html=True)
st.caption("Ferramenta de detecção de texto gerado por inteligência artificial, baseada em análise linguística avançada.")
st.divider()

col_esq, col_dir = st.columns([1.1, 1])

with col_esq:
    st.subheader("📥 Insira o texto que deseja analisar")
    txt = st.text_area(
        "texto",
        height=350,
        placeholder="Digite ou cole o texto aqui...",
        label_visibility="collapsed",
    )
    btn = st.button("🔬 Iniciar Análise", use_container_width=True)

with col_dir:
    st.subheader("📊 Relatório do texto")

    if btn and txt.strip():
        res = LinguagemIA().processar_analise_total(txt)

        if res:
            renderizar_veredito_html(res["score"])
            st.write("")

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Diversidade (TTR)", f"{res['ttr'] * 100:.0f}%",
                help="Palavras únicas ÷ total. Baixo = vocabulário repetido.",
            )
            c2.metric(
                "Ritmo (desvio)", f"{res['desvio']} pal.",
                help="Variação no tamanho das frases. IA costuma ficar abaixo de 6,5.",
            )
            c3.metric(
                "Entropia", f"{res['entropia']} bits",
                help="Imprevisibilidade do vocabulário (Shannon).",
            )

            st.write("---")

            c4, c5, c6 = st.columns(3)
            c4.metric(
                "Bigramas repetidos", f"{res['bigramas']}%",
                help="Pares de palavras que se repetem no texto.",
            )
            c5.metric(
                "Gatilhos", res["total_gatilhos"],
                help="Marcadores típicos de IA (conectivos, clichês). Quanto mais, mais suspeito.",
            )
            c6.metric(
                "Média por frase", f"{res['media_f']} pal.",
                help="Média de palavras por frase — contexto do ritmo.",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.subheader("Evidências")
            with st.expander("Marcadores encontrados"):
                trans = res["lista_trans"] or ["nenhum"]
                adj = res["lista_adj"] or ["nenhum"]
                st.write("**Conectivos:** " + ", ".join(trans))
                st.write("**Adjetivos genéricos:** " + ", ".join(adj))
       
            st.subheader("📈 Distribuição")
            df = pd.DataFrame({
                "Métrica": ["TTR", "Ritmo", "Bigramas"],
                "Valor (%)": [res["ttr"] * 100, min(res["desvio"] * 10, 100), res["bigramas"]],
            })
            st.bar_chart(df, x="Métrica", y="Valor (%)")

        else:
            st.error(f"Texto curto demais (mínimo {MIN_PALAVRAS} palavras).")

    elif btn:
        st.warning("Cole um texto na coluna da esquerda.")
    else:
        st.info("Aguardando texto para analisar.")

st.divider()
renderizar_painel_teoria()
