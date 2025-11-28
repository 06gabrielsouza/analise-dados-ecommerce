# Relatório de Análise de Dados – E-commerce Brasileiro

**Autores:** Gabriel dos Santos Souza e Leandro de Morais
**Turma:** 3º Período - ADS Embarque Digital
**Data:** 08 de Novembro de 2025

---

## 1. Sumário Executivo

### Divisão de Responsabilidades

Para a execução deste projeto, as responsabilidades foram divididas da seguinte forma:

| Membro da Equipe | Responsabilidades Principais | Notebooks/Fases |
| :--- | :--- | :--- |
| **Gabriel dos Santos Souza** | Limpeza de Dados, Feature Engineering, Análise Exploratória (EDA) | `01_data_cleaning.py`, `02_feature_engineering.py`, `03_exploratory_analysis.py`, `04_eda_temporal_categorical.py` |
| **Leandro de Morais** | Inferência Estatística, Cálculo de KPIs, Geração de Insights, Relatório Analítico | `05_statistical_inference.py`, `06_kpis_insights.py`, Relatório Analítico, README |


| **Leandro de Morais** | Inferência Estatística, Cálculo de KPIs, Geração de Insights, Relatório Analítico |

Este relatório apresenta uma análise aprofundada dos dados de vendas de um e-commerce brasileiro, cobrindo o período de janeiro a outubro de 2024. A análise resultou em insights acionáveis para a direção, com foco em otimização de receita, performance logística e comportamento do cliente. Os principais achados são:

1.  **Otimização de Pagamentos é Crucial para a Receita:** A taxa de cancelamento de pedidos realizados com **Boleto (18.6%)** e **Cartão de Débito (18.7%)** é significativamente mais alta que a de **Cartão de Crédito (8.4%)** e **PIX (8.8%)**. Uma campanha para incentivar o uso de PIX e crédito, ou um sistema de lembretes para pagamento de boletos, poderia recuperar uma parcela significativa da receita perdida.

2.  **Eletrônicos Dominam a Receita, mas com Margens Apertadas:** A categoria de **Eletrônicos** representa **53% da receita total**, impulsionada por um ticket médio altíssimo (R$ 2.762). No entanto, a categoria também possui a maior média de desconto (5.1%), sugerindo uma sensibilidade ao preço. Estratégias de cross-selling com produtos de margem maior, como acessórios, podem aumentar a lucratividade.

3.  **Performance Logística Regional Apresenta Desafios:** A região **Nordeste** registra a **maior taxa de atraso (49.4%)** e o segundo maior custo de frete médio (R$ 36.43), atrás apenas da região Norte. Isso indica gargalos logísticos que podem estar impactando a satisfação do cliente e a recompra. Uma revisão dos parceiros logísticos ou a implementação de um centro de distribuição local são ações recomendadas.

4.  **Sazonalidade de Vendas é Moderada, mas Relevante:** As vendas apresentam um pico em **Março**, tanto em volume de pedidos quanto em receita. Compreender os fatores por trás dessa alta (ex: datas comemorativas, comportamento do consumidor pós-férias) pode permitir a replicação de estratégias bem-sucedidas em outros meses do ano.

---

## 2. Dados e Metodologia

### 2.1. Fonte e Estrutura dos Dados

Para esta análise, foi utilizado um conjunto de dados sintético, gerado para simular as operações de um e-commerce brasileiro com 5.000 pedidos iniciais. O dataset contém informações detalhadas sobre pedidos, clientes, produtos, pagamentos e entregas. As principais colunas incluem:

*   **Identificadores:** `Order_ID`
*   **Datas:** `Order_Date`, `D_Forecast` (previsão), `D_Date` (real)
*   **Geografia:** `UF`, `Region`
*   **Produto:** `Category`, `Subcategory`
*   **Valores:** `Subtotal`, `Discount`, `P_Service` (frete), `Total`
*   **Status:** `Payment_Method`, `Purchase_Status`, `Services`

### 2.2. Preparação e Limpeza dos Dados

O dataset bruto passou por um rigoroso processo de limpeza e preparação para garantir a qualidade e a confiabilidade da análise. As seguintes etapas foram executadas:

