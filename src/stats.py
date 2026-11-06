import pandas as pd
import numpy as np
from typing import Dict, Any, List

def calcular_estatisticas(series: pd.Series) -> Dict[str, Any]:
    """
    Calcula todas as estatísticas descritivas exigidas na Tabela do Tópico 8.
    """
    if series.empty:
        return {}

    q1 = float(np.percentile(series, 25))
    mediana = float(np.median(series))  # Q2
    q3 = float(np.percentile(series, 75))
    iqr = q3 - q1

    # Regra do 1.5 * IQR para detecção de Outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = series[(series < lower_bound) | (series > upper_bound)].tolist()

    return {
        "media": float(np.mean(series)),
        "mediana": mediana,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "amplitude": float(np.max(series) - np.min(series)),
        "desvio_padrao": float(np.std(series, ddof=1)) if len(series) > 1 else 0.0,
        "outliers": outliers,
        "limite_inferior": lower_bound,
        "limite_superior": upper_bound
    }