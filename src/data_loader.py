import pandas as pd
import numpy as np

def carregar_dados() -> pd.DataFrame:
    """
    Carrega a base de dados de Alfabetização por UF, Sexo e Raça/Cor.
    Caso o arquivo CSV local não exista, gera dados simulados do IBGE (Censo 2022).
    """
    try:
        df = pd.read_csv("data/alfabetizacao_uf.csv")
    except FileNotFoundError:
        # Gera dataset simulado representativo por UF
        ufs = [
            ("Rondônia", "RO", "Norte"), ("Acre", "AC", "Norte"), ("Amazonas", "AM", "Norte"),
            ("Roraima", "RR", "Norte"), ("Pará", "PA", "Norte"), ("Amapá", "AP", "Norte"),
            ("Tocantins", "TO", "Norte"), ("Maranhão", "MA", "Nordeste"), ("Piauí", "PI", "Nordeste"),
            ("Ceará", "CE", "Nordeste"), ("Rio Grande do Norte", "RN", "Nordeste"), ("Paraíba", "PB", "Nordeste"),
            ("Pernambuco", "PE", "Nordeste"), ("Alagoas", "AL", "Nordeste"), ("Sergipe", "SE", "Nordeste"),
            ("Bahia", "BA", "Nordeste"), ("Minas Gerais", "MG", "Sudeste"), ("Espírito Santo", "ES", "Sudeste"),
            ("Rio de Janeiro", "RJ", "Sudeste"), ("São Paulo", "SP", "Sudeste"), ("Paraná", "PR", "Sul"),
            ("Santa Catarina", "SC", "Sul"), ("Rio Grande do Sul", "RS", "Sul"), ("Mato Grosso do Sul", "MS", "Centro-Oeste"),
            ("Mato Grosso", "MT", "Centro-Oeste"), ("Goiás", "GO", "Centro-Oeste"), ("Distrito Federal", "DF", "Centro-Oeste")
        ]
        
        races = ["Branca", "Preta", "Parda", "Amarela", "Indígena"]
        genders = ["Homens", "Mulheres"]
        
        records = []
        np.random.seed(42)
        
        for name, sigla, reg in ufs:
            base_val = 94.0 if reg in ["Sul", "Sudeste"] else (91.0 if reg == "Centro-Oeste" else 84.0)
            for r in races:
                mod_r = 2.5 if r in ["Branca", "Amarela"] else (-2.0 if r in ["Preta", "Parda"] else -5.0)
                for g in genders:
                    mod_g = 1.2 if g == "Mulheres" else -0.5
                    noise = np.random.normal(0, 1.8)
                    rate = round(float(np.clip(base_val + mod_r + mod_g + noise, 60.0, 99.5)), 2)
                    records.append({
                        "UF": name,
                        "Sigla": sigla,
                        "Regiao": reg,
                        "Raca_Cor": r,
                        "Sexo": g,
                        "Taxa_Alfabetizacao": rate
                    })
        df = pd.DataFrame(records)
    return df