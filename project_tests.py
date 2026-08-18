import pandas as pd

import data_processing

PAT_TEST_FILE = 'pistols_and_thrifties_recent.csv'
R2_TEST_FILE = 'round_2_decisions_recent.csv'
MV_TEST_FILE = 'missing_values_test.csv'


def test_missing_values(data: pd.DataFrame, name_col: str, id_col: str):
    expected = [
        {'Name': 'NRG', 'ID': 1034},
        {'Name': 'FNC', 'ID': 2593},
        {'Name': 'TL', 'ID': 474},
        {'Name': 'SEN', 'ID': 2},
        {'Name': 'T1', 'ID': 15},
        {'Name': 'DFM', 'ID': 278}
    ]
    df_expected = pd.DataFrame(expected)
    data_processing.missing_values(data, name_col, id_col)
    assert df_expected.equals(data)


def main():
    df_pat = pd.read_csv(PAT_TEST_FILE)
    df_r2 = pd.read_csv(R2_TEST_FILE)
    df_mv = pd.read_csv(MV_TEST_FILE)

    test_missing_values(df_mv, 'Name', 'ID')
    print('All tests passed!')


if __name__ == '__main__':
    main()
