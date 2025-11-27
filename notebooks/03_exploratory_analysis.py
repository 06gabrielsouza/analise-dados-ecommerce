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
sns.set_palette('Set2')

print("="*80)
print("ANÁLISE DE DADOS - E-COMMERCE BRASILEIRO")
print("Notebook 3: Análise Exploratória de Dados (EDA)")
print("="*80)

# ============================================================================
# 1. CARREGAMENTO DOS DADOS LIMPOS
# ============================================================================
print("\n" + "="*80)
print("1. CARREGAMENTO DOS DADOS LIMPOS")
print("="*80)

df = pd.read_csv('../data/ecommerce_clean.csv')

# Reconverter datas
date_columns = ['Order_Date', 'D_Forecast', 'D_Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

print(f"✓ Dados carregados: {len(df)} registros")
print(f"✓ Período: {df['Order_Date'].min().date()} a {df['Order_Date'].max().date()}")

# ============================================================================
# 2. ANÁLISE DESCRITIVA - MEDIDAS DE TENDÊNCIA E DISPERSÃO
# ============================================================================
print("\n" + "="*80)
print("2. ANÁLISE DESCRITIVA")
print("="*80)

# Variáveis numéricas chave
key_vars = ['Total', 'Subtotal', 'P_Service', 'Discount', 'Quantity', 
            'delivery_lead_time', 'delivery_delay_days', 'freight_share']

print("\n--- Estatísticas Descritivas ---")
desc_stats = df[key_vars].describe()
print(desc_stats.round(2))

# Medidas adicionais
print("\n--- Medidas Adicionais ---")
additional_stats = pd.DataFrame({
    'Mediana': df[key_vars].median(),
    'Moda': df[key_vars].mode().iloc[0] if len(df[key_vars].mode()) > 0 else np.nan,
    'Desvio Padrão': df[key_vars].std(),
    'Coef. Variação (%)': (df[key_vars].std() / df[key_vars].mean() * 100),
    'Assimetria': df[key_vars].skew(),
    'Curtose': df[key_vars].kurtosis()
})
print(additional_stats.round(2))

# ============================================================================
# 3. ANÁLISE UNIVARIADA - DISTRIBUIÇÕES
# ============================================================================
print("\n" + "="*80)
print("3. ANÁLISE UNIVARIADA - DISTRIBUIÇÕES")
print("="*80)

# 3.1 Histogramas das variáveis principais
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Distribuição das Variáveis Principais', fontsize=16, fontweight='bold')

# Total
axes[0, 0].hist(df['Total'], bins=50, edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Total (R$)')
axes[0, 0].set_ylabel('Frequência')
axes[0, 0].set_title(f'Ticket Total\nMédia: R$ {df["Total"].mean():.2f}')
axes[0, 0].axvline(df['Total'].mean(), color='red', linestyle='--', label='Média')
axes[0, 0].axvline(df['Total'].median(), color='green', linestyle='--', label='Mediana')
axes[0, 0].legend()

# Subtotal
axes[0, 1].hist(df['Subtotal'], bins=50, edgecolor='black', alpha=0.7, color='orange')
axes[0, 1].set_xlabel('Subtotal (R$)')
axes[0, 1].set_ylabel('Frequência')
axes[0, 1].set_title(f'Subtotal\nMédia: R$ {df["Subtotal"].mean():.2f}')
axes[0, 1].axvline(df['Subtotal'].mean(), color='red', linestyle='--', label='Média')
axes[0, 1].legend()

# Frete
axes[0, 2].hist(df['P_Service'], bins=50, edgecolor='black', alpha=0.7, color='green')
axes[0, 2].set_xlabel('Frete (R$)')
axes[0, 2].set_ylabel('Frequência')
axes[0, 2].set_title(f'Valor do Frete\nMédia: R$ {df["P_Service"].mean():.2f}')
axes[0, 2].axvline(df['P_Service'].mean(), color='red', linestyle='--', label='Média')
axes[0, 2].legend()

# Desconto
axes[1, 0].hist(df['Discount']*100, bins=30, edgecolor='black', alpha=0.7, color='purple')
axes[1, 0].set_xlabel('Desconto (%)')
axes[1, 0].set_ylabel('Frequência')
axes[1, 0].set_title(f'Taxa de Desconto\nMédia: {df["Discount"].mean()*100:.2f}%')
axes[1, 0].axvline(df['Discount'].mean()*100, color='red', linestyle='--', label='Média')
axes[1, 0].legend()

# Lead time
lead_time_clean = df['delivery_lead_time'].dropna()
axes[1, 1].hist(lead_time_clean, bins=40, edgecolor='black', alpha=0.7, color='brown')
axes[1, 1].set_xlabel('Prazo de Entrega (dias)')
axes[1, 1].set_ylabel('Frequência')
axes[1, 1].set_title(f'Prazo de Entrega\nMédia: {lead_time_clean.mean():.1f} dias')
axes[1, 1].axvline(lead_time_clean.mean(), color='red', linestyle='--', label='Média')
axes[1, 1].legend()

# Delay
delay_clean = df['delivery_delay_days'].dropna()
axes[1, 2].hist(delay_clean, bins=40, edgecolor='black', alpha=0.7, color='red')
axes[1, 2].set_xlabel('Atraso (dias)')
axes[1, 2].set_ylabel('Frequência')
axes[1, 2].set_title(f'Atraso na Entrega\nMédia: {delay_clean.mean():.1f} dias')
axes[1, 2].axvline(0, color='green', linestyle='--', linewidth=2, label='No prazo')
axes[1, 2].axvline(delay_clean.mean(), color='red', linestyle='--', label='Média')
axes[1, 2].legend()

plt.tight_layout()
plt.savefig('../figures/01_distribuicoes.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 01_distribuicoes.png")
plt.close()

# 3.2 Boxplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Boxplots - Identificação de Outliers', fontsize=16, fontweight='bold')

axes[0].boxplot(df['Total'].dropna(), vert=True)
axes[0].set_ylabel('Total (R$)')
axes[0].set_title('Ticket Total')
axes[0].grid(True, alpha=0.3)

axes[1].boxplot(lead_time_clean, vert=True)
axes[1].set_ylabel('Dias')
axes[1].set_title('Prazo de Entrega')
axes[1].grid(True, alpha=0.3)

axes[2].boxplot(df['freight_share'].dropna()*100, vert=True)
axes[2].set_ylabel('Percentual (%)')
axes[2].set_title('Participação do Frete no Total')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figures/02_boxplots.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 02_boxplots.png")
plt.close()

# ============================================================================
# 4. ANÁLISE BIVARIADA E CORRELAÇÕES
# ============================================================================
print("\n" + "="*80)
print("4. ANÁLISE BIVARIADA E CORRELAÇÕES")
print("="*80)

# Matriz de correlação
numeric_cols = ['Total', 'Subtotal', 'P_Service', 'Discount', 'Quantity', 
                'delivery_lead_time', 'freight_share', 'avg_item_price']

corr_matrix = df[numeric_cols].corr()

print("\n--- Matriz de Correlação ---")
print(corr_matrix.round(3))

# Heatmap de correlação
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlação - Variáveis Numéricas', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('../figures/03_correlacao.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 03_correlacao.png")
plt.close()

# Scatter plots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Relações entre Variáveis', fontsize=16, fontweight='bold')

# Subtotal vs Total
axes[0].scatter(df['Subtotal'], df['Total'], alpha=0.5, s=20)
axes[0].set_xlabel('Subtotal (R$)')
axes[0].set_ylabel('Total (R$)')
axes[0].set_title(f'Subtotal vs Total\nCorrelação: {df["Subtotal"].corr(df["Total"]):.3f}')
axes[0].grid(True, alpha=0.3)

# Desconto vs Total
axes[1].scatter(df['Discount']*100, df['Total'], alpha=0.5, s=20, color='orange')
axes[1].set_xlabel('Desconto (%)')
axes[1].set_ylabel('Total (R$)')
axes[1].set_title(f'Desconto vs Total\nCorrelação: {df["Discount"].corr(df["Total"]):.3f}')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figures/04_scatter_plots.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 04_scatter_plots.png")
plt.close()

print("\n" + "="*80)
print("FIM DO NOTEBOOK 3 - PARTE 1")
print("="*80)