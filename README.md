# 📊 Projeto de Análise de Dados de E-commerce Brasileiro

## 👨‍💻 Equipe

| Nome | Responsabilidade Principal | Turma |
| :--- | :--- | :--- |
| **Gabriel dos Santos Souza** | Limpeza de Dados, Feature Engineering, Análise Exploratória (EDA) | 3º Período - ADS Embarque Digital |
| **Leandro de Morais** | Inferência Estatística, Cálculo de KPIs, Geração de Insights, Relatório Analítico | 3º Período - ADS Embarque Digital |

## 🎯 Contexto e Objetivos

Este projeto visa fornecer à direção de um e-commerce brasileiro respostas confiáveis e com tratamento estatístico sobre as principais métricas de negócio: receita, margens, frete, prazos de entrega e comportamento do cliente.

O objetivo final é produzir um **Relatório Analítico** robusto, acompanhado de um código Python totalmente reprodutível, que demonstre o rigor da análise exploratória e inferencial realizada.

## ✅ Requisitos Atendidos (Checklist)

O projeto foi desenvolvido para atender integralmente a todos os requisitos solicitados, conforme detalhado na tabela abaixo:

| Categoria | Requisito | Status | Detalhes da Implementação |
| :--- | :--- | :--- | :--- |
| **Entregável** | Relatório Analítico (PDF/MD) | **OK** | Gerado em `reports/relatorio_analitico.pdf` e `reports/relatorio_analitico.md`. |
| **Qualidade de Dados** | Diagramas, Chaves, Integridade, Deduplicação | **OK** | Verificação de unicidade (`Order_ID`), tratamento de NA, remoção de duplicatas e validação de cálculos no `01_data_cleaning.py`. |
| **Análise Descritiva** | Medidas de Tendência/Dispersão, EDA com gráficos | **OK** | Estatísticas descritivas e 13 visualizações (histogramas, boxplots, heatmaps) nos notebooks `03_` e `04_`. |
| **Inferência** | ICs para médias/proporções, verificação de suposições | **OK** | IC 95% para Ticket Médio, Taxa de Atraso e Confirmação. Testes de normalidade e hipóteses no `05_statistical_inference.py`. |
| **Reprodutibilidade** | Notebook Python + SQL | **OK** | 6 notebooks Python sequenciais, script `run_all.sh` para automação e arquivo `schema.sql` para estrutura de dados. |
| **KPIs** | Receita, Ticket Médio, Frete, Atraso, Conversão, Mix, Sazonalidade | **OK** | Todos os KPIs calculados e analisados no `06_kpis_insights.py`. |

## 🛠️ Estrutura do Projeto e Pipeline de Análise

O projeto segue uma estrutura modular e um pipeline de análise bem definido, garantindo a rastreabilidade e a reprodutibilidade.

### Estrutura de Diretórios

```
/ecommerce-analytics
├── data/                 # Dados brutos, intermediários e limpos (ecommerce_clean.csv)
│   └── schema.sql        # Arquivo SQL com o esquema das tabelas (para requisito de reprodutibilidade)
├── figures/              # Gráficos e visualizações gerados (.png)
├── notebooks/            # Código-fonte da análise (6 notebooks Python)
├── reports/              # Relatório Analítico (.md, .pdf) e resumos de inferência
├── venv/                 # Ambiente virtual Python
├── README.md             # Documentação do projeto (Este arquivo)
└── run_all.sh            # Script para execução completa da pipeline
```

### Detalhamento do Código (Notebooks)

| Notebook | Responsável | Fase da Análise | Descrição Detalhada |
| :--- | :--- | :--- | :--- |
| `01_data_cleaning.py` | Gabriel | Data Cleaning | Carregamento, tratamento de tipos, NA (imputação por mediana/zero), e remoção de duplicatas por `Order_ID`. |
| `02_feature_engineering.py` | Gabriel | Feature Engineering | Criação de 13 novas variáveis (ex: `delivery_delay_days`, `freight_share`, `is_late`) e tratamento de outliers extremos (Z-score > 3) para garantir a robustez dos testes estatísticos subsequentes. |
| `03_exploratory_analysis.py` | Gabriel | EDA (Descritiva) | Análise univariada (distribuições, boxplots) e bivariada (matriz de correlação, scatter plots) das variáveis financeiras e de tempo. |
| `04_eda_temporal_categorical.py` | Gabriel | EDA (Segmentação) | Análise de sazonalidade (mensal), performance regional (UF/Região), mix de produtos (Categoria) e comportamento de pagamento. |
| `05_statistical_inference.py` | Leandro | Inferência Estatística | Testes de normalidade, cálculo de Intervalos de Confiança (ICs 95% para médias e proporções) e Testes de Hipóteses (t-Student, Qui-Quadrado, ANOVA). |
| `06_kpis_insights.py` | Leandro | KPIs e Insights | Cálculo de todos os KPIs solicitados, análise de elasticidade ao desconto e geração do Dashboard consolidado. |

## ⚙️ Como Reproduzir a Análise

A análise é totalmente reprodutível em qualquer ambiente Linux/macOS com Python.

### 1. Pré-requisitos

Certifique-se de ter o Python 3.11+ instalado.

### 2. Instalação e Configuração

```bash
# 1. Navegue até o diretório do projeto
cd /caminho/para/ecommerce-analytics

# 2. Crie e ative o ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

### 3. Execução Completa

O script `run_all.sh` executa todos os notebooks em sequência, garantindo que o pipeline seja seguido corretamente e que todos os arquivos de saída (dados limpos, figuras, relatórios) sejam gerados.

```bash
# Execute o script
./run_all.sh
```

### 4. Resultados

Após a execução, os principais resultados estarão disponíveis:

*   **Relatório Final:** `reports/relatorio_analitico.pdf`
*   **Dashboard de KPIs:** `figures/13_dashboard_kpis.png`
*   **Dados Limpos:** `data/ecommerce_clean.csv`

## 💡 Principais Insights para a Direção

O relatório analítico detalha 4 achados acionáveis, sendo os 3 mais relevantes:

1.  **Risco de Cancelamento em Pagamentos:** A taxa de cancelamento de pedidos com **Boleto** e **Cartão de Débito** é mais de **10 pontos percentuais** superior à de PIX e Cartão de Crédito.
2.  **Dependência de Eletrônicos:** A categoria **Eletrônicos** gera **53% da receita**, mas possui o maior desconto médio, indicando margens apertadas e alta sensibilidade ao preço.
3.  **Gargalo Logístico Regional:** A região **Nordeste** apresenta a **maior taxa de atraso (49.4%)**, sugerindo a necessidade urgente de otimização de parceiros logísticos ou infraestrutura local.
