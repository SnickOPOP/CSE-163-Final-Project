import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def r2_round_wins(r2: pd.DataFrame) -> None:
    columns_to_check = ['Round 2 Winner', 'Round 3 Winner', 'Round 4 Winner',
                        'Round 5 Winner']
    r2['Round Wins'] = (
        r2[columns_to_check].eq(r2['Pistol Loser Team'], axis=0).sum(axis=1)
    )

def eda(pat: pd.DataFrame, r2: pd.DataFrame) -> None:
    print('Pistols and Thrifties:')
    print(pat.shape)
    print(pat['GameID'].nunique())
    print(pat['MatchID'].nunique())
    print(pat['Team Name'].nunique())
    print(pat['TeamID'].nunique())
    print(pat['Result'].value_counts())
    print(pat['Pistols Won'].describe())
    print(pat['Potential Thrifties'].describe())
    print(pat['Thrifties Won'].describe())

    print('Round 2 Decisions:')
    print(r2.shape)
    print(r2['GameID'].nunique())
    print(r2['MatchID'].nunique())
    print(r2['Pistol Winner TeamID'].nunique())
    print(r2['Pistol Winner Team'].nunique())
    print(r2['Pistol Loser TeamID'].nunique())
    print(r2['Pistol Loser Team'].nunique())
    print(r2['Pistol Winner Side'].value_counts())
    print(r2['Pistol Loser Side'].value_counts())
    print(r2['Decision'].value_counts())
    print(r2['Round 2 Winner'].nunique())
    print(r2['Round 3 Winner'].nunique())
    print(r2['Round 4 Winner'].nunique())
    print(r2['Round 5 Winner'].nunique())
    print(r2['Round Wins'].value_counts())

    g1 = sns.catplot(x='Pistols Won', kind='count', data=pat)
    for ax in g1.axes.flat:
        ax.bar_label(ax.containers[0])
    plt.title('Count of Pistols won in a Single Map')
    plt.savefig('eda_pistols_won.png', bbox_inches='tight')

    g2 = sns.catplot(x='Thrifties Won', kind='count', data=pat)
    for ax in g2.axes.flat:
        ax.bar_label(ax.containers[0])
    plt.title('Count of Thrifties won in a Single Map')
    plt.savefig('eda_thrifties_won.png', bbox_inches='tight')

    g3 = sns.catplot(x='Decision', kind='count', data=r2)
    for ax in g3.axes.flat:
        ax.bar_label(ax.containers[0])
    plt.title('Count of Round 2 Decisions Made')
    plt.savefig('eda_decision.png', bbox_inches='tight')

    g4 = sns.catplot(x='Round Wins', kind='count', data=r2)
    for ax in g4.axes.flat:
        ax.bar_label(ax.containers[0])
    plt.title('Count of Round Wins from Rounds 2-5')
    plt.savefig('eda_round_wins.png', bbox_inches='tight')


def main():
    pat = pd.read_csv('pat_cleaned.csv')
    r2 = pd.read_csv('r2_cleaned.csv')

    r2_round_wins(r2)
    eda(pat, r2)


if __name__ == '__main__':
    main()