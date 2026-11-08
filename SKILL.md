---
name: omnx-youtube-transcrever-video
description: "Baixa a legenda de um vídeo do YouTube e entrega o texto sem alterar nenhuma palavra, corrido ou com o tempo marcado. Use quando a pessoa mandar um link ou ID do YouTube e pedir 'transcreve esse vídeo', 'pega a transcrição', 'baixa a legenda', 'quero o texto desse vídeo' ou 'tira o texto com os tempos'. Não use para vídeo sem legenda, arquivo de áudio ou vídeo no computador, editar vídeo (cortez) nem planejar conteúdo de redes sociais (cami)."
---

# Transcrever vídeo do YouTube

Objetivo: entregar o texto da legenda de um vídeo, palavra por palavra. Os caminhos desta skill são relativos à pasta
deste `SKILL.md`.

**Aviso que a pessoa precisa ouvir uma vez:** a leitura usa a biblioteca `youtube-transcript-api`, que não é oficial
do YouTube. Ela pode parar de funcionar quando o YouTube muda, e o YouTube pode bloquear o acesso de algumas redes.
Se falhar, siga a tabela de falhas abaixo.

## Passos

1. Confirme o link ou ID. Sem link, pergunte qual é o vídeo.
2. Rode o script, preferindo o `uv` quando existir, porque ele instala a biblioteca sozinho:
   ```bash
   uv run scripts/transcrever.py "<link>"              # texto corrido
   uv run scripts/transcrever.py "<link>" --tempo      # uma linha por trecho, com [MM:SS]
   uv run scripts/transcrever.py "<link>" --idioma en  # idioma específico
   uv run scripts/transcrever.py "<link>" --listar     # idiomas disponíveis
   ```
   Sem `uv`, use `python3 scripts/transcrever.py`. Se vier `biblioteca_ausente`, peça licença à pessoa ("Posso instalar
   a biblioteca que lê as legendas?") e, com o aceite, crie um ambiente separado em
   `~/.config/omnx-youtube-transcrever-video/venv`, instale `youtube-transcript-api` nele e rode o script com o Python desse
   ambiente.
3. Entregue. Para texto longo, grave em arquivo: pergunte onde, ou use a pasta atual, com `--saida "<id>-transcricao.txt"`.
   O script não sobrescreve arquivo existente.
4. Diga de qual idioma veio e se a legenda é automática (campo `automatica` do resumo, ou `--listar`).

## Regra central

**Nunca altere a transcrição.** Não corrija palavra, pontuação, nome ou gíria; não resuma, não traduza. O texto corrido
muda só as quebras de linha, e o script faz isso. Se a pessoa pedir resumo, roteiro ou tradução, faça depois, em
separado, deixando claro que é outro texto.

## Quando falhar

O erro sai em JSON, com `erro`, `mensagem` e `o_que_fazer`. Traduza para a pessoa em português simples: o que
aconteceu, uma ação e o que você vai fazer.

| `erro` | O que dizer e fazer |
|---|---|
| `sem_legenda` | O vídeo não tem legenda ou está desativada. Rode `--listar`. Se não houver nenhuma, a skill não resolve. |
| `video_indisponivel` | Vídeo apagado, privado, com restrição de idade ou link errado. Confira o link. Não use a conta da pessoa. |
| `bloqueado_pelo_youtube` | O YouTube bloqueou esta internet. Tente outra rede. Se persistir, peça para colar o texto de "Mostrar transcrição" na descrição do vídeo. |
| `falha_na_biblioteca` | A biblioteca pode ter quebrado com alguma mudança do YouTube. Com o aceite da pessoa, atualize-a e tente de novo. Se persistir, use "Mostrar transcrição". |
| `biblioteca_ausente` | Peça licença e instale, conforme o passo 2. |

Não use proxy, cookies, conta da pessoa ou truque para contornar bloqueio. O plano B é ela colar o texto.

## Outro sistema operacional

- No Windows, chame `py -3 scripts/transcrever.py` e crie o ambiente em
  `%USERPROFILE%\.config\omnx-youtube-transcrever-video\venv`; o Python fica em `venv\Scripts\python.exe`. No Linux e no Mac,
  fica em `venv/bin/python`.
- Instale Python ou `uv` pelo gerenciador oficial (Homebrew no Mac, winget no Windows, apt no Linux) com o aceite da
  pessoa. Em alguns sistemas, o comando é `python3`; em outros, `python`.
- A IA testa no computador da pessoa e conta o que realmente funcionou.

## Outra ferramenta (Codex e outras)

Compatível com Claude Code, Codex e outras ferramentas de agentes, em Mac, Windows e Linux. Se a pessoa pedir para instalar
fora do Claude Code, a IA dela adapta na hora, testa no computador dela e conta o que realmente funcionou:
