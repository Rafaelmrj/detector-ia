from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


_PASTA_PROJETO = Path(__file__).resolve().parent.parent


def renderizar_painel_teoria():
    css_path = _PASTA_PROJETO / "interface" / "painel-teoria.css"
    html_path = _PASTA_PROJETO / "interface" / "painel-teoria.html"
    
    if not css_path.is_file() or not html_path.is_file():
        st.error(
            "Arquivos painel-teoria.css e painel-teoria.html precisam estar "
            f"na pasta: {_PASTA_PROJETO / 'interface'}"
        )
        return
    
    css_content = css_path.read_text(encoding='utf-8')
    html_content = html_path.read_text(encoding="utf-8")
    
    # Injeta CSS dentro do HTML
    html_with_css = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>{css_content}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    components.html(html_with_css, height=600, scrolling=True)


def renderizar_veredito_html(score):
    if score < 35:
        st.markdown(
            f'<div class="badge" style="background: rgba(46, 213, 115, 0.15); border: 1px solid #2ed573; color: #2ed573;">✓ Índice de Similaridade Sintática: {score}% — Padrão de Escrita Humana</div>',
            unsafe_allow_html=True
        )
    elif score < 70:
        st.markdown(
            f'<div class="badge" style="background: rgba(255, 165, 0, 0.15); border: 1px solid #ffa500; color: #ffa500;">⚠ Índice de Similaridade Sintática: {score}% — Estrutura Híbrida Atípica (Alta Suspeita)</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="badge" style="background: rgba(255, 71, 87, 0.15); border: 1px solid #ff4757; color: #ff4757;">🔬 Índice de Similaridade Sintática: {score}% — Alta Densidade de Linguagem Artificial</div>',
            unsafe_allow_html=True
        )


def card_html(titulo, valor, sulfixo=""):
    st.markdown(
        f"""
        <div class="custom-card">
            <div class="card-title">{titulo}</div>
            <div class="card-value">{valor}<span style="font-size:1rem; color:#8fa0bc; font-weight:400;"> {sulfixo}</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )
