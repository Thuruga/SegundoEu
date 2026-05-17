---
status: incomplete
---

<description>
Atualizar o estado da aplicação e o prompt do Scriptwriter:
1. `src/state.py`: Mudar `video_path` de string opcional para `video_paths: Optional[List[str]]`.
2. `src/agents/scriptwriter.py`: Ensinar a IA a usar asteriscos para ênfase vocal e atualizar a geração de keywords para 3-4 conceitos visuais distintos/abstratos em inglês que servirão como Cenas.
</description>

<tasks>
1. Substituir `video_path: Optional[str]` por `video_paths: Optional[List[str]]` em `src/state.py`.
2. Em `src/agents/scriptwriter.py`, adicionar regra para uso de asteriscos (ex: *palavra*).
3. Modificar a instrução `<keywords>` para pedir 3 a 4 conceitos totalmente distintos e abstratos.
4. Atualizar o exemplo de In-Context Learning com asteriscos no texto e 4 conceitos visuais distintos nas keywords.
5. Verificar sintaxe.
6. Criar SUMMARY.md, atualizar STATE.md e fazer commit/push.
</tasks>
