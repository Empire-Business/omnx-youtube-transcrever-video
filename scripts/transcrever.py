#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["youtube-transcript-api>=1.2,<2"]
# ///
"""Baixa a legenda de um vídeo do YouTube e devolve o texto sem alterar nenhuma palavra.

Uso:
    transcrever.py <link-ou-id> [--tempo] [--idioma pt-BR,pt,en] [--saida arquivo.txt]
    transcrever.py <link-ou-id> --listar

Saída:
    Sem --saida, o texto vai para a saída padrão.
    Com --saida, grava o arquivo (nunca sobrescreve) e imprime um resumo em JSON.
    Erros saem em JSON na saída de erro, com o campo "erro" e o que fazer.

Códigos de saída:
    0 ok | 1 entrada inválida | 2 sem legenda | 3 biblioteca ausente | 4 bloqueio ou falha do YouTube
"""
import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = r"[A-Za-z0-9_-]{11}"
PADROES_LINK = [
    r"[?&]v=(" + ID_RE + r")(?![A-Za-z0-9_-])",
    r"youtu\.be/(" + ID_RE + r")(?![A-Za-z0-9_-])",
    r"youtube(?:-nocookie)?\.com/(?:embed|v|shorts|live)/(" + ID_RE + r")(?![A-Za-z0-9_-])",
]
IDIOMAS_PADRAO = "pt-BR,pt,en,es"
TAMANHO_PARAGRAFO = 600
TAMANHO_MAXIMO_PARAGRAFO = 1000


def extrair_id(entrada):
    """Devolve o ID de 11 caracteres de um link do YouTube ou de um ID puro, ou None."""
    texto = entrada.strip()
    if re.fullmatch(ID_RE, texto):
        return texto
    for padrao in PADROES_LINK:
        achado = re.search(padrao, texto)
        if achado:
            return achado.group(1)
    return None


def formatar_tempo(segundos):
    total = int(segundos)
    horas, resto = divmod(total, 3600)
    minutos, segs = divmod(resto, 60)
    if horas:
        return "{:02d}:{:02d}:{:02d}".format(horas, minutos, segs)
    return "{:02d}:{:02d}".format(minutos, segs)


def limpar_quebras(texto):
    """Só tira quebras de linha internas da legenda. Não muda nenhuma palavra."""
    return " ".join(texto.split())


def texto_corrido(trechos):
    """Junta os trechos em parágrafos. Muda só as quebras de linha, nunca as palavras."""
    paragrafos = []
    atual = []
    tamanho = 0
    for trecho in trechos:
        pedaco = limpar_quebras(trecho["text"])
        if not pedaco:
            continue
        atual.append(pedaco)
        tamanho += len(pedaco) + 1
        fim_de_frase = pedaco[-1] in ".!?…"
        if (tamanho >= TAMANHO_PARAGRAFO and fim_de_frase) or tamanho >= TAMANHO_MAXIMO_PARAGRAFO:
            paragrafos.append(" ".join(atual))
            atual = []
            tamanho = 0
    if atual:
        paragrafos.append(" ".join(atual))
    return "\n\n".join(paragrafos)


def texto_com_tempo(trechos):
    linhas = []
    for trecho in trechos:
        pedaco = limpar_quebras(trecho["text"])
        if pedaco:
            linhas.append("[{}] {}".format(formatar_tempo(trecho["start"]), pedaco))
    return "\n".join(linhas)


def falhar(codigo, erro, mensagem, o_que_fazer):
    corpo = {"erro": erro, "mensagem": mensagem, "o_que_fazer": o_que_fazer}
    print(json.dumps(corpo, ensure_ascii=False), file=sys.stderr)
    sys.exit(codigo)


def carregar_biblioteca():
    try:
        import youtube_transcript_api as biblioteca
    except ImportError:
        falhar(
            3,
            "biblioteca_ausente",
            "Falta a biblioteca que lê as legendas do YouTube.",
            "Peça permissão à pessoa e rode pelo uv (uv run) ou instale num ambiente separado. Veja o SKILL.md.",
        )
    return biblioteca


