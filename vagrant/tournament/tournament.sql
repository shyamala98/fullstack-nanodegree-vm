-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the tournament database
\c vagrant
drop database if exists tournament;
create database tournament;
\c tournament

--Create the Player table
drop table if exists TRMNT_players;
create table TRMNT_players (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

--Create the Matches table
drop table if exists TRMNT_matches;
create table TRMNT_matches (
    id serial PRIMARY KEY,
    winnerID integer REFERENCES TRMNT_players (id),
    loserID integer REFERENCES TRMNT_players (id),
    isTie boolean
)

--Create the view for player wins
create view TRMNT_player_wins_VW as
WITH wins_table AS (
    select trmnt_players.id as playerID, trmnt_players.name as playerName, count(trmnt_matches.winnerid) as wins
        from trmnt_players
        left outer join trmnt_matches on
        ( trmnt_players.id = trmnt_matches.winnerid AND trmnt_matches.istie = false) OR
        ( (trmnt_players.id = trmnt_matches.winnerid  OR trmnt_players.id = trmnt_matches.loserid) AND trmnt_matches.istie = true)
         group by playerID ),
     matches_table AS
        (select count(trmnt_matches.id) as numMatches, trmnt_players.id as playerID
                from trmnt_players
                left outer join trmnt_matches on
                (trmnt_players.id = trmnt_matches.winnerid or trmnt_players.id = trmnt_matches.loserid)
                group by playerID),
     owm_table AS
        (select trmnt_players.ID  as playerID , sum(wins_table.wins) as owm
            from trmnt_players, wins_table
            where wins_table.playerID in (
               -- find the opponent ids
               ((select winnerID as oppID from trmnt_matches where loserID = trmnt_players.id)
                union (select loserID as oppID from  trmnt_matches where winnerID = trmnt_players.id))
            )
            group by trmnt_players.ID)
select wins_table.playerID as playerID, wins_table.playerName as playerName, wins_table.wins as wins,
        matches_table.numMatches as numMatches, owm_table.owm as owm
from wins_table
left join matches_table on wins_table.playerID = matches_table.playerID
left join owm_table on owm_table.playerID=wins_table.playerID
order by wins desc;