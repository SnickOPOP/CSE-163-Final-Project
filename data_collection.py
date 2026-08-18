import vlrdevapi
from vlrdevapi._series.economy import BuyType
import pandas as pd

EVENTS = 'all'

pistols_and_thrifties = []
round_2_decision = []

vct_events = vlrdevapi.event.list(tier='vct', status='completed',
                                  return_all=True)
franchised_events = []

event = vct_events.events[0]
event_counter = 0
while vlrdevapi.event(event.id).info().start_date.year > 2022:
    franchised_events.append(event)
    event_counter += 1
    event = vct_events.events[event_counter]

events = []
if EVENTS == 'recent':
    events.append(franchised_events[0])
if EVENTS == 'all':
    events = franchised_events

for event in events:
    matches = vlrdevapi.event(event.id).matches()
    for match in matches.matches:
        match_id = match.match_id
        games = vlrdevapi.series.info(match_id).games

        for game in games:
            econ = vlrdevapi.series.economy(series_id=match_id,
                                            game_id=game.game_id)
            rounds = econ.rounds

            if len(rounds) > 0:
                map_winner_pistols = 0
                if (
                    vlrdevapi.series.info(match_id).team1.tag == econ.team1
                ):
                    team1ID = vlrdevapi.series.info(match_id).team1.id
                    team2ID = vlrdevapi.series.info(match_id).team2.id
                    team1_name = vlrdevapi.series.info(match_id).team1.tag
                    team2_name = vlrdevapi.series.info(match_id).team2.tag
                else:
                    team1ID = vlrdevapi.series.info(match_id).team2.id
                    team2ID = vlrdevapi.series.info(match_id).team1.id
                    team1_name = vlrdevapi.series.info(match_id).team2.tag
                    team2_name = vlrdevapi.series.info(match_id).team1.tag

                if rounds[-1].winner.name == team1_name:
                    map_winner_id = team1ID
                    map_loser_id = team2ID
                    map_winner_name = team1_name
                    map_loser_name = team2_name
                else:
                    map_winner_id = team2ID
                    map_loser_id = team1ID
                    map_winner_name = team2_name
                    map_loser_name = team1_name

                if rounds[0].winner.name == map_winner_name:
                    map_winner_pistols += 1
                if rounds[12].winner.name == map_winner_name:
                    map_winner_pistols += 1

                if map_winner_pistols == 2:
                    map_loser_pistols = 0
                elif map_winner_pistols == 1:
                    map_loser_pistols = 1
                else:
                    map_loser_pistols = 2

                map_winner_thrifty_rounds = 0
                map_winner_thrifty_wins = 0
                map_loser_thrifty_rounds = 0
                map_loser_thrifty_wins = 0

                for round in rounds:
                    if (
                        (
                            round.buy_type_team1 == BuyType.ECO.value
                            and round.buy_type_team2 == BuyType.SEMI_BUY.value
                        )
                        or (
                            round.buy_type_team1 == BuyType.ECO.value
                            and round.buy_type_team2 == BuyType.FULL_BUY.value
                        )
                        or (
                            round.buy_type_team1 == BuyType.SEMI_ECO.value
                            and round.buy_type_team2 == BuyType.FULL_BUY.value
                        )
                    ):
                        if map_winner_name == team1_name:
                            map_winner_thrifty_rounds += 1
                            if round.winner.name == team1_name:
                                map_winner_thrifty_wins += 1
                        else:
                            map_loser_thrifty_rounds += 1
                            if round.winner.name == team1_name:
                                map_loser_thrifty_wins += 1
                    elif (
                        (
                            round.buy_type_team2 == BuyType.ECO.value
                            and round.buy_type_team1 == BuyType.SEMI_BUY.value
                        )
                        or (
                            round.buy_type_team2 == BuyType.ECO.value
                            and round.buy_type_team1 == BuyType.FULL_BUY.value
                        )
                        or (
                            round.buy_type_team2 == BuyType.SEMI_ECO.value
                            and round.buy_type_team1 == BuyType.FULL_BUY.value
                        )
                    ):
                        if map_winner_name == team2_name:
                            map_winner_thrifty_rounds += 1
                            if round.winner.name == team2_name:
                                map_winner_thrifty_wins += 1
                        else:
                            map_loser_thrifty_rounds += 1
                            if round.winner.name == team2_name:
                                map_loser_thrifty_wins += 1

                pistols_and_thrifties.append({
                    'MatchID': match_id,
                    'GameID': game.game_id,
                    'Team Name': map_winner_name,
                    'TeamID': map_winner_id,
                    'Result': 'won',
                    'Pistols Won': map_winner_pistols,
                    'Potential Thrifties': map_winner_thrifty_rounds,
                    'Thrifties Won': map_winner_thrifty_wins
                })

                pistols_and_thrifties.append({
                    'MatchID': match_id,
                    'GameID': game.game_id,
                    'Team Name': map_loser_name,
                    'TeamID': map_loser_id,
                    'Result': 'lost',
                    'Pistols Won': map_loser_pistols,
                    'Potential Thrifties': map_loser_thrifty_rounds,
                    'Thrifties Won': map_loser_thrifty_wins
                })

                pistol_winner = rounds[0].winner.name
                if team1_name == pistol_winner:
                    losing_team_buy = rounds[1].buy_type_team2
                    pistol_winner_id = team1ID
                    pistol_winner_side = 'defense'
                    pistol_loser = team2_name
                    pistol_loser_id = team2ID
                    pistol_loser_side = 'attack'
                else:
                    losing_team_buy = rounds[1].buy_type_team1
                    pistol_winner_id = team2ID
                    pistol_winner_side = 'attack'
                    pistol_loser = team1_name
                    pistol_loser_id = team1ID
                    pistol_loser_side = 'defense'

                if losing_team_buy == BuyType.ECO.value:
                    decision = 'eco'
                else:
                    decision = 'force'

                round_2_decision.append({
                    'MatchID': match_id,
                    'GameID': game.game_id,
                    'Pistol Winner TeamID': pistol_winner_id,
                    'Pistol Winner Team': pistol_winner,
                    'Pistol Winner Side': pistol_winner_side,
                    'Pistol Loser TeamID': pistol_loser_id,
                    'Pistol Loser Team': pistol_loser,
                    'Pistol Loser Side': pistol_loser_side,
                    'Decision': decision,
                    'Round 2 Winner': rounds[1].winner.name,
                    'Round 3 Winner': rounds[2].winner.name,
                    'Round 4 Winner': rounds[3].winner.name,
                    'Round 5 Winner': rounds[4].winner.name
                })

if EVENTS == 'recent':
    df_pat = pd.DataFrame(pistols_and_thrifties)
    df_pat.to_csv('pistols_and_thrifties_recent.csv', index=False)
    df_round_2 = pd.DataFrame(round_2_decision)
    df_round_2.to_csv('round_2_decisions_recent.csv', index=False)
if EVENTS == 'all':
    df_pat = pd.DataFrame(pistols_and_thrifties)
    df_pat.to_csv('pistols_and_thrifties.csv', index=False)
    df_round_2 = pd.DataFrame(round_2_decision)
    df_round_2.to_csv('round_2_decisions.csv', index=False)
