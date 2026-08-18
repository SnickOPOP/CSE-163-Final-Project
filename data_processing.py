import vlrdevapi
import pandas as pd
import numpy as np


def read_vlr_data(dataset_filepath: str) -> pd.DataFrame:
    return pd.read_csv(dataset_filepath)


def data_summary(data: pd.DataFrame) -> None:
    data.info()
    missing_summary = pd.DataFrame({
        'Missing Count': data.isna().sum(),
        'Percentage (%)': (data.isna().mean() * 100)
    })
    print(missing_summary)


def missing_values(data: pd.DataFrame, name_col: str, id_col: str) -> None:
    data[name_col] = np.where(
        data[name_col].isnull(),
        data[id_col].apply(lambda id: vlrdevapi.team.info(team_id=id).tag),
        data[name_col]
    )


def main():
    df_pat = read_vlr_data('pistols_and_thrifties.csv')
    df_r2 = read_vlr_data('round_2_decisions.csv')
    print('Before Dealing with Missing Values:')
    data_summary(df_pat)
    data_summary(df_r2)
    df_r = read_vlr_data('r2_cleaned.csv')

    missing_values(df_pat, 'Team Name', 'TeamID')
    missing_values(df_r2, 'Pistol Loser Team', 'Pistol Loser TeamID')

    print('After Dealing with Missing Values:')
    data_summary(df_pat)
    data_summary(df_r2)

    missing_only = df_r.loc[df_r.isna().any(axis=1), df_r.isna().any(axis=0)]
    print("\nFiltered DataFrame:\n", missing_only)

    df_pat.to_csv('pat_cleaned.csv', index=False)
    df_r2.to_csv('r2_cleaned.csv', index=False)


if __name__ == '__main__':
    main()
