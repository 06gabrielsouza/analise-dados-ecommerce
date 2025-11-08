"""
Notebook 2: Detecção de Outliers e Feature Engineering
E-commerce Analytics Project

Este notebook realiza:
1. Detecção e tratamento de outliers
2. Feature Engineering (criação de novas variáveis)
3. Validação de integridade dos dados
4. Exportação dos dados limpos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuração de visualização
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')

print("="*80)
print("ANÁLISE DE DADOS - E-COMMERCE BRASILEIRO")
print("Notebook 2: Outliers e Feature Engineering")
print("="*80)

# ============================================================================
# 1. CARREGAMENTO DO CHECKPOINT
# ============================================================================
print("\n" + "="*80)
print("1. CARREGAMENTO DO CHECKPOINT")
print("="*80)

df = pd.read_csv('../data/ecommerce_cleaned_checkpoint.csv')

# Reconverter datas
date_columns = ['Order_Date', 'D_Forecast', 'D_Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

print(f"✓ Dados carregados: {len(df)} registros")

# ============================================================================
# 2. DETECÇÃO E TRATAMENTO DE OUTLIERS
# ============================================================================
print("\n" + "="*80)
print("2. DETECÇÃO E TRATAMENTO DE OUTLIERS")
print("="*80)

def detect_outliers_iqr(data, column, multiplier=1.5):
    """Detecta outliers usando método IQR"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    outliers = (data[column] < lower_bound) | (data[column] > upper_bound)
    return outliers, lower_bound, upper_bound

def detect_outliers_zscore(data, column, threshold=3):
    """Detecta outliers usando Z-score"""
    z_scores = np.abs(stats.zscore(data[column].dropna()))
    outliers_idx = data[column].dropna().index[z_scores > threshold]
    outliers = data.index.isin(outliers_idx)
    return outliers

# Analisar outliers em variáveis numéricas chave
numeric_vars = ['Total', 'Subtotal', 'P_Service', 'Quantity']

outlier_summary = []

for var in numeric_vars:
    print(f"\n--- Análise de outliers: {var} ---")
    
    # IQR
    outliers_iqr, lower, upper = detect_outliers_iqr(df, var)
    n_outliers_iqr = outliers_iqr.sum()
    
    # Z-score
    outliers_z = detect_outliers_zscore(df, var)
    n_outliers_z = outliers_z.sum()
    
    print(f"Outliers (IQR): {n_outliers_iqr} ({n_outliers_iqr/len(df)*100:.2f}%)")
    print(f"Outliers (Z-score): {n_outliers_z} ({n_outliers_z/len(df)*100:.2f}%)")
    print(f"Range IQR: [{lower:.2f}, {upper:.2f}]")
    print(f"Min: {df[var].min():.2f}, Max: {df[var].max():.2f}")
    
    outlier_summary.append({
        'Variable': var,
        'Outliers_IQR': n_outliers_iqr,
        'Outliers_IQR_Pct': n_outliers_iqr/len(df)*100,
        'Outliers_Zscore': n_outliers_z,
        'Lower_Bound': lower,
        'Upper_Bound': upper
    })

# Criar DataFrame de resumo
outlier_df = pd.DataFrame(outlier_summary)
print("\n--- Resumo de Outliers ---")
print(outlier_df)

# Tratamento: remover outliers extremos (Z-score > 3)
print("\n--- Tratamento de Outliers ---")
initial_count = len(df)

# Combinar outliers de todas as variáveis
outliers_mask = pd.Series(False, index=df.index)
for var in numeric_vars:
    outliers_mask |= detect_outliers_zscore(df, var, threshold=3)

print(f"Total de registros com outliers extremos: {outliers_mask.sum()}")

# Remover outliers
df_clean = df[~outliers_mask].copy()
print(f"Registros removidos: {initial_count - len(df_clean)}")
print(f"Registros restantes: {len(df_clean)}")

# ============================================================================
# 3. FEATURE ENGINEERING
# ============================================================================
print("\n" + "="*80)
print("3. FEATURE ENGINEERING")
print("="*80)

# 3.1 Variáveis de tempo
print("\n--- Criando variáveis de tempo ---")

# Delivery lead time (tempo total de entrega)
df_clean['delivery_lead_time'] = (df_clean['D_Date'] - df_clean['Order_Date']).dt.days
df_clean.loc[df_clean['Purchase_Status'] == 'Cancelado', 'delivery_lead_time'] = np.nan
print("✓ delivery_lead_time: dias entre pedido e entrega")

# Delivery delay (atraso em relação à previsão)
df_clean['delivery_delay_days'] = (df_clean['D_Date'] - df_clean['D_Forecast']).dt.days
df_clean.loc[df_clean['Purchase_Status'] == 'Cancelado', 'delivery_delay_days'] = np.nan
print("✓ delivery_delay_days: diferença entre entrega real e prevista")