1.  **Tratamento de Tipos:** As colunas de data foram convertidas para o formato `datetime`, e as colunas numéricas foram ajustadas para `float` ou `int`.
2.  **Valores Faltantes:** Valores ausentes em `Discount` foram preenchidos com 0 (assumindo ausência de desconto). Em `P_Service` (frete), foram imputados com a mediana do respectivo tipo de serviço. Datas de entrega (`D_Date`) ausentes em pedidos confirmados foram preenchidas com a data prevista para permitir a análise de atraso.
3.  **Remoção de Duplicatas:** Foram identificados e removidos 50 registros duplicados baseados no `Order_ID`, mantendo-se a primeira ocorrência.
4.  **Tratamento de Outliers e Robustez Estatística:** Outliers em variáveis financeiras (`Total`, `Subtotal`, `P_Service`) foram identificados e tratados para evitar a distorção das análises de tendência central e, principalmente, dos testes de inferência subsequentes.

    Utilizamos o método **Z-score** com um limiar de **3 desvios-padrão** para identificar valores extremos. Este método é adequado para dados que, embora não sejam estritamente normais, possuem uma distribuição unimodal e simétrica o suficiente para que valores muito distantes da média sejam considerados anômalos.

    A remoção de **364 registros** (aproximadamente 7.3% do *dataset* inicial) foi uma decisão metodológica para garantir a **robustez** dos Intervalos de Confiança (ICs) e dos testes de hipóteses (ANOVA), que são sensíveis a valores extremos. Os *outliers* removidos representam transações atípicas que, se mantidas, poderiam inflacionar artificialmente a média e o desvio-padrão, comprometendo a generalização dos resultados para a população de pedidos.

Após a limpeza, o dataset final ficou com **4.636 registros**.

### 2.3. Feature Engineering

Novas variáveis foram criadas para aprofundar a análise e permitir o cálculo de KPIs complexos:

*   `delivery_lead_time`: Tempo total entre a data do pedido e a data da entrega.
*   `delivery_delay_days`: Diferença em dias entre a entrega real e a prevista.
*   `is_late`: Flag binário (1/0) que indica se um pedido atrasou.
*   `is_confirmed`: Flag binário (1/0) que indica se o pagamento foi confirmado.
*   `freight_share`: Proporção do valor do frete em relação ao total do pedido.
*   `discount_abs`: Valor absoluto do desconto em Reais.

---

## 3. Análise Exploratória de Dados (EDA)

### 3.1. Distribuições e Medidas de Tendência

A análise das principais variáveis numéricas revela uma forte assimetria à direita, comum em dados financeiros. A média do **Ticket Total** é de **R$ 952,86**, enquanto a mediana é de R$ 497,78, indicando que um menor número de pedidos de alto valor eleva a média geral.

| Métrica               | Ticket Total | Prazo de Entrega (dias) | Atraso (dias) | Desconto (%) |
| --------------------- | ------------ | ----------------------- | ------------- | ------------ |
| **Média**             | R$ 952,86    | 10.1                    | 2.9           | 4.0%         |
| **Mediana**           | R$ 497,78    | 9.0                     | 1.0           | 0.0%         |
| **Desvio Padrão**     | R$ 1.229,15  | 6.9                     | 4.9           | 5.5%         |
| **Mínimo**            | R$ 21,54     | 0                       | -7.0          | 0.0%         |
| **Máximo**            | R$ 7.844,19  | 33                      | 21            | 20.0%        |

![Distribuições das Variáveis Principais](../figures/01_distribuicoes.png)
*Figura 1: Histogramas de Ticket Total, Prazo de Entrega e Atraso.*

### 3.2. Análise de Correlações

A matriz de correlação mostra, como esperado, uma correlação quase perfeita entre `Subtotal` e `Total` (0.97). Uma correlação negativa fraca entre `Discount` e `Total` (-0.11) sugere que descontos maiores não necessariamente levam a um aumento do ticket total, podendo estar associados a produtos de menor valor.

![Matriz de Correlação](../figures/03_correlacao.png)
*Figura 2: Heatmap de correlação entre as principais variáveis numéricas.*

### 3.3. Análise Categórica

