import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuração de visualização
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')

print("="*80)
print("ANÁLISE DE DADOS - E-COMMERCE BRASILEIRO")
print("Notebook 1: Limpeza e Preparação dos Dados")
print("="*80)

# ============================================================================
# 1. CARREGAMENTO E INSPEÇÃO INICIAL
# ============================================================================
print("\n" + "="*80)
print("1. CARREGAMENTO E INSPEÇÃO INICIAL DOS DADOS")
print("="*80)

# Carregar dados
df_raw = pd.read_csv('../data/ecommerce_raw.csv')

print(f"\n✓ Dados carregados: {len(df_raw)} registros")
print(f"\nDimensões: {df_raw.shape[0]} linhas × {df_raw.shape[1]} colunas")

print("\n--- Primeiras 5 linhas ---")
print(df_raw.head())

print("\n--- Informações sobre tipos de dados ---")
print(df_raw.info())

print("\n--- Estatísticas descritivas ---")
print(df_raw.describe())

print("\n--- Valores faltantes por coluna ---")
missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw)) * 100
missing_df = pd.DataFrame({
    'Missing_Count': missing,
    'Missing_Percentage': missing_pct
})
print(missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False))

# ============================================================================
# 2. TRATAMENTO DE TIPOS DE DADOS
# ============================================================================
print("\n" + "="*80)
print("2. TRATAMENTO DE TIPOS DE DADOS")
print("="*80)

# Criar cópia para trabalhar
df = df_raw.copy()

# Converter datas
date_columns = ['Order_Date', 'D_Forecast', 'D_Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    print(f"✓ Coluna '{col}' convertida para datetime")

# Garantir tipos numéricos
numeric_columns = ['Quantity', 'Subtotal', 'Discount', 'P_Service', 'Total']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    print(f"✓ Coluna '{col}' convertida para numérico")

# Trimming em strings
string_columns = ['Order_ID', 'UF', 'Region', 'Category', 'Subcategory', 
                  'Payment_Method', 'Purchase_Status', 'Services']
for col in string_columns:
    df[col] = df[col].astype(str).str.strip()
    print(f"✓ Coluna '{col}' com trimming aplicado")

print(f"\n✓ Tipos de dados corrigidos")

# ============================================================================
# 3. TRATAMENTO DE VALORES FALTANTES
# ============================================================================
print("\n" + "="*80)
print("3. TRATAMENTO DE VALORES FALTANTES")
print("="*80)

print("\n--- Valores faltantes antes do tratamento ---")
print(df.isnull().sum()[df.isnull().sum() > 0])

# D_Date: faltante para pedidos cancelados é esperado
# Para confirmados sem data, vamos usar a data prevista
mask_confirmed_no_date = (df['Purchase_Status'] == 'Confirmado') & (df['D_Date'].isnull())
df.loc[mask_confirmed_no_date, 'D_Date'] = df.loc[mask_confirmed_no_date, 'D_Forecast']
print(f"\n✓ {mask_confirmed_no_date.sum()} datas de entrega preenchidas com data prevista")

# Discount: preencher com 0 (sem desconto)
df['Discount'].fillna(0, inplace=True)
print(f"✓ Valores faltantes em 'Discount' preenchidos com 0")

# P_Service: preencher com mediana por Services
for service in df['Services'].unique():
    mask = (df['Services'] == service) & (df['P_Service'].isnull())
    median_freight = df[df['Services'] == service]['P_Service'].median()
    df.loc[mask, 'P_Service'] = median_freight
    if mask.sum() > 0:
        print(f"✓ {mask.sum()} valores de frete preenchidos para '{service}' com mediana: R$ {median_freight:.2f}")

print("\n--- Valores faltantes após tratamento ---")
remaining_missing = df.isnull().sum()[df.isnull().sum() > 0]
if len(remaining_missing) == 0:
    print("✓ Nenhum valor faltante restante!")
else:
    print(remaining_missing)

# ============================================================================
# 4. REMOÇÃO DE DUPLICATAS
# ============================================================================
print("\n" + "="*80)
print("4. REMOÇÃO DE DUPLICATAS")
print("="*80)

print(f"\nRegistros antes: {len(df)}")

# Verificar duplicatas por Order_ID
duplicates = df[df.duplicated(subset=['Order_ID'], keep=False)]
print(f"Duplicatas encontradas: {len(duplicates)}")

if len(duplicates) > 0:
    print("\n--- Exemplo de duplicatas ---")
    print(duplicates.head(10)[['Order_ID', 'Order_Date', 'Total', 'Purchase_Status']])
    
    # Remover duplicatas mantendo a primeira ocorrência
    df = df.drop_duplicates(subset=['Order_ID'], keep='first')
    print(f"\n✓ Duplicatas removidas")

print(f"Registros após remoção: {len(df)}")

# Salvar checkpoint
df.to_csv('../data/ecommerce_cleaned_checkpoint.csv', index=False)
print("\n✓ Checkpoint salvo: ecommerce_cleaned_checkpoint.csv")

print("\n" + "="*80)
print("FIM DO NOTEBOOK 1")
print("="*80)