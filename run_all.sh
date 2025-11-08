#!/bin/bash
# Script para executar toda a pipeline de análise

echo "=================================================="
echo "INICIANDO PIPELINE DE ANÁLISE DE E-COMMERCE"
echo "=================================================="

cd "$(dirname "$0")/notebooks"

# Ativar ambiente virtual
source ../venv/bin/activate

echo ""
echo "[1/6] Executando limpeza de dados..."
python 01_data_cleaning.py

echo ""
echo "[2/6] Executando feature engineering..."
python 02_feature_engineering.py

echo ""
echo "[3/6] Executando análise exploratória..."
python 03_exploratory_analysis.py

echo ""
echo "[4/6] Executando análise temporal e categórica..."
python 04_eda_temporal_categorical.py

echo ""
echo "[5/6] Executando inferência estatística..."
python 05_statistical_inference.py

echo ""
echo "[6/6] Calculando KPIs e gerando insights..."
python 06_kpis_insights.py

echo ""
echo "=================================================="
echo "PIPELINE CONCLUÍDA COM SUCESSO!"
echo "=================================================="
echo ""
echo "Arquivos gerados:"
echo "  - Dados limpos: data/ecommerce_clean.csv"
echo "  - Visualizações: figures/*.png"
echo "  - Relatórios: reports/*.txt"
echo "  - Relatório final: reports/relatorio_analitico.pdf"
echo ""
