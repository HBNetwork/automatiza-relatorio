import pandas as pd
from datetime import datetime
from pdf_reports import pug_to_html, write_report
# A biblioteca datetime vai ser fundamental para criação do relatório da data, uma vez importada, a cada vez que o código for gerado, o relatório ficará com a data atual

#pip install pdf_reports -q


planilha = pd.read_excel("planilhas/Vendas_diogo.xlsx")

# Calculos da planilha

faturamento = planilha[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
faturamento = faturamento.sort_values(by='Valor Final', ascending=False)


quantidade = planilha[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
quantidade = quantidade.sort_values(by='ID Loja', ascending=False)


hoje = datetime.now().date()
# a variavél hoje vai ser importante para a atualização do relatório

html = pug_to_html('planilhas/modelo_vendas.pug',planilha=planilha,hoje=hoje, faturamento=faturamento)
# localizar o caminho do modelo de relatório e informar todos as váriavéis que são expostas no relatório final, em PDF

write_report(html, 'vendas.pdf')
# aqui vamos criar o pdf, nomeando ele. Lembre-se de alterar o dados no .pug de acordo com sua necessidade.


#Calculo para apresentação do relatório
faturamento.iloc[0:5].reset_index()

quantidade.iloc[:25].reset_index()

ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Medio'})


faturamento = faturamento


tabela_resumo = faturamento.join(quantidade).join(ticket_medio)
tabela_resumo = tabela_resumo.rename(columns={'Valor Final': 'Faturamento Total'})


