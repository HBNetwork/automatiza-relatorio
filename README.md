# automatiza-relatorio


## Considerações iniciais do projeto
    
Este projeto foi elaborado no intuito de suprir uma necessidade real: extrair informações relevantes de uma base de daods gerando um relaório automatizado em PDF.

## Problema e Solução

Utilzando Python podemos automatizar rotinas que exigem tarefas repepetivas. No caso real desse projeto, é necessário um gestor alimentar uma base de dados constantemente, extraindo  informações de outras unidades, diariamente.

A solução proposta contempla a criação de um arquivo único, gerado automaticamente e devidamente exportado para PDF.

## Procedimentos necessários

Em nossos testes, foi observado uma certa dependência ao instalar a lib pdf_reports.

Em resumo, identificamos que usúarios do MAC necessitam instalação do pacote PANGO, enquanto usuários do Windows necessitam instalação do GTK.

Para maiores informações : https://doc.courtbouillon.org/weasyprint/stable/first_steps.html