**Receita por Categoria:** A categoria de **Eletrônicos** é a principal fonte de receita, seguida por **Casa e Decoração**. Livros, apesar de terem um alto volume de pedidos, contribuem com a menor parcela da receita devido ao baixo ticket médio.

![Análise por Categoria](https://private-us-east-1.manuscdn.com/sessionFile/QZFEkxQOHKeamYWLo4fQ3z/sandbox/H57AvMkVReQI51ldYykAE6-images_1764336169594_na1fn_L2hvbWUvdWJ1bnR1L2FuYWxpc2UtZGFkb3MtZWNvbW1lcmNlL2ZpZ3VyZXMvMDdfYW5hbGlzZV9jYXRlZ29yaWE.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUVpGRWt4UU9IS2VhbVlXTG80ZlEzei9zYW5kYm94L0g1N0F2TWtWUmVRSTUxbGRZeWtBRTYtaW1hZ2VzXzE3NjQzMzYxNjk1OTRfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyRnVZV3hwYzJVdFpHRmtiM010WldOdmJXMWxjbU5sTDJacFozVnlaWE12TURkZllXNWhiR2x6WlY5allYUmxaMjl5YVdFLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=XP5UTRPsbBRV2GLs7~plty~R1DZHhxfI2ZvqG6xYNueTDwK40r4hR4vanBDk0fIDHAYUrJ-vvh1~kpffifCMyafTPiWvf2-YSrnSaABpL7h-IyksVp9Q6QPM7-GwROp9rV-GmeKtVAPG~gWMeKnh45o70FkczAuxxFpEynVT8mtI~vVU70CdeTTvM2TMyvh6lensiL4OpIa08UkyR9Xfvq-KTCmZoX8or3CQkLMJrSqK2v0vE-oGdUi9FyDivoS4O3epYnV19lTHhBlTf0C5Py6uVO462cY2YGeb5OjyxPmnFj6NFYbLsSQcE-ieWzkoY6ZaGegVzb6OCdl6VxUv9Q__)
*Figura 3: Análise de Receita, Ticket Médio e Desconto por Categoria.*

**Performance Logística:** O serviço **Standard** é o mais utilizado (70% dos pedidos confirmados), com o frete mais baixo, porém o maior prazo de entrega. O serviço **Same-Day**, embora mais caro, cumpre a promessa de entrega rápida. A taxa de atraso, no entanto, é similar entre os três serviços, pairando em torno de 47%.

![Análise de Serviços de Entrega](https://private-us-east-1.manuscdn.com/sessionFile/QZFEkxQOHKeamYWLo4fQ3z/sandbox/H57AvMkVReQI51ldYykAE6-images_1764336169595_na1fn_L2hvbWUvdWJ1bnR1L2FuYWxpc2UtZGFkb3MtZWNvbW1lcmNlL2ZpZ3VyZXMvMDlfYW5hbGlzZV9zZXJ2aWNv.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUVpGRWt4UU9IS2VhbVlXTG80ZlEzei9zYW5kYm94L0g1N0F2TWtWUmVRSTUxbGRZeWtBRTYtaW1hZ2VzXzE3NjQzMzYxNjk1OTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyRnVZV3hwYzJVdFpHRmtiM010WldOdmJXMWxjbU5sTDJacFozVnlaWE12TURsZllXNWhiR2x6WlY5elpYSjJhV052LnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=epiX2YuE0M5z5FSJCo3-AxSWoWQwaPZN6KSFvsaqKoETQqeX8fR0WiHspBqwif4zZA28xMPDUd3qcht2TWra8Zmx1bokrz2CxLkyxtPgErs868a4SCpaGZe84QhDRHR~2UhLEvdAn~ZUOYeb1WGt0sxOYLgseTmzAb8L5uDnoeSbziNUR5lL~4V6WzdXnXW2CWUSiyPrhw~rL-O9gN4DdY~PrhcutXfuxBMEDnb5d9QxnP9b6WYRqks~s9tgJlrdJF5CCS7mOyR-vfoG0F3sNLsdzByUZj-5beD3liOryhyc6KdbIvWNA2v2iclMZtm0ZoZi~G7eiZAe4wcfcMik0w__)
*Figura 4: Comparativo de Frete, Prazo e Atraso por tipo de serviço.*

---

## 4. Inferência Estatística

Para validar os achados e fazer generalizações para a população de clientes, foram realizados testes de hipóteses e calculados intervalos de confiança (ICs) com 95% de confiança.

### 4.1. Verificação de Suposições

Para a realização dos testes paramétricos, como o Intervalo de Confiança (IC) baseado na distribuição *t* e a Análise de Variância (ANOVA), a suposição de normalidade dos dados é ideal.

Os testes de normalidade (Shapiro-Wilk, D'Agostino-Pearson) rejeitaram a hipótese nula de normalidade para as variáveis financeiras e de tempo (p < 0.05). No entanto, devido ao **grande tamanho da amostra** (*n* = 4.636), o **Teorema do Limite Central** garante que a **distribuição amostral das médias** tende à normalidade, permitindo a aplicação robusta dos testes paramétricos.

Além da normalidade, a ANOVA exige a suposição de **homogeneidade das variâncias** (homocedasticidade) entre os grupos. O **Teste de Levene** foi aplicado para verificar se a variância do *Ticket Total* é similar entre as diferentes categorias de produtos.

*   **Resultado do Teste de Levene:** [P-valor: 0.00000]
*   **Conclusão:** Rejeita H0. Variâncias não são homogêneas (Heterocedasticidade).

A documentação completa dos testes de suposição está disponível no notebook `05_statistical_inference.py`.

### 4.2. Intervalos de Confiança (IC 95%)

Os ICs fornecem uma faixa de valores prováveis para as médias e proporções da população.

*   **IC para Ticket Médio Total:** Com 95% de confiança, o ticket médio de todos os clientes do e-commerce está entre **R$ 915,64 e R$ 990,08**.
*   **IC para Taxa de Atraso:** A verdadeira taxa de atraso da operação logística está entre **45.68% e 48.73%**.
*   **IC para Taxa de Confirmação:** A proporção de pedidos que são efetivamente pagos e confirmados está entre **88.09% e 89.89%**.

![Intervalos de Confiança para Médias](https://private-us-east-1.manuscdn.com/sessionFile/QZFEkxQOHKeamYWLo4fQ3z/sandbox/H57AvMkVReQI51ldYykAE6-images_1764336169595_na1fn_L2hvbWUvdWJ1bnR1L2FuYWxpc2UtZGFkb3MtZWNvbW1lcmNlL2ZpZ3VyZXMvMTFfaWNfbWVkaWFz.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUVpGRWt4UU9IS2VhbVlXTG80ZlEzei9zYW5kYm94L0g1N0F2TWtWUmVRSTUxbGRZeWtBRTYtaW1hZ2VzXzE3NjQzMzYxNjk1OTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyRnVZV3hwYzJVdFpHRmtiM010WldOdmJXMWxjbU5sTDJacFozVnlaWE12TVRGZmFXTmZiV1ZrYVdGei5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=TscEF4f3G0YOFG1qbySThYiCoccvZit-jBOddlv1EL-LHNQ6GbbPlJ7jUqCVbkWAA16slns9ldpipyMMofXRp26bIl7umwyMl34gZbfeRhGTpVsHA3ZMjKGH~1bzEYM3fadt7wxU-YQnjwAckIoWPY4ozSaIvCz8Beo86I8ImXuo8p2gXKMXZhQwVlJUNCNEeB1avcwawIXUWNhRbB2Tm4uquut6D33JaLDsegrLG5Yx4YUJuenUHCOrTe~Y6BWWHlzyzLVORyfkBy9lSTr8T9iUrUIGz6TcSnOK6LztSojP8FRIiZOf6jWFZs9EitCLDsqpHHIHZ5auGtol~RfljQ__)
*Figura 5: Intervalos de confiança de 95% para as principais métricas de média.*

### 4.3. Testes de Hipóteses

*   **Taxa de Confirmação vs. Método de Pagamento:** O teste Qui-Quadrado mostrou uma **associação estatisticamente significativa** (p < 0.001) entre o método de pagamento e a confirmação do pedido. Isso confirma que a diferença nas taxas de confirmação entre Boleto/Débito e Crédito/PIX não ocorre ao acaso.

*   **Ticket Médio vs. Categoria:** O teste ANOVA revelou **diferenças estatisticamente significativas** (p < 0.001) no ticket médio entre as diferentes categorias de produtos, validando que `Eletrônicos` possuem um ticket médio estruturalmente maior que as demais.

---

## 5. KPIs e Insights de Negócio

O dashboard abaixo consolida os principais KPIs (Key Performance Indicators) e direciona para os insights mais relevantes.

![Dashboard de KPIs](https://private-us-east-1.manuscdn.com/sessionFile/QZFEkxQOHKeamYWLo4fQ3z/sandbox/H57AvMkVReQI51ldYykAE6-images_1764336169649_na1fn_L2hvbWUvdWJ1bnR1L2FuYWxpc2UtZGFkb3MtZWNvbW1lcmNlL2ZpZ3VyZXMvMTNfZGFzaGJvYXJkX2twaXM.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvUVpGRWt4UU9IS2VhbVlXTG80ZlEzei9zYW5kYm94L0g1N0F2TWtWUmVRSTUxbGRZeWtBRTYtaW1hZ2VzXzE3NjQzMzYxNjk2NDlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyRnVZV3hwYzJVdFpHRmtiM010WldOdmJXMWxjbU5sTDJacFozVnlaWE12TVROZlpHRnphR0p2WVhKa1gydHdhWE0ucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=DDhtvuaLqTAFgOMBhSLAzu~AFQrdL~P7hAf6FnTqAgOC69TgVCuzRXqqSKJUmdzSNXyb8KFntiv67O-mor07B~a27xBzhdElTgxSKUWZAo-XRaF19rkU4ulftb9dXkKiE6KYj0j0hNhp5nDvMbKpsk4UJ1RO5MM0CargLX58mn06oZ4uJOTkyZ9IV5j9v6cmd2GDgJxq5HcUVXfzX2FOTxDWp3ddkPPaHrDchYhQNCB2xMsOFEmjfJwolUH1mLmcA5j2yCfWUpyGHwobaiiIYkTAGmPK5lR19uXTjxIhOteg2ZY2cZ5KDTLUNhV-cVvxykVHqhkT2NcJZNghd4JINg__)
*Figura 6: Dashboard consolidado com os principais KPIs do negócio.*

### Principais KPIs

| Categoria         | KPI                     | Valor                  |
| ----------------- | ----------------------- | ---------------------- |
| **Financeiro**    | Receita Total (Confirmada) | R$ 3.915.541,69        |
|                   | Ticket Médio            | R$ 952,86              |
|                   | Take-rate de Frete      | 3.48%                  |
| **Operacional**   | Taxa de Confirmação     | 88.95%                 |
|                   | Taxa de Cancelamento    | 11.05%                 |
| **Logístico**     | Prazo Médio de Entrega  | 10.1 dias              |
|                   | Taxa de Atraso          | 47.20%                 |

### Insights Acionáveis

1.  **Ação em Pagamentos:** A diferença de mais de 10 pontos percentuais na taxa de confirmação entre Boleto/Débito e PIX/Crédito é um ponto de atenção. **Recomendação:** Implementar um sistema de recuperação de boletos não pagos (ex: lembretes por e-mail/WhatsApp) e promover o PIX com pequenos incentivos (ex: cashback ou desconto no frete).

2.  **Estratégia de Mix de Produtos:** A alta concentração de receita em Eletrônicos (53%) cria uma dependência. **Recomendação:** Fomentar o crescimento de categorias com boa margem e ticket médio crescente, como **Casa e Decoração** (26% da receita), através de campanhas de marketing direcionadas e kits de produtos (bundles).

3.  **Otimização Logística:** A taxa de atraso de 47% é um ponto crítico que afeta a experiência do cliente. A região Nordeste é a mais impactada. **Recomendação:** Renegociar SLAs (Service Level Agreements) com as transportadoras, diversificar parceiros logísticos na região Nordeste e avaliar a viabilidade de um mini centro de distribuição para reduzir o *lead time*.
