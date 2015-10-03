#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(name) from Players;")
    conn.commit()
    num = c.fetchone()[0]
    conn.close()
    return num

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Players values (%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # Retreives a list of player ids in sorted (best to worst) order
    c.execute("SELECT id from v_playerStandings")
    id_list = list(c.fetchall())
    standings = []
    # Uses the id to retreive the other information about each player
    for ids in id_list:
        c.execute("SELECT count from v_playerStandings where id = %s", (ids,))
        wins = c.fetchone()[0]
        c.execute("SELECT name from v_total where id = %s limit 1;", (ids,))
        name = c.fetchone()[0]
        # Checking if a player has any matches
        c.execute("SELECT exists(select * from v_numgames)")
        if c.fetchone()[0] is False:
            matches = 0
        else :
            c.execute("SELECT count from v_numGames where p1 = %s", (name,))
            matches = c.fetchone()[0]
        tup = (ids, name, wins, matches)
        standings.append(tup)
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT name from Players where id = %s", (winner,))
    player1 = c.fetchone()[0]
    c.execute("SELECT name from Players where id = %s", (loser,))
    player2 = c.fetchone()[0]
    # Results are reported in the format: player1, player2, id of winner
    c.execute("INSERT INTO Matches values (%s, %s, %s)",
              (player1, player2, winner,))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    # Gets a sorted list of player ids
    c.execute("SELECT id from v_playerstandings")
    id_list = list(c.fetchall())
    temp = []
    # temp is a temporary list that holds tuples of (id, name)
    for ids in id_list:
        c.execute("SELECT name from v_total where id = %s limit 1", (ids,))
        name = c.fetchone()[0]
        tup = (ids, name)
        temp.append(tup)
    pairings = []
    # here the tuples in temp are combined into pairings
    for i in range(len(temp)/2):
        tup1 = temp[i * 2]
        tup2 = temp[i * 2 + 1]
        pair = tup1 + tup2
        pairings.append(pair)
    return pairings
