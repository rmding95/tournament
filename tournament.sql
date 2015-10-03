-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

-- Table that stores player data
CREATE TABLE Players (
	name text,
	id serial PRIMARY KEY
);

-- Table that stores match data
CREATE TABLE Matches (
	p1 text,
	p2 text , 
	winner_id int REFERENCES Players(id) 
);

-- Joins the player and matches table on the player id
CREATE VIEW v_total as 
	SELECT * from players 
	LEFT JOIN matches on players.id = matches.winner_id;

-- A list of names that represents how many games each player has played
CREATE VIEW v_temp as 
	SELECT p1 from v_total WHERE p1 IS NOT NULL 
	UNION ALL
	SELECT p2 from v_total WHERE p2 IS NOT NULL;

-- Shows each player and the number of games played
CREATE VIEW v_numGames as
	SELECT p1, count(*) from v_temp 
	GROUP BY p1
	ORDER BY p1 asc;

-- Shows each player id and the number of wins
CREATE VIEW v_numWins as 
	SELECT id, count(winner_id) from v_total
	GROUP BY id
	ORDER BY id asc;

-- A sorted list of player ids from best to worst
CREATE VIEW v_playerStandings as
	SELECT * from v_numWins
	ORDER BY count desc;

/* FOR TESTING
INSERT INTO Players VALUES('DJOKOVIC');
INSERT INTO Players VALUES('CILIC');
INSERT INTO Players VALUES('WAWRINKA');
INSERT INTO Players VALUES('GASQUET');
INSERT INTO Players VALUES('POSPISIL');
INSERT INTO Players VALUES('MURRAY');
INSERT INTO Players VALUES('SIMON');
INSERT INTO Players VALUES('FEDERER');
INSERT INTO Players VALUES('NADAL');

INSERT INTO Matches VALUES('DJOKOVIC', 'CILIC', '1');
INSERT INTO Matches VALUES('WAWRINKA', 'GASQUET', '4');
INSERT INTO Matches VALUES('POSPISIL', 'MURRAY', '6');
INSERT INTO Matches VALUES('SIMON', 'FEDERER', '8');
INSERT INTO Matches VALUES('DJOKOVIC', 'GASQUET', '1');
INSERT INTO Matches VALUES('MURRAY', 'FEDERER', '8');
INSERT INTO Matches VALUES('DJOKOVIC', 'FEDERER', '1');
*/

