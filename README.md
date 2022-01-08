# MonteCarloFootballMatchSim
Monte Carlo Football Match Simulator

Brief: Monte Carlo simulations for predicting football match outcomes.

Programming language: Python

Library dependencies: 

- pandas
- numpy
- prettytable


Needs user input: can choose to be on a one-game basis (Keyboard) or from csv file (csv).

In the event the "Keyboard" choice is selected, the user will have to input: home team, home team xG, away team, away team xG.
By default, the number of simulations is 20,000. Information about the simulations is printed on-screen: 

- simulation #
- simulation time (in seconds)
- home team # of goals
- away team # of goals
- whether it is a home win/away win/draw
- the score margin.

At the end of the simulations, a table with statistics is presented, including the win probability for each team, as well as the draw probability.
Afterwards, the score matrix is printed, with % probabilities gives for each possible score. 
At the end, a short summary of the entire program is given.

If the event the "csv" choice is selected, a csv filename will be requested. The header of the csv file must be: 

Team-H, xG-H, Team-A, xG-A.

I have prepared and added a csv file with all the 191 games played in the Premier League this season (2021-2022) as an example. For each game in the file, a simulation will be conducted as if it were on a one-game basis. All the steps outlined above are valid for this choice as well. 
At the end of the simulations, a csv file is written with the following data:

- home team
- win probability
- expected points (xPts-H)
- away team
- win probability
- expected points (xPts-A)

How to run the program: python3 MC_MatchSimSimple.py
