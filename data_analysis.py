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


def ques1_analysis(pat: pd.DataFrame) -> None:
    print(pat.groupby('Pistols Won')['Result'].value_counts())

    pistols_won_percentages = (
            pat.groupby('Pistols Won')['Result']
            .value_counts(normalize=True)
            * 100
    )

    print(pistols_won_percentages)

    pistols_won_percentages_graph = (
        pat.groupby('Pistols Won')['Result']
        .value_counts(normalize=True)
        .unstack()
        * 100
    )

    pistols_won_percentages_graph.plot(kind='bar', stacked=False)
    plt.xticks(rotation=0)
    plt.xlabel('Pistol Round Wins')
    plt.ylabel('Percentages')
    plt.title('Percentage of Games won by Pistol Round Wins')
    plt.savefig('games_won_by_pistol_wins.png')


def ques2_analysis(r2: pd.DataFrame) -> None:
    print(r2.groupby('Decision')['Round Wins'].value_counts())

    r2_percentages = (
        r2.groupby('Decision')['Round Wins']
        .value_counts(normalize=True)
        * 100
    )

    print(r2_percentages)

    r2_percentages_graph = (
        r2.groupby('Decision')['Round Wins']
        .value_counts(normalize=True)
        .unstack()
        * 100
    )

    r2_percentages_graph.plot(kind='bar', stacked=False)
    plt.xticks(rotation=0)
    plt.xlabel('Round 2 Decision')
    plt.ylabel('Percentages')
    plt.title(
        'Percentage of Games where Amount of Rounds Won by Round 2 Decision'
    )
    plt.savefig('rounds_won_by_decision.png')


def ques3_analysis(pat: pd.DataFrame) -> None:
    print(pat.groupby('Thrifties Won')['Result'].value_counts())

    thrifties_won_percentages = (
            pat.groupby('Thrifties Won')['Result']
            .value_counts(normalize=True)
            * 100
    )

    print(thrifties_won_percentages)

    thrifties_won_percentages_graph = (
        pat.groupby('Thrifties Won')['Result']
        .value_counts(normalize=True)
        .unstack()
        * 100
    )

    thrifties_won_percentages_graph.plot(kind='bar', stacked=False)
    plt.xticks(rotation=0)
    plt.xlabel('Thrifty Round Wins')
    plt.ylabel('Percentages')
    plt.title('Percentage of Games won by Thrifty Round Wins')
    plt.savefig('games_won_by_thrifty_wins.png')


def main():
    pat = pd.read_csv('pat_cleaned.csv')
    r2 = pd.read_csv('r2_cleaned.csv')

    r2_round_wins(r2)
    eda(pat, r2)
    ques1_analysis(pat)
    ques2_analysis(r2)
    ques3_analysis(pat)


if __name__ == '__main__':
    main()
