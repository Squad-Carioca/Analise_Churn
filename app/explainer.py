# app/explainer.py

import joblib
import pandas as pd
import shap
import logging

logger = logging.getLogger(__name__)

PIPELINE_PATH = "app/pipeline_churn.joblib"
EXPLAINER_PATH = "app/explainer_churn.joblib"

try:
    pipeline_completo = joblib.load(PIPELINE_PATH)
    explainer = joblib.load(EXPLAINER_PATH)
    logger.info("Pipeline e explicador carregados com sucesso.")
except FileNotFoundError as e:
    logger.error("Erro ao carregar modelos: %s.", e)
    raise RuntimeError("Modelo ou explicador não encontrado.")


#logger.info("Dentro de Explainer!")

def get_prediction_and_explanation(cliente_input_df: pd.DataFrame):
    """ Usa o pipeline completo para prever e o explicador para detalhar. """

    # 1. Obter a predição e a probabilidade
    predicao_num = pipeline_completo.predict(cliente_input_df)[0]
    probabilidade_churn = pipeline_completo.predict_proba(cliente_input_df)[0][1]
    predicao_texto = "Sim (Risco de Churn)" if predicao_num == 1 else "Não (Baixo Risco)"

    # 2. Pré-processar os dados para o explicador
    dados_processados = pipeline_completo.named_steps['preprocessor'].transform(cliente_input_df)

    # 3. Calcular os valores SHAP - a saída é 3D (amostras, features, classes)
    shap_values = explainer.shap_values(dados_processados.toarray())
    # A saída é 3D (1, 45, 2). Queremos a fatia para a classe 1 (Churn).
    # Isso extrai a matriz 2D (1, 45) que corresponde ao impacto na classe "Churn".
    shap_values_churn = shap_values[:, :, 1]

    # 4. Formatar a explicação de forma robusta
    feature_names = pipeline_completo.named_steps['preprocessor'].get_feature_names_out()
    # Agora o Pandas recebe a matriz 2D correta
    df_shap = pd.DataFrame(shap_values_churn, columns=feature_names)
    df_shap_agg = pd.Series(dtype='float64')

    # Agrupamos os impactos pela feature original
    for col in df_shap.columns:
        original_feature = col.split('__')[1].split('_')[0]
        if original_feature not in df_shap_agg:
            df_shap_agg[original_feature] = 0

        df_shap_agg[original_feature] += int(df_shap[col].iloc[0])

    fatores_importantes = df_shap_agg.abs().sort_values(ascending=False)

    explicacao_final = []

    for feature, _ in fatores_importantes.head(3).items():
        impact = df_shap_agg[feature]
        direcao = "AUMENTA" if impact > 0 else "DIMINUI"
        explicacao_final.append(f"O fator '{feature}' {direcao} o risco de churn.")

    return {
        "predicao": predicao_texto,
        "probabilidade_churn": float(probabilidade_churn),
        "explicacao": explicacao_final
    }