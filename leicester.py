import pandas as pd
import numpy as np

games = pd.read_csv(r'E:\Python stuff\epl15matches.csv')

home = []; away = []
np.random.seed(123)
size = 10000

# Generate random home & away goals for each match on expected goals (xG)
for lab, row in games.iterrows():
    home_goals = np.random.poisson(row['xG'], size=size)
    away_goals = np.random.poisson(row['xGA'], size=size)
    home.append(home_goals)
    away.append(away_goals)
    
# DataFrame of all match results
match_index = list(map(lambda i: 'match '+str(i), np.arange(1, 381)))
df = pd.DataFrame({'match_index': match_index,
                   'home_team': games['home_team'],
                   'away_team': games['away_team']})

    # Split home and away goals into seasons
goals_sim = pd.DataFrame({'home_goals':np.concatenate(home), 
              'away_goals':np.concatenate(away)}, 
             index=np.repeat(range(380), size))
sim = df.join(goals_sim)

    # Generate season indices (sim indices)
season_index = list(map(lambda i: 'season '+str(i), np.arange(1, size+1))) * 380
sim.index = season_index

# Calculate points of each season
home_points = []
away_points = []
condition = [sim.home_goals > sim.away_goals, sim.home_goals == sim.away_goals]     
sim['home_points'] = np.select(condition, [3, 1], default=0)
sim['away_points'] = np.select(condition, [0, 1], default=3)

# Aggregate points, goals for/against/difference
total_points = sim.groupby([sim.index, sim.home_team])['home_points'].sum() + sim.groupby([sim.index, sim.away_team])['away_points'].sum()
total_gf = sim.groupby([sim.index, sim.home_team])['home_goals'].sum() + sim.groupby([sim.index, sim.away_team])['away_goals'].sum()
total_ga = sim.groupby([sim.index, sim.home_team])['away_goals'].sum() + sim.groupby([sim.index, sim.away_team])['home_goals'].sum()
total_gd = total_gf - total_ga

total_table = pd.concat([total_points, total_gf, total_ga, total_gd], axis=1)
total_table.columns = ('points', 'goals_for', 'goals_against', 'goals_dif')
total_table.index.names = ['Season', 'Team']
total_table = total_table.sort_values(['Season','points', 'goals_dif', 'goals_for'], ascending=(1,0,0,0))
pos = list(np.arange(1, 21)) * size
total_table.insert(0, column='position', value=pos)

# Average position
avg_table = total_table.groupby(level=1).mean().sort_values(['position'])
titles = total_table[total_table['position'] == 1].groupby(level=1)['position'].count().reindex(avg_table.index, fill_value=0)
p_value = titles / size
p_value.name = 'title_percentage'
avg_table = avg_table.join(p_value)
avg_table['title_percentage'] = avg_table['title_percentage'].apply(lambda i: "{0:.2%}".format(i))
print(avg_table)