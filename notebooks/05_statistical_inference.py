import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("NOTEBOOK 5: CORRIGIDO")
print("="*80)

df = pd.read_csv('../data/ecommerce_clean.csv')

# 1. Normalidade (Só para variáveis com variância)
print("\n--- Teste de Normalidade (Shapiro-Wilk) ---")
coluna_teste = 'Total'
stat, p = stats.shapiro(df[coluna_teste].sample(min(len(df), 500)))
print(f"Variável: {coluna_teste} | P-valor: {p:.5f}")
if p < 0.05: print("Conclusão: Não é normal.")
else: print("Conclusão: É normal.")

# 2. IC Médias
media = df['Total'].mean()
erro = stats.sem(df['Total'])
ic = stats.t.interval(0.95, len(df)-1, loc=media, scale=erro)
print(f"\nTicket Médio: R$ {media:.2f}")
print(f"IC 95%: {ic}")

# 3. ANOVA (CORREÇÃO AQUI: Verifica se há categorias suficientes)
print("\n--- ANOVA: Ticket Médio por Categoria ---")
categorias = df['Category'].unique()

if len(categorias) < 2:
    print(f"⚠️ AVISO: Apenas 1 categoria encontrada ({categorias[0]}).")
    print("Não é possível realizar ANOVA (comparação entre grupos) com apenas um grupo.")
else:
    grupos = [df[df['Category'] == cat]['Total'] for cat in categorias]
    f_val, p_val = stats.f_oneway(*grupos)
    print(f"P-valor: {p_val:.5f}")

# Salvar gráfico simples de IC
plt.figure(figsize=(6, 4))
plt.bar(['Ticket Médio'], [media], yerr=[media - ic[0]], capsize=10, color='skyblue')
plt.title('Intervalo de Confiança 95% - Ticket Médio')
plt.savefig('../figures/11_ic_medias.png')
print("\n✓ Gráfico IC salvo.")

# Salvar resumo vazio para não quebrar fluxo
with open('../reports/inference_summary.txt', 'w') as f:
    f.write(f"Ticket Medio: {media}\nIC: {ic}\n")