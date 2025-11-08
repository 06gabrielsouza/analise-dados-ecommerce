# Instruções de Entrega - Projeto de Análise de E-commerce

## Informações Importantes

**ATENÇÃO:** A entrega deverá ser feita **INDIVIDUALMENTE**, informando de qual equipe você faz parte.

## O que Entregar

1. **Relatório Analítico (PDF)**: `reports/relatorio_analitico.pdf`

1. **Código Utilizado**: Todos os notebooks Python na pasta `notebooks/`

1. **Dados Limpos**: `data/ecommerce_clean.csv`

1. **README**: `README.md` (este arquivo explica o projeto)

## Como Preparar a Entrega

### Opção 1: Compactar todo o projeto

```bash
cd /home/ubuntu
zip -r ecommerce-analytics.zip ecommerce-analytics/ -x "ecommerce-analytics/venv/*"
```

### Opção 2: Compactar apenas os arquivos essenciais

```bash
cd /home/ubuntu/ecommerce-analytics
zip -r entrega.zip \
  reports/relatorio_analitico.pdf \
  notebooks/*.py \
  data/ecommerce_clean.csv \
  data/ecommerce_raw.csv \
  figures/*.png \
  README.md \
  INSTRUCOES_ENTREGA.md
```

## Apresentação (29/11)

O trabalho será apresentado no dia **29/11**. Prepare-se para:

1. Explicar a metodologia de limpeza e tratamento dos dados

1. Apresentar os principais KPIs encontrados

1. Discutir os insights acionáveis

1. Demonstrar os testes estatísticos realizados

1. Responder perguntas sobre o código e as análises

## Checklist de Entrega

- [ ] Relatório em PDF está completo e legível

- [ ] Todos os notebooks estão funcionando

- [ ] README.md explica como reproduzir a análise

- [ ] Informei de qual equipe faço parte

- [ ] Revisei os principais insights e KPIs

- [ ] Testei a execução do script `run_all.sh`

## Contato

Em caso de dúvidas sobre o projeto ou a análise, consulte o README.md ou os comentários nos notebooks Python.

Boa sorte! 🚀

