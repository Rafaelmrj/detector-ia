import re
import math
from collections import Counter


def _normalizar(txt):
    return txt.lower().translate(str.maketrans("áàãâéêíóôõúç", "aaaaeeiooouc"))


def _calcular_score(ttr, desvio, gatilhos, bigramas, n_palavras):
    pts = 0

    if gatilhos >= 12:
        pts += 48
    elif gatilhos >= 8:
        pts += 38
    elif gatilhos >= 5:
        pts += 28
    elif gatilhos >= 3:
        pts += 18
    elif gatilhos >= 1:
        pts += 8

    if n_palavras > 0:
        densidade = (gatilhos / n_palavras) * 100
        if densidade >= 6:
            pts += 12
        elif densidade >= 3:
            pts += 6

    if desvio < 4:
        pts += 22
    elif desvio < 6.5:
        pts += 16
    elif desvio < 8:
        pts += 6

    if ttr < 0.42:
        pts += 18
    elif ttr < 0.50:
        pts += 10
    elif ttr < 0.58:
        pts += 4

    if bigramas > 15:
        pts += 12
    elif bigramas > 8:
        pts += 7
    elif bigramas > 4:
        pts += 3

    if gatilhos >= 5 and desvio < 7:
        pts += 10

    return min(100, pts)


class LinguagemIA:
    def __init__(self):
        self.transicoes = [
            "alem disso", "portanto", "em resumo", "concluindo", "nesse sentido",
            "vale ressaltar", "por outro lado", "em ultima analise", "torna-se imperativo",
            "notavelmente", "e importante notar", "com o intuito de", "com o objetivo de",
        ]
        self.adjetivos = [
            "fundamental", "crucial", "essencial", "revolucionario", "divisor de aguas",
            "bizarro", "perfeito", "indispensavel", "vital", "significativo",
        ]
        self.fechamentos = [
            "em suma", "em sintese", "por fim", "como visto", "dessa forma",
        ]

    def tokenizar(self, texto):
        return re.findall(r"\b\w+\b", _normalizar(texto))

    def extrair_frases(self, texto):
        partes = re.split(r"[.!?]+", texto)
        return [p.strip() for p in partes if len(p.strip()) > 5]

    def calcular_entropia_shannon(self, palavras):
        if not palavras:
            return 0
        n = len(palavras)
        contagem = Counter(palavras)
        h = 0.0
        for qtd in contagem.values():
            p = qtd / n
            h -= p * math.log2(p)
        return round(h, 2)

    def analisar_burstiness(self, frases):
        if len(frases) <= 1:
            return 0.0, 0.0
        tamanhos = [len(f.split()) for f in frases]
        media = sum(tamanhos) / len(tamanhos)
        variancia = sum((x - media) ** 2 for x in tamanhos) / len(tamanhos)
        return round(math.sqrt(variancia), 2), round(media, 2)

    def analisar_n_gramas(self, palavras):
        if len(palavras) < 3:
            return 0.0, 0.0

        bigramas = [(palavras[i], palavras[i + 1]) for i in range(len(palavras) - 1)]
        freq_bi = Counter(bigramas)
        if not bigramas:
            score_bi = 0.0
        else:
            score_bi = sum(v for v in freq_bi.values() if v > 1) / len(bigramas)

        trigramas = [(palavras[i], palavras[i + 1], palavras[i + 2]) for i in range(len(palavras) - 2)]
        freq_tri = Counter(trigramas)
        score_tri = sum(v for v in freq_tri.values() if v > 1) / len(trigramas)

        return round(score_bi * 100, 1), round(score_tri * 100, 1)

    def escanear_padroes_viciados(self, texto_limpo):
        base = _normalizar(texto_limpo)
        trans = [m for m in self.transicoes if m in base]
        adj = [m for m in self.adjetivos if m in base]
        fech = sum(1 for m in self.fechamentos if m in base)
        total = len(trans) + len(adj) + fech
        return total, trans, adj

    def processar_analise_total(self, texto, min_palavras=25):
        palavras = self.tokenizar(texto)
        if len(palavras) < min_palavras:
            return None

        frases = self.extrair_frases(texto)
        ttr = len(set(palavras)) / len(palavras)
        entropia = self.calcular_entropia_shannon(palavras)
        desvio_ritmo, media_frases = self.analisar_burstiness(frases)
        score_bi, score_tri = self.analisar_n_gramas(palavras)
        total_gatilhos, lista_trans, lista_adj = self.escanear_padroes_viciados(texto)
        n_pal = len(palavras)
        score_final = _calcular_score(
            ttr, desvio_ritmo, total_gatilhos, score_bi, n_pal
        )

        return {
            "score": min(score_final, 100),
            "ttr": round(ttr, 2),
            "entropia": entropia,
            "desvio": desvio_ritmo,
            "media_f": media_frases,
            "bigramas": score_bi,
            "trigramas": score_tri,
            "total_gatilhos": total_gatilhos,
            "lista_trans": lista_trans,
            "lista_adj": lista_adj,
            "total_palavras": len(palavras),
            "total_frases": len(frases),
        }