# Flag de atraso
df_clean['is_late'] = (df_clean['delivery_delay_days'] > 0).astype(int)
df_clean.loc[df_clean['Purchase_Status'] == 'Cancelado', 'is_late'] = np.nan
print("✓ is_late: indicador binário de atraso")

# 3.2 Variáveis de status
print("\n--- Criando variáveis de status ---")

# Flag de confirmação
df_clean['is_confirmed'] = (df_clean['Purchase_Status'] == 'Confirmado').astype(int)
print("✓ is_confirmed: indicador de pedido confirmado")

# 3.3 Variáveis financeiras
print("\n--- Criando variáveis financeiras ---")

# Participação do frete no total
df_clean['freight_share'] = df_clean['P_Service'] / df_clean['Total']
print("✓ freight_share: proporção do frete no valor total")

# Desconto absoluto
df_clean['discount_abs'] = df_clean['Discount'] * df_clean['Subtotal']
print("✓ discount_abs: valor absoluto do desconto em R$")

# Ticket médio por item
df_clean['avg_item_price'] = df_clean['Subtotal'] / df_clean['Quantity']
print("✓ avg_item_price: preço médio por item")

# 3.4 Variáveis temporais
print("\n--- Criando variáveis temporais ---")

df_clean['order_year'] = df_clean['Order_Date'].dt.year
df_clean['order_month'] = df_clean['Order_Date'].dt.month
df_clean['order_month_name'] = df_clean['Order_Date'].dt.month_name()
df_clean['order_quarter'] = df_clean['Order_Date'].dt.quarter
df_clean['order_dayofweek'] = df_clean['Order_Date'].dt.dayofweek
df_clean['order_dayname'] = df_clean['Order_Date'].dt.day_name()

print("✓ Variáveis de ano, mês, trimestre e dia da semana criadas")

# ============================================================================
# 4. VALIDAÇÃO DE INTEGRIDADE
# ============================================================================
print("\n" + "="*80)
print("4. VALIDAÇÃO DE INTEGRIDADE DOS DADOS")
print("="*80)

# Verificar consistência de cálculos
print("\n--- Verificando consistência de valores ---")

# Total = Subtotal * (1 - Discount) + P_Service
df_clean['total_calculated'] = df_clean['Subtotal'] * (1 - df_clean['Discount']) + df_clean['P_Service']
df_clean['total_diff'] = abs(df_clean['Total'] - df_clean['total_calculated'])

inconsistent = df_clean[df_clean['total_diff'] > 0.1]
print(f"Registros com inconsistência no Total: {len(inconsistent)}")

if len(inconsistent) > 0:
    print("⚠ Corrigindo valores de Total...")
    df_clean['Total'] = df_clean['total_calculated']
    print("✓ Valores corrigidos")

df_clean.drop(['total_calculated', 'total_diff'], axis=1, inplace=True)

# Verificar valores negativos
print("\n--- Verificando valores negativos ---")
for col in ['Subtotal', 'Total', 'P_Service', 'Quantity']:
    negative = (df_clean[col] < 0).sum()
    if negative > 0:
        print(f"⚠ {col}: {negative} valores negativos encontrados")
    else:
        print(f"✓ {col}: sem valores negativos")

# Verificar unicidade de Order_ID
print("\n--- Verificando unicidade de Order_ID ---")
duplicates = df_clean['Order_ID'].duplicated().sum()
if duplicates == 0:
    print("✓ Todos os Order_ID são únicos")
else:
    print(f"⚠ {duplicates} Order_ID duplicados encontrados")

# ============================================================================
# 5. EXPORTAÇÃO DOS DADOS LIMPOS
# ============================================================================
print("\n" + "="*80)
print("5. EXPORTAÇÃO DOS DADOS LIMPOS")
print("="*80)

# Salvar dados limpos
df_clean.to_csv('../data/ecommerce_clean.csv', index=False)
print("✓ Dados limpos salvos: ecommerce_clean.csv")

# Resumo final
print("\n--- RESUMO FINAL ---")
print(f"Registros originais: {len(df)}")
print(f"Registros após limpeza: {len(df_clean)}")
print(f"Registros removidos: {len(df) - len(df_clean)}")
print(f"Colunas originais: {df.shape[1]}")
print(f"Colunas após feature engineering: {df_clean.shape[1]}")
print(f"Novas features criadas: {df_clean.shape[1] - df.shape[1]}")

print("\n--- Novas features criadas ---")
new_features = ['delivery_lead_time', 'delivery_delay_days', 'is_late', 'is_confirmed',
                'freight_share', 'discount_abs', 'avg_item_price', 'order_year', 
                'order_month', 'order_month_name', 'order_quarter', 'order_dayofweek', 
                'order_dayname']
for i, feat in enumerate(new_features, 1):
    print(f"{i}. {feat}")

print("\n" + "="*80)
print("FIM DO NOTEBOOK 2")
print("="*80)