def classificar_falha(biblioteca, excecao):
    """Traduz a exceção da biblioteca para (código, erro, mensagem, o que fazer)."""
    nome = type(excecao).__name__
    sem_legenda = {
        "TranscriptsDisabled": "O dono do vídeo desativou as legendas.",
        "NoTranscriptFound": "Este vídeo não tem legenda nos idiomas pedidos.",
    }
    if nome in sem_legenda:
        return (2, "sem_legenda", sem_legenda[nome],
                "Rode com --listar para ver os idiomas. Sem nenhuma legenda, esta skill não resolve.")
    indisponivel = {
        "VideoUnavailable": "O vídeo não existe mais ou o link está errado.",
        "VideoUnplayable": "O YouTube não deixa reproduzir este vídeo.",
        "AgeRestricted": "O vídeo tem restrição de idade e exige conta conectada.",
        "InvalidVideoId": "O ID do vídeo não é válido.",
    }
    if nome in indisponivel:
        return (2, "video_indisponivel", indisponivel[nome],
                "Confira o link com a pessoa. Não tente entrar com a conta dela.")
    if nome in ("RequestBlocked", "IpBlocked"):
        return (4, "bloqueado_pelo_youtube",
                "O YouTube bloqueou o acesso a partir desta internet.",
                "Tente em outra rede. Se continuar, peça à pessoa para abrir 'Mostrar transcrição' no vídeo e colar o texto.")
    return (4, "falha_na_biblioteca",
            "A biblioteca não conseguiu ler o vídeo ({}). Ela não é oficial e pode parar quando o YouTube muda.".format(nome),
            "Atualize a biblioteca e tente de novo. Se continuar, peça à pessoa para colar o texto de 'Mostrar transcrição'.")


def escolher_legenda(lista, idiomas):
    """Prefere legenda humana nos idiomas pedidos, depois automática, depois a primeira que houver."""
    disponiveis = list(lista)
    for idioma in idiomas:
        for gerada in (False, True):
            for legenda in disponiveis:
                if legenda.language_code == idioma and legenda.is_generated == gerada:
                    return legenda
    humanas = [l for l in disponiveis if not l.is_generated]
    return (humanas or disponiveis)[0] if disponiveis else None


def gravar_sem_sobrescrever(destino, conteudo):
    caminho = Path(destino).expanduser()
    if caminho.exists():
        falhar(1, "arquivo_ja_existe", "Já existe um arquivo em {}.".format(caminho),
               "Pergunte à pessoa se pode usar outro nome. Este script não sobrescreve.")
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo + "\n", encoding="utf-8")
    return caminho


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Baixa a legenda de um vídeo do YouTube.")
    parser.add_argument("video", help="link ou ID do vídeo")
    parser.add_argument("--tempo", action="store_true", help="uma linha por trecho, com [MM:SS]")
    parser.add_argument("--idioma", default=IDIOMAS_PADRAO, help="códigos em ordem de preferência")
    parser.add_argument("--saida", help="arquivo onde gravar (não sobrescreve)")
    parser.add_argument("--listar", action="store_true", help="só lista os idiomas disponíveis")
    args = parser.parse_args()

    video_id = extrair_id(args.video)
    if not video_id:
        falhar(1, "link_invalido", "Não encontrei um vídeo do YouTube em: {}".format(args.video),
               "Peça o link completo do vídeo.")

    biblioteca = carregar_biblioteca()
    try:
        lista = biblioteca.YouTubeTranscriptApi().list(video_id)
        if args.listar:
            itens = [{"idioma": l.language_code, "nome": l.language, "automatica": l.is_generated} for l in lista]
            print(json.dumps({"video": video_id, "legendas": itens}, ensure_ascii=False, indent=2))
            return
        idiomas = [i.strip() for i in args.idioma.split(",") if i.strip()]
        legenda = escolher_legenda(lista, idiomas)
        if legenda is None:
            falhar(2, "sem_legenda", "Este vídeo não tem legendas.", "Sem legenda, esta skill não resolve.")
        baixada = legenda.fetch()
    except SystemExit:
        raise
    except Exception as excecao:  # a biblioteca muda; toda falha vira mensagem clara
        falhar(*classificar_falha(biblioteca, excecao))

    trechos = [{"text": s.text, "start": s.start} for s in baixada.snippets]
    texto = texto_com_tempo(trechos) if args.tempo else texto_corrido(trechos)
    if not texto.strip():
        falhar(2, "sem_legenda", "A legenda veio vazia.", "Sem texto para entregar. Avise a pessoa.")

    if args.saida:
        caminho = gravar_sem_sobrescrever(args.saida, texto)
        print(json.dumps({
            "video": video_id, "arquivo": str(caminho), "idioma": legenda.language_code,
            "automatica": legenda.is_generated, "trechos": len(trechos), "palavras": len(texto.split()),
        }, ensure_ascii=False, indent=2))
    else:
        print(texto)


if __name__ == "__main__":
    main()
