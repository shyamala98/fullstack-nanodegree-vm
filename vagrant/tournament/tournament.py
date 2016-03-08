#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Author: Shyamala Prakash
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM TRMNT_matches *")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM TRMNT_players *")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) FROM TRMNT_players")
    numplayers = c.fetchone()
    conn.close()
    return numplayers[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("PREPARE insertPlayerSql(text) AS INSERT INTO TRMNT_players (name) VALUES ($1)")
    c.execute("EXECUTE insertPlayerSql(%s)", [name])
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
    standings = []
    conn = connect()
    c = conn.cursor()
    c.execute("select playerID, playerName, wins, nummatches from TRMNT_player_wins_vw")
    rows = c.fetchall()
    for row in rows:
        print " ", row[0], row[1], row[2], row[3]
        s = [row[0], row[1], row[2], row[3]]
        standings.append(s)
    conn.close()
    return standings

def reportMatch(winner, loser='null', isTie='f'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    if (loser != 'null'):
        c.execute("PREPARE insertMatchSql(int, int, boolean) AS INSERT INTO TRMNT_matches (winnerid, loserid, istie) VALUES ($1, $2, $3)")
        c.execute("EXECUTE insertMatchSql(%s, %s, %s)", (winner, loser, isTie))
    else:
        c.execute("PREPARE insertMatchSql(int, boolean) AS INSERT INTO TRMNT_matches (winnerid, loserid, istie) VALUES ($1, null, $2)")
        c.execute("EXECUTE insertMatchSql(%s, %s)", (winner, isTie))
    conn.commit()
    conn.close()

def hasBye(player):
    """Returns true if the player has had a Bye

    :param player:
    :return:true if player has had a Bye, False otherwise
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) FROM TRMNT_matches where winnerid=%s and loserId is null",[player])
    n = c.fetchone()
    conn.close()
    if (n[0]>0):
        return True
    else:
        return False

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
    pairings = []
    standings = playerStandings()
    if (countPlayers()%2 > 0):
        #assign a bye to the first player that has not had a bye
        for s in standings:
            pid = s[0]
            if (not hasBye(pid)):
                reportMatch(pid) #record the bye for the player
                removePlayer = s
                break
        standings.remove(removePlayer)
    plist1 = standings[::2]
    plist2 = standings[1::2]
    for pos, player1 in enumerate(plist1):
        [i1, n1, w1, m1] = player1
        [i2, n2, w2, m2] = plist2[pos]
        pairings.append([i1,n1,i2,n2])
    return pairings







