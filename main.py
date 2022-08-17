import pandas as pd
from datetime import datetime
from pdf_reports import pug_to_html, write_report

import sys


def cli():
    if len(sys.argv) != 2:
        sys.exit(1)

    return sys.argv[-1]


def le_planilha(filename):
    return pd.read_excel(filename)


def calcula_faturamento(planilha):
    faturamento = planilha[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
    return faturamento.sort_values(by='Valor Final', ascending=False)


def calcula_quantidade(planilha):
    quantidade = planilha[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
    return quantidade.sort_values(by='ID Loja', ascending=False)


def calcula_ticket_medio(faturamento, quantidade):
    ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
    return ticket_medio.rename(columns={0: 'Ticket Medio'})


def calcula_resumo(faturamento, quantidade, ticket_medio):
    faturamento.iloc[0:5].reset_index()
    quantidade.iloc[:25].reset_index()

    tabela_resumo = faturamento.join(quantidade).join(ticket_medio)
    return tabela_resumo.rename(columns={'Valor Final': 'Faturamento Total'})


def hoje(now=datetime.now):
    return now().date()


def escreve_pdf(filename, pugfile, data=hoje, **params):
    html = pug_to_html(pugfile, hoje=data(), **params)
    write_report(html, filename)


if __name__ == "__main__":
    filename = cli()
    planilha = le_planilha(filename)
    faturamento = calcula_faturamento(planilha)
    quantidade = calcula_quantidade(planilha)
    ticket_medio = calcula_ticket_medio(faturamento, quantidade)
    resumo = calcula_resumo(faturamento, quantidade, ticket_medio)
    escreve_pdf("vendas.pdf", pugfile="planilhas/modelo_vendas.pug", planilha=planilha, faturamento=faturamento)
