select m1.date, m1.team as home_team, m2.team as away_team, m1.h_a, m1.xG, m1.xGA, m1.scored, m1.missed, m1.wins, m1.draws, m1.loses
from football_matches.matches as m1
inner join football_matches.matches as m2
	on m1.date = m2.date
	and m1.xGA = m2.xG
	and m1.h_a = 'h'
where m1.year = 2015
and m1.league = 'EPL'
order by home_team, m1.date
