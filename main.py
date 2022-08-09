import pandas as pd
from datetime import datetime
from pdf_reports import pug_to_html, write_report

import sys
parametro = []
for param in sys.argv :
    parametro.append(param)

#print(parametro.pop())

#pip install pdf_reports -q


planilha = pd.read_excel(parametro.pop())
#planilha = pd.read_excel("planilhas/Vendas_diogo.xlsx")

# Calculos da planilha

faturamento = planilha[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
faturamento = faturamento.sort_values(by='Valor Final', ascending=False)


quantidade = planilha[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
quantidade = quantidade.sort_values(by='ID Loja', ascending=False)


hoje = datetime.now().date()


html = pug_to_html('planilhas/modelo_vendas.pug',planilha=planilha,hoje=hoje, faturamento=faturamento)


write_report(html, 'vendas.pdf')

faturamento.iloc[0:5].reset_index()

quantidade.iloc[:25].reset_index()

ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Medio'})


faturamento = faturamento


tabela_resumo = faturamento.join(quantidade).join(ticket_medio)
tabela_resumo = tabela_resumo.rename(columns={'Valor Final': 'Faturamento Total'})


