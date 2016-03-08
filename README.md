rdb-fullstack
=============
Project: Tournament Results Project  - [Shyamala Prakash]
================================
This project contains python modules that track results of matches in a tournament and pairs players using the results of previous matches.

Required Libraries and Dependencies
-----------------------------------
It uses Postgres database to store information about the players and match results.
This project was tested within the Vagrant virtual machine provided in the vagrant/ directory.

Requires Python v2.* 
Requires psycopg2 library - This library implements the Python DB API specifications 2.0

Source files:
tournament.sql: 
Creates the database tournament
Creates the tables for players and matches called TRMNT_players and TRMNT_matches
Creates a view called TRMNT_player_wins_VW that aggregates information from TRNMT_players and TRMNT_matches 

tournament.py: Python module that defines functions to add/update/delete records from the database
tournament_test.py: Python module that tests the functions in tournament.py

How to Run Project
------------------
Clone this project from Git to your local machine

<!-- The following section was copied from the Tournament results getting started guide -->

<b>Using the Vagrant Virtual Machine</b>

The Vagrant VM has PostgreSQL installed and configured, as well as the psql
command line interface (CLI)

To use the Vagrant virtual machine, navigate to the
full­stack­nanodegree­vm/tournament directory in the terminal, then use the command <br/>
vagrantup(powers on the virtual machine) followed by <br/>
vagrantssh(logs into the virtual machine).

cd /vagrant to change directory to the synced folders in order to work on your project,<br/>
once your cd /vagrant, if you type ls on the command line, you'll see your tournament<br/>
folder.

The Vagrant VM provided has PostgreSQL server installed,
as well as the psql command line interface (CLI), so you'll need to have your VM on and
be logged into it to run your database configuration file (tournament.sql), and test
your Python file with tournament_test.py.

To run: <br/>
cd tournament <br/>
Create the tournament database, tables and views: <br/>
psql <br/>
\>\i tournament.sql <br/>
Exit from psql <br/>
python tournament_test.py

Extra Credit Description
------------------------
TRMNT_matches table includes a column isTie (boolean) to record a tied result for a match.

TRNMT_player_wins_vw is created <br/>
tournament=\><br/>
select  * from trmnt_player_wins_vw;<br/>
Will display: <br/>
 playerid |    playername    | wins | nummatches | owm <br/>

 playerid: Id of the player in the TRMNT_players table <br/>
 playerName: Name of the player in the TMNT_players table <br/>
 wins: the number of wins for this player (a tie is counted as a win) <br/>
 numMatches: is the number of matches played <br/>
 owm: number of matches won by the opponent <br/>
 The view is sorted in descending order, first by the number of wins and then by the owm
 
The swissPairings function can support an odd number of players. 
The player with the maximum number of wins is given a bye. a player cannot have more than 1 bye.

