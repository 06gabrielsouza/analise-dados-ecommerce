# 05_statistical_inference.py

import pandas as pd
from scipy import stats as st
import statsmodels.api as sm
from statsmodels.formula.api import ols

# --- Constantes ---
CAMINHO_DADOS = 'data/ecommerce_clean.csv'
NIVEL_CONFIANCA = 0.95
P_VALOR_LIMITE = 0.05

def carregar_dados(caminho):
    """Carrega os dados limpos."""
    try:
        df = pd.read_csv(caminho)
        # Converter colunas de data (ajuste o nome se necessário)
        df['data_pedido'] = pd.to_datetime(df['data_pedido'])
        print("Dados limpos carregados com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo {CAMINHO_DADOS} não encontrado.")
        print("Certifique-se de executar os scripts 01 a 04 primeiro.")
        return None

def testar_normalidade(df, coluna):
    """Testa a normalidade de uma coluna (ex: valor_pedido)."""
    print(f"\n--- Teste de Normalidade (Shapiro-Wilk) para '{coluna}' ---")
    if len(df[coluna]) > 5000:
        dados_amostra = df[coluna].sample(5000)
    else:
        dados_amostra = df[coluna]
        
    stat, p_valor = st.shapiro(dados_amostra)
    print(f"Estatística={stat:.3f}, p-valor={p_valor:.3f}")
    if p_valor > P_VALOR_LIMITE:
        print(f"Conclusão: Os dados de '{coluna}' parecem ser distribuídos normalmente.")
    else:
        print(f"Conclusão: Os dados de '{coluna}' NÃO parecem ser distribuídos normalmente.")

def calcular_ic_media(df, coluna):
    """Calcula o Intervalo de Confiança de 95% para a média."""
    print(f"\n--- IC 95% para Média de '{coluna}' ---")
    dados = df[coluna].dropna()
    media = dados.mean()
    erro_padrao = st.sem(dados)
    
    if len(dados) < 30:
        print("Aviso: Amostra pequena. O IC pode não ser confiável.")
        return

    intervalo = st.t.interval(NIVEL_CONFIANCA, len(dados)-1, loc=media, scale=erro_padrao)
    print(f"A média de '{coluna}' é ${media:.2f}.")
    print(f"O IC 95% está entre ${intervalo[0]:.2f} e ${intervalo[1]:.2f}.")

def teste_t_duas_amostras(df, coluna_grupo, grupo_a, grupo_b, coluna_valor):
    """Compara a média de duas amostras independentes (ex: PIX vs Boleto)."""
    print(f"\n--- Teste T: '{coluna_valor}' entre '{grupo_a}' vs '{grupo_b}' ---")
    
    # Assumindo que 'metodo_pagamento' é a coluna_grupo
    amostra_a = df[df[coluna_grupo] == grupo_a][coluna_valor].dropna()
    amostra_b = df[df[coluna_grupo] == grupo_b][coluna_valor].dropna()
    
    # Teste de Levene para verificar variâncias
    levene_stat, levene_p = st.levene(amostra_a, amostra_b)
    variancias_iguais = levene_p > P_VALOR_LIMITE
    
    stat, p_valor = st.ttest_ind(amostra_a, amostra_b, equal_var=variancias_iguais)
    print(f"Teste de Levene (Variâncias): p-valor={levene_p:.3f} (iguais={variancias_iguais})")
    print(f"Teste T: Estatística={stat:.3f}, p-valor={p_valor:.3f}")
    
    if p_valor < P_VALOR_LIMITE:
        print(f"Conclusão: Existe uma diferença estatisticamente significativa em '{coluna_valor}' entre {grupo_a} e {grupo_b}.")
    else:
        print(f"Conclusão: NÃO há diferença estatisticamente significativa.")

def teste_qui_quadrado(df, coluna1, coluna2):
    """Testa a associação entre duas variáveis categóricas (ex: Região e Categoria)."""
    print(f"\n--- Teste Qui-Quadrado: '{coluna1}' vs '{coluna2}' ---")
    tabela_contingencia = pd.crosstab(df[coluna1], df[coluna2])
    
    chi2, p_valor, dof, expected = st.chi2_contingency(tabela_contingencia)
    
    print(f"Estatística Chi2={chi2:.3f}, p-valor={p_valor:.3f}, Graus de Liberdade={dof}")
    if p_valor < P_VALOR_LIMITE:
        print(f"Conclusão: Existe uma associação estatisticamente significativa entre '{coluna1}' e '{coluna2}'.")
    else:
        print(f"Conclusão: NÃO há associação estatisticamente significativa.")

def teste_anova(df, coluna_categorica, coluna_valor):
    """Compara a média de 3 ou mais grupos (ex: Valor do Pedido por Região)."""
    print(f"\n--- ANOVA: '{coluna_valor}' por '{coluna_categorica}' ---")
    
    # Prepara os dados para o statsmodels
    model = ols(f'{coluna_valor} ~ C({coluna_categorica})', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    
    print(anova_table)
    p_valor = anova_table['PR(>F)'][0]
    
    if p_valor < P_VALOR_LIMITE:
        print(f"Conclusão: Existe uma diferença estatisticamente significativa em '{coluna_valor}' entre os grupos de '{coluna_categorica}'.")
    else:
        print(f"Conclusão: NÃO há diferença estatisticamente significativa.")

def main():
    df = carregar_dados(CAMINHO_DADOS)
    if df is None:
        return

    # --- Execute as Análises ---
    # (Substitua 'valor_pedido', 'metodo_pagamento', 'regiao' pelos nomes reais das colunas)
    
    # 1. Normalidade (para uma variável contínua)
    testar_normalidade(df, 'valor_pedido')

    # 2. Intervalo de Confiança (para uma variável contínua)
    calcular_ic_media(df, 'valor_pedido')
    
    # 3. Teste T (Comparar 2 grupos)
    # Ex: O valor do pedido de 'PIX' é diferente de 'Boleto'?
    teste_t_duas_amostras(df, 'metodo_pagamento', 'PIX', 'Boleto', 'valor_pedido')
    
    # 4. Qui-Quadrado (Associar 2 categorias)
    # Ex: A 'regiao' está associada ao 'status_pedido' (ex: Cancelado)?
    teste_qui_quadrado(df, 'regiao', 'status_pedido')

    # 5. ANOVA (Comparar 3+ grupos)
    # Ex: O 'valor_pedido' varia entre as 'regioes'?
    teste_anova(df, 'regiao', 'valor_pedido')

if __name__ == "__main__":
    main()