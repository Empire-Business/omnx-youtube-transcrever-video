# Transcrever YouTube

Baixa a legenda de um vídeo do YouTube e entrega o texto sem mudar nenhuma palavra, corrido ou com o tempo marcado. A leitura usa a biblioteca youtube-transcript-api, que não é oficial do YouTube e pode parar de funcionar quando o YouTube mudar.

Guia visual: abra o `COMO-FUNCIONA.html` desta pasta (dois cliques; funciona sem internet).

## Como instalar

**Direto do GitHub:** no Claude Code, diga: "Instale a skill a partir de https://github.com/Empire-Business/omnx-youtube-transcrever-video". Para atualizar, diga: "Atualize a skill a partir de https://github.com/Empire-Business/omnx-youtube-transcrever-video". A IA baixa e copia os arquivos.

Se você já baixou esta pasta:

O caminho mais fácil é pedir para a sua IA:

1. Abra o Claude Code numa conversa nova.
2. Diga: "Instale a skill omnx-youtube-transcrever-video a partir desta pasta" e indique onde a pasta está.
3. A IA copia os arquivos. Você vai ver uma mensagem dizendo que a skill foi instalada.
4. Feche e abra a conversa de novo, para a skill aparecer.

### Mac ou Linux, se preferir fazer sem a IA

Peça para a IA executar o arquivo `install.sh`. Ele copia a pasta para `~/.claude/skills/omnx-youtube-transcrever-video` (`~` é a sua pasta pessoal).

### Windows

1. Peça para a IA: "Copie esta pasta para `%USERPROFILE%\.claude\skills\omnx-youtube-transcrever-video`".
2. Sem IA: copie a pasta com esse nome para `%USERPROFILE%\.claude\skills\` pelo Explorador de Arquivos.
3. Feche e abra a conversa.

## Como usar

- "Transcreve este vídeo: (link)"
- "Pega a legenda deste vídeo com os tempos marcados."
- "Baixa a transcrição em inglês deste vídeo."
- "Quais legendas este vídeo tem?"

## O que você precisa ter

- Claude Code instalado
- Python 3 ou uv (a IA instala, se faltar, com o seu aceite)
- A biblioteca youtube-transcript-api (a IA instala com o seu aceite)
- Internet

## O que esta skill não faz

- O vídeo não tem legenda
- O vídeo é privado, apagado ou tem restrição de idade
- O YouTube bloqueia a sua internet
- Tentar em outra rede
- Atualizar a biblioteca, com seu aceite
- Abrir “Mostrar transcrição” no vídeo e colar o texto
- Transcrever arquivo de áudio ou vídeo do computador
- Editar vídeo: Cortez
- Mudar o texto: resumo ou tradução vêm depois, à parte

## Outra ferramenta

Foi testada no Claude Code. Não foi testada no Codex. O `SKILL.md` traz, na seção "Outra ferramenta (Codex e outras)", as instruções para a sua IA adaptar a skill ao instalar.

Atualizado em 08/11/2026.
