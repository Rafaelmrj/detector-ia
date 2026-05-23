# Detector de Escrita de I.A - Auditoria Linguística

Este projeto é uma ferramenta desenvolvida para identificar o uso de Inteligência Artificial (como ChatGPT) em textos acadêmicos e científicos. A análise é feita de forma estatística, avaliando padrões humanos de escrita como a variedade de vocabulário, a complexidade das palavras usadas e a variação no tamanho das frases (ritmo autoral).

---

## Como o projeto está organizado

* **`core/`**: Pasta com a inteligência do sistema (`engine.py`), que faz todos os cálculos matemáticos do texto.
* **`interface/`**: Pasta que cuida da parte visual que você vê na tela.
    * `app.py`: O arquivo principal que junta o visual com a lógica e roda o sistema.
    * `styles.py`: Arquivo que configura as tarjas de veredito, cores e os cards.
    * `painel-teoria.html` e `.css`: A página de documentação teórica do projeto.

---

## Guia de Instalação (Passo a passo)

### Passo 1: Instalar o Python
O sistema precisa do Python instalado para funcionar.
1. Acesse o site oficial: https://www.python.org
2. Vá em **Downloads** e baixe a versão recomendada para o seu Windows.
3. **⚠️ ATENÇÃO:** Quando abrir o instalador, antes de clicar em qualquer outra coisa, marque a caixinha **"Add python.exe to PATH"** na parte de baixo da janela. Depois, clique em "Install Now" e avance até o fim.

### Passo 2: Abrir o terminal dentro da pasta certa
1. Abra o gerenciador de arquivos do Windows e vá até a pasta do projeto (chamada `detector-ia`).
2. Segure a tecla **Shift** no seu teclado e, ao mesmo tempo, dê um **clique com o botão direito do mouse** em qualquer espaço em branco dentro dessa pasta.
3. No menu que abrir, clique em **"Abrir no Terminal"** (ou "Abrir janela de comando aqui"). Uma tela preta vai aparecer.

### Passo 3: Instalar os pacotes necessários
Com a tela preta aberta, copie o comando abaixo, cole nele e aperte a tecla **Enter**:

```bash
python -m pip install streamlit pandas   



