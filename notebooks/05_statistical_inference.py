"""
Notebook 5: Inferência Estatística
E-commerce Analytics Project

Este notebook realiza:
1. Testes de normalidade
2. Intervalos de confiança para médias
3. Intervalos de confiança para proporções
4. Testes de hipóteses
5. Análise de significância estatística
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, t, shapiro, kstest, normaltest
import warnings
warnings.filterwarnings('ignore')

# Configuração de visualização
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')

print("="*80)
print("ANÁLISE DE DADOS - E-COMMERCE BRASILEIRO")
print("Notebook 5: Inferência Estatística")
print("="*80)

# ============================================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================================
print("\n" + "="*80)
print("1. CARREGAMENTO DOS DADOS")
print("="*80)

df = pd.read_csv('../data/ecommerce_clean.csv')

# Reconverter datas
date_columns = ['Order_Date', 'D_Forecast', 'D_Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

print(f"✓ Dados carregados: {len(df)} registros")

# ============================================================================
# 2. TESTES DE NORMALIDADE
# ============================================================================
print("\n" + "="*80)
print("2. TESTES DE NORMALIDADE")
print("="*80)

# Variáveis para testar
variables_to_test = ['Total', 'Subtotal', 'P_Service', 'delivery_lead_time', 
                     'delivery_delay_days', 'freight_share']

normality_results = []

for var in variables_to_test:
    data = df[var].dropna()
    
    # Shapiro-Wilk Test (melhor para n < 5000)
    if len(data) <= 5000:
        stat_shapiro, p_shapiro = shapiro(data)
    else:
        stat_shapiro, p_shapiro = np.nan, np.nan
    
    # D'Agostino-Pearson Test
    stat_dagostino, p_dagostino = normaltest(data)
    
    # Kolmogorov-Smirnov Test
    stat_ks, p_ks = kstest(data, 'norm', args=(data.mean(), data.std()))
    
    normality_results.append({
        'Variable': var,
        'N': len(data),
        'Shapiro_Stat': stat_shapiro,
        'Shapiro_p': p_shapiro,
        'DAgostino_Stat': stat_dagostino,
        'DAgostino_p': p_dagostino,
        'KS_Stat': stat_ks,
        'KS_p': p_ks,
        'Normal': 'Sim' if p_dagostino > 0.05 else 'Não'
    })

normality_df = pd.DataFrame(normality_results)
print("\n--- Testes de Normalidade ---")
print("Hipótese nula (H0): Os dados seguem distribuição normal")
print("Nível de significância: α = 0.05")
print("\n" + normality_df.to_string(index=False))

# Q-Q Plots
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Q-Q Plots - Verificação de Normalidade', fontsize=16, fontweight='bold')

for idx, var in enumerate(variables_to_test):
    row = idx // 3
    col = idx % 3
    data = df[var].dropna()
    
    stats.probplot(data, dist="norm", plot=axes[row, col])
    axes[row, col].set_title(f'{var}\n(n={len(data)})')
    axes[row, col].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figures/10_qq_plots.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico salvo: 10_qq_plots.png")
plt.close()

# ============================================================================
# 3. INTERVALOS DE CONFIANÇA PARA MÉDIAS
# ============================================================================
print("\n" + "="*80)
print("3. INTERVALOS DE CONFIANÇA PARA MÉDIAS (95%)")
print("="*80)

def calculate_ci_mean(data, confidence=0.95):
    """Calcula intervalo de confiança para média"""
    data_clean = data.dropna()
    n = len(data_clean)
    mean = data_clean.mean()
    std_err = stats.sem(data_clean)
    
    # Usar distribuição t para amostras
    ci = stats.t.interval(confidence, n-1, loc=mean, scale=std_err)
    
    margin = ci[1] - mean
    
    return {
        'n': n,
        'mean': mean,
        'std': data_clean.std(),
        'std_err': std_err,
        'ci_lower': ci[0],
        'ci_upper': ci[1],
        'margin': margin
    }

# Variáveis de interesse
mean_variables = {
    'Total': 'Ticket Total (R$)',
    'Subtotal': 'Subtotal (R$)',
    'P_Service': 'Frete (R$)',
    'Discount': 'Desconto (%)',
    'delivery_lead_time': 'Prazo de Entrega (dias)',
    'delivery_delay_days': 'Atraso (dias)',
    'freight_share': 'Participação Frete (%)'
}

ci_mean_results = []

for var, label in mean_variables.items():
    if var in ['Discount', 'freight_share']:
        data = df[var] * 100  # Converter para percentual
    else:
        data = df[var]
    
    ci_result = calculate_ci_mean(data)
    ci_result['Variable'] = label
    ci_mean_results.append(ci_result)

ci_mean_df = pd.DataFrame(ci_mean_results)
ci_mean_df = ci_mean_df[['Variable', 'n', 'mean', 'std', 'ci_lower', 'ci_upper', 'margin']]

print("\n--- Intervalos de Confiança para Médias (95%) ---")
print(ci_mean_df.round(2).to_string(index=False))

# Visualização dos ICs
fig, ax = plt.subplots(figsize=(14, 8))

y_pos = np.arange(len(ci_mean_df))
means = ci_mean_df['mean'].values
ci_lower = ci_mean_df['ci_lower'].values
ci_upper = ci_mean_df['ci_upper'].values
errors = [means - ci_lower, ci_upper - means]

ax.barh(y_pos, means, xerr=errors, align='center', alpha=0.7, 
        ecolor='black', capsize=5, color='steelblue')
ax.set_yticks(y_pos)
ax.set_yticklabels(ci_mean_df['Variable'])
ax.set_xlabel('Valor')
ax.set_title('Intervalos de Confiança (95%) para Médias', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('../figures/11_ic_medias.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico salvo: 11_ic_medias.png")
plt.close()

# ============================================================================
# 4. INTERVALOS DE CONFIANÇA PARA PROPORÇÕES
# ============================================================================
print("\n" + "="*80)
print("4. INTERVALOS DE CONFIANÇA PARA PROPORÇÕES (95%)")
print("="*80)

def calculate_ci_proportion(successes, n, confidence=0.95):
    """Calcula intervalo de confiança para proporção"""
    p = successes / n
    z = norm.ppf((1 + confidence) / 2)
    
    # Intervalo de confiança de Wilson
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2*n)) / denominator
    adjustment = z * np.sqrt((p*(1-p) + z**2/(4*n)) / n) / denominator
    
    ci_lower = centre - adjustment
    ci_upper = centre + adjustment
    
    return {
        'n': n,
        'successes': successes,
        'proportion': p,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'margin': adjustment
    }

# Proporções de interesse
n_total = len(df)
n_confirmed = len(df[df['is_confirmed'] == 1])

# Taxa de confirmação
ci_confirmed = calculate_ci_proportion(df['is_confirmed'].sum(), n_total)

# Taxa de atraso (apenas pedidos confirmados)
df_confirmed = df[df['is_confirmed'] == 1]
n_confirmed_total = len(df_confirmed)
n_late = df_confirmed['is_late'].sum()
ci_late = calculate_ci_proportion(n_late, n_confirmed_total)

# Taxa de confirmação por método de pagamento
payment_ci_results = []
for payment in df['Payment_Method'].unique():
    df_payment = df[df['Payment_Method'] == payment]
    n_payment = len(df_payment)
    n_payment_confirmed = df_payment['is_confirmed'].sum()
    
    ci_payment = calculate_ci_proportion(n_payment_confirmed, n_payment)
    ci_payment['Payment_Method'] = payment
    payment_ci_results.append(ci_payment)

payment_ci_df = pd.DataFrame(payment_ci_results)

print("\n--- Taxa de Confirmação Geral ---")
print(f"Proporção: {ci_confirmed['proportion']*100:.2f}%")
print(f"IC 95%: [{ci_confirmed['ci_lower']*100:.2f}%, {ci_confirmed['ci_upper']*100:.2f}%]")
print(f"Margem de erro: ±{ci_confirmed['margin']*100:.2f}%")

print("\n--- Taxa de Atraso (Pedidos Confirmados) ---")
print(f"Proporção: {ci_late['proportion']*100:.2f}%")
print(f"IC 95%: [{ci_late['ci_lower']*100:.2f}%, {ci_late['ci_upper']*100:.2f}%]")
print(f"Margem de erro: ±{ci_late['margin']*100:.2f}%")

print("\n--- Taxa de Confirmação por Método de Pagamento ---")
payment_ci_display = payment_ci_df[['Payment_Method', 'n', 'proportion', 'ci_lower', 'ci_upper']]
payment_ci_display['proportion'] = (payment_ci_display['proportion'] * 100).round(2)
payment_ci_display['ci_lower'] = (payment_ci_display['ci_lower'] * 100).round(2)
payment_ci_display['ci_upper'] = (payment_ci_display['ci_upper'] * 100).round(2)
print(payment_ci_display.to_string(index=False))

# Visualização
fig, ax = plt.subplots(figsize=(12, 6))

y_pos = np.arange(len(payment_ci_df))
proportions = payment_ci_df['proportion'].values * 100
ci_lower = payment_ci_df['ci_lower'].values * 100
ci_upper = payment_ci_df['ci_upper'].values * 100
errors = [proportions - ci_lower, ci_upper - proportions]

ax.barh(y_pos, proportions, xerr=errors, align='center', alpha=0.7,
        ecolor='black', capsize=5, color='mediumseagreen')
ax.set_yticks(y_pos)
ax.set_yticklabels(payment_ci_df['Payment_Method'])
ax.set_xlabel('Taxa de Confirmação (%)')
ax.set_title('IC 95% - Taxa de Confirmação por Método de Pagamento', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim(70, 100)

plt.tight_layout()
plt.savefig('../figures/12_ic_proporcoes.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico salvo: 12_ic_proporcoes.png")
plt.close()

# ============================================================================
# 5. TESTES DE HIPÓTESES
# ============================================================================
print("\n" + "="*80)
print("5. TESTES DE HIPÓTESES")
print("="*80)

# 5.1 Teste t: Ticket médio por região (Sudeste vs outras)
print("\n--- Teste t: Ticket Médio Sudeste vs Outras Regiões ---")

df_sudeste = df[df['Region'] == 'Sudeste']['Total']
df_outras = df[df['Region'] != 'Sudeste']['Total']

t_stat, p_value = stats.ttest_ind(df_sudeste, df_outras)

print(f"Média Sudeste: R$ {df_sudeste.mean():.2f}")
print(f"Média Outras: R$ {df_outras.mean():.2f}")
print(f"Estatística t: {t_stat:.4f}")
print(f"P-valor: {p_value:.4f}")
print(f"Conclusão: {'Diferença significativa' if p_value < 0.05 else 'Sem diferença significativa'} (α=0.05)")

# 5.2 Teste qui-quadrado: Taxa de confirmação vs Método de Pagamento
print("\n--- Teste Qui-Quadrado: Confirmação vs Método de Pagamento ---")

contingency_table = pd.crosstab(df['Payment_Method'], df['Purchase_Status'])
chi2, p_chi, dof, expected = stats.chi2_contingency(contingency_table)

print("\nTabela de Contingência:")
print(contingency_table)
print(f"\nEstatística χ²: {chi2:.4f}")
print(f"P-valor: {p_chi:.6f}")
print(f"Graus de liberdade: {dof}")
print(f"Conclusão: {'Associação significativa' if p_chi < 0.05 else 'Sem associação significativa'} (α=0.05)")

# 5.3 ANOVA: Ticket médio por categoria
print("\n--- ANOVA: Ticket Médio por Categoria ---")

categories = df['Category'].unique()
category_groups = [df[df['Category'] == cat]['Total'].values for cat in categories]

f_stat, p_anova = stats.f_oneway(*category_groups)

print(f"Estatística F: {f_stat:.4f}")
print(f"P-valor: {p_anova:.6f}")
print(f"Conclusão: {'Diferenças significativas entre categorias' if p_anova < 0.05 else 'Sem diferenças significativas'} (α=0.05)")

# Médias por categoria
print("\nMédias por Categoria:")
for cat in categories:
    mean_cat = df[df['Category'] == cat]['Total'].mean()
    print(f"  {cat}: R$ {mean_cat:.2f}")

# Salvar resultados
inference_summary = {
    'Normalidade': normality_df,
    'IC_Medias': ci_mean_df,
    'IC_Proporcoes_Pagamento': payment_ci_display,
    'Teste_t_Sudeste': {
        'Media_Sudeste': df_sudeste.mean(),
        'Media_Outras': df_outras.mean(),
        't_statistic': t_stat,
        'p_value': p_value
    },
    'Qui_Quadrado': {
        'chi2': chi2,
        'p_value': p_chi,
        'dof': dof
    },
    'ANOVA_Categoria': {
        'F_statistic': f_stat,
        'p_value': p_anova
    }
}

# Salvar em arquivo
with open('../reports/inference_summary.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RESUMO DE INFERÊNCIA ESTATÍSTICA\n")
    f.write("="*80 + "\n\n")
    
    f.write("1. INTERVALOS DE CONFIANÇA PARA MÉDIAS (95%)\n")
    f.write("-"*80 + "\n")
    f.write(ci_mean_df.round(2).to_string(index=False) + "\n\n")
    
    f.write("2. TAXA DE CONFIRMAÇÃO GERAL\n")
    f.write("-"*80 + "\n")
    f.write(f"Proporção: {ci_confirmed['proportion']*100:.2f}%\n")
    f.write(f"IC 95%: [{ci_confirmed['ci_lower']*100:.2f}%, {ci_confirmed['ci_upper']*100:.2f}%]\n\n")
    
    f.write("3. TAXA DE ATRASO (PEDIDOS CONFIRMADOS)\n")
    f.write("-"*80 + "\n")
    f.write(f"Proporção: {ci_late['proportion']*100:.2f}%\n")
    f.write(f"IC 95%: [{ci_late['ci_lower']*100:.2f}%, {ci_late['ci_upper']*100:.2f}%]\n\n")

print("\n✓ Resumo de inferência salvo: inference_summary.txt")

print("\n" + "="*80)
print("FIM DO NOTEBOOK 5")
print("="*80)
