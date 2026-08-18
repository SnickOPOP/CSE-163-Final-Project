import vlrdevapi
import pandas as pd


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
    data[''] #WIP


def main():
    df_pat = read_vlr_data('pistols_and_thrifties.csv')
    df_r2 = read_vlr_data('round_2_decisions.csv')
    print('Before Dealing with Missing Values:')
    data_summary(df_pat)
    data_summary(df_r2)

    missing_values(df_pat, 'Team Name', 'TeamID')
    missing_values(df_r2, 'Pistol Loser Team', 'Pistol Loser TeamID')

    print('After Dealing with Missing Values:')
    data_summary(df_pat)
    data_summary(df_r2)
    

if __name__ == '__main__':
    main()