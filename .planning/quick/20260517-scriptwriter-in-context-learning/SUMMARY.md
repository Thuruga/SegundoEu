---
status: complete
---

# Quick Task: Implementação de In-Context Learning no Scriptwriter

**Objetivo:** Substituir o conteúdo do 'system' prompt para implementar In-Context Learning, reforçando o idioma pt-BR, o limite de 120-140 palavras e o uso frequente de vírgulas, além de adicionar um exemplo prático do padrão esperado.

## Alterações Realizadas
- Substituição completa da secção `STRICT RULES` e adição do `EXEMPLO DO PADRÃO DE ESCRITA ESPERADO` no `ChatPromptTemplate` do ficheiro `src/agents/scriptwriter.py`.
- **Regras Absolutas:** O prompt agora exige de forma estrita a escrita em pt-BR (sem anotações de palco), um total exato de 120 a 140 palavras e a inclusão de vírgulas a cada 3-4 palavras no máximo para forçar a segmentação e o ritmo lento da locução/legendas.
- **In-Context Learning:** Adicionado um exemplo completo dentro da tag `<script>` contendo um texto filosófico altamente pontuado com vírgulas e as palavras-chave na tag `<keywords>` usando termos visuais sombrios/minimalistas (ex: `foggy night, empty street dark, fading candlelight`).
