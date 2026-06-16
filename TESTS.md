# 🧪 Guia de Testes - Finance BOT

Siga este roteiro para validar se as duas versões do BOT estão funcionando corretamente.

## 1. Testes de Registro (V1 e V2)
Envie as seguintes mensagens no Telegram e verifique se o BOT responde "✅ Registrado!":

- **Gasto Simples:** `Café 5.50`
- **Gasto com Categoria:** `Uber 25 reais transporte`
- **Gasto com Forma de Pagamento:** `Mercado 120 no crédito`
- **Receita (Ganho):** `Recebi salário de 5000`

**Validação:** Abra o arquivo `data/gastos.csv` e verifique se as linhas foram adicionadas corretamente.

---

## 2. Testes de Comandos (V1 e V2)
Execute os comandos abaixo e valide a resposta:

- `/ver`: Deve mostrar os últimos 10 registros (incluindo os que você acabou de criar).
- `/resumo`: Deve mostrar o total gasto no mês e o balanço por categoria.
- `/baixar`: O BOT deve enviar o arquivo `gastos.csv` para você no Telegram.
- `/ajuda`: Deve exibir a lista de comandos.
- `/start`: Deve exibir a mensagem de boas-vindas.

---

## 3. Testes de Inteligência RAG (Apenas V2)
Certifique-se de que a API Python está rodando e o arquivo foi indexado. Pergunte:

- **Busca por Descrição:** `/perguntar quanto gastei com pizza?`
- **Busca por Mês Passado:** `/perguntar qual foi meu maior gasto em maio?`
- **Análise Comparativa:** `/perguntar gastei mais com transporte ou alimentação este mês?`
- **Filtro por Categoria:** `/perguntar quanto gastei na categoria lazer em maio?`

**Validação:** A resposta da IA deve ser condizente com os dados reais presentes no CSV.

---

## 4. Dicas de Resolução de Problemas
- **BOT não responde:** Verifique se o `ngrok` está ativo e a `WEBHOOK_URL` está correta no n8n.
- **RAG retorna erro:** Verifique se a API Python (porta 8000) está acessível e se você rodou o nó de indexação.
- **Caracteres Estranhos:** Certifique-se de que o arquivo CSV está sendo salvo em codificação UTF-8.
