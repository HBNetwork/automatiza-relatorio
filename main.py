import pandas as pd
from datetime import datetime
from pdf_reports import pug_to_html, write_report
from argparse import ArgumentParser, FileType, ArgumentTypeError


def file_must_exist(filename, mode="r"):
    try:
        with open(filename, mode=mode) as f:
            pass
    except OSError as exc:
        raise ArgumentTypeError(exc)


def cli():

    parser = ArgumentParser("autoreport", description="Gera relatórios lindões.")
    parser.add_argument("xls", type=FileType("rb"), help="Nome do arquivo da planilha fonte.")
    parser.add_argument("pdf", type=FileType("wb"), help="Nome do arquivo do relatório gerado.")
    parser.add_argument("-p", "--pug", type=file_must_exist, default="planilhas/modelo_vendas.pug", help="Arquivo de " \
                                                                                                    "estilo.")

    return parser.parse_args()


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


def main(xls, pdf, pug):
    planilha = le_planilha(xls)
    faturamento = calcula_faturamento(planilha)
    quantidade = calcula_quantidade(planilha)
    ticket_medio = calcula_ticket_medio(faturamento, quantidade)
    resumo = calcula_resumo(faturamento, quantidade, ticket_medio)
    escreve_pdf(pdf, pugfile=pug, planilha=planilha, faturamento=faturamento, resumo=resumo)


if __name__ == "__main__":
    main(**vars(cli()))
