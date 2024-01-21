# Copyright       : @TacticsBadger (also known as @AnalyticsGopher), member of @CPFCInsights
# Website         : TacticsNotAntics: https://tacticsnotantics.org
# Github          : https://github.com/TacticsBadger/MonteCarloFootballMatchSim/
# Version 1.0.0   : November 17, 2021
# Current version : 1.5.0
# Last Updated    : January  21, 2024

'''
Brief: Monte Carlo simulations for predicting match outcomes.
Needs user input: keyboard or csv.
In the event the "csv" choice is selected, a csv filename will be requested. The header of the csv file must be:
Team-H, xG-H, Team-A, xG-A.

xG data should ideally be taken from https://fbref.com/en/ (uses Opta data).  
'''

import sys
import math
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from prettytable import PrettyTable

print("*************************** Tactics Not Antics *************************")
print("*************          Monte Carlo Match Simulator        **************")
print("*************        Version 1.0.0: November  17, 2021    **************")
print("*************        Version 1.5.0: September 09, 2023    **************")
print("*************        Last Update  : January   21, 2024    **************")
print("************************************************************************")
print("*************************** PL TEAMS 2023-24 ***************************")
print("* Arsenal        | Aston Villa    | Brentford          | Brighton      *")
print("* Burnley        | Chelsea        | Crystal Palace     | Everton       *")
print("* Luton Town     | Fulham         | Liverpool          | Bournemouth   *")
print("* Manchester Utd | Newcastle Utd  | Nottingham Forest  | Sheffield Utd *")
print("* West Ham       | Tottenham      | Manchester City    | Wolves        *")
print("************************************************************************")

num_simulations = 20000
choice = input("* Keyboard or csv: ")

if choice == "Keyboard":
    print ("Reading data from the keyboard.")
    input_home_team = input("* Add home team: ")
    input_home_team_xg_str = input("* Add home team xG: ")
    input_home_team_xg = float(input_home_team_xg_str)
    input_away_team = input("* Add away team: ")
    input_away_team_xg_str = input("* Add away team xG: ")
    input_away_team_xg = float(input_away_team_xg_str)
    #print the simulation table and run simulations
    print ("********************")
    print ("*                  *")
    print ("* SIMULATION TABLE *")
    print ("*                  *")
    print ("********************")
    count_home_wins = 0
    count_home_loss = 0
    count_away_wins = 0
    count_away_loss = 0
    count_draws = 0
    score_mat = []
    tot_sim_time = 0
    sim_table = PrettyTable(["SIMULATION #", "SIMULATION TIME (s)", input_home_team, input_away_team, "HOME WIN", "AWAY WIN", "DRAW", "SCORE MARGIN"])
    for i in range(num_simulations):
        #get simulation start time
        start_time = time.time()
        #run the sim - generate a random Poisson distribution
        target_home_goals_scored = np.random.poisson(input_home_team_xg)
        target_away_goals_scored = np.random.poisson(input_away_team_xg)
        home_win = 0
        away_win = 0
        draw = 0
        margin = 0
        # if more goals for home team => home team wins
        if target_home_goals_scored > target_away_goals_scored:
            count_home_wins += 1
            count_away_loss += 1
            home_win = 1
            margin = target_home_goals_scored - target_away_goals_scored
        # if more goals for away team => away team wins
        elif target_home_goals_scored < target_away_goals_scored:
            count_away_wins += 1
            count_home_loss += 1
            away_win = 1
            margin = target_away_goals_scored - target_home_goals_scored
        elif target_home_goals_scored == target_away_goals_scored:
            draw = 1
            count_draws += 1
            margin = target_away_goals_scored - target_home_goals_scored
        # add score to score matrix
        score_mat.append((target_home_goals_scored, target_away_goals_scored))
        #get end time
        end_time = time.time()
        #add the time to the total simulation time
        tot_sim_time += round((end_time - start_time),5)
        #add the info to the simulation table
        sim_table.add_row([i+1, round((end_time - start_time),5), target_home_goals_scored, target_away_goals_scored, home_win, away_win, draw, margin])
    print(sim_table)

    # calculate probabilities to win/lose/draw
    home_win_probability = round((count_home_wins/num_simulations * 100),2)
    away_win_probability = round((count_away_wins/num_simulations * 100),2)
    draw_probability = round((count_draws/num_simulations * 100),2)
    
    # print the simulation statistics
    print ("*************")
    print ("*           *")
    print ("* SIM STATS *")
    print ("*           *")
    print ("*************")
    sim_table_stats = PrettyTable(["Total # of sims", "Total time (s) for sims", "HOME WINS", "AWAY WINS", "DRAWS"])
    sim_table_stats.add_row([num_simulations, round(tot_sim_time,3), count_home_wins, count_away_wins, count_draws])
    sim_table_stats.add_row(["-", "-", str(home_win_probability)+"%", str(away_win_probability)+"%", str(draw_probability)+"%"])
    print(sim_table_stats)
    
    # get the score matrix
    total_scores = len(score_mat)
    max_score = 5
    assemble_scores = [[0 for x in range(max_score)] for y in range(max_score)]
    for i in range(total_scores):
        if score_mat[i][0] == 0 and score_mat[i][1] == 0:
            assemble_scores[0][0] += 1
        elif score_mat[i][0] == 0 and score_mat[i][1] == 1:
            assemble_scores[0][1] += 1
        elif score_mat[i][0] == 0 and score_mat[i][1] == 2:
            assemble_scores[0][2] += 1     
        elif score_mat[i][0] == 0 and score_mat[i][1] == 3:
            assemble_scores[0][3] += 1     
        elif score_mat[i][0] == 0 and score_mat[i][1] == 4:
            assemble_scores[0][4] += 1    
        elif score_mat[i][0] == 1 and score_mat[i][1] == 0:
            assemble_scores[1][0] += 1
        elif score_mat[i][0] == 1 and score_mat[i][1] == 1:
            assemble_scores[1][1] += 1     
        elif score_mat[i][0] == 1 and score_mat[i][1] == 2:
            assemble_scores[1][2] += 1     
        elif score_mat[i][0] == 1 and score_mat[i][1] == 3:
            assemble_scores[1][3] += 1     
        elif score_mat[i][0] == 1 and score_mat[i][1] == 4:
            assemble_scores[1][4] += 1
        elif score_mat[i][0] == 2 and score_mat[i][1] == 0:
            assemble_scores[2][0] += 1
        elif score_mat[i][0] == 2 and score_mat[i][1] == 1:
            assemble_scores[2][1] += 1     
        elif score_mat[i][0] == 2 and score_mat[i][1] == 2:
            assemble_scores[2][2] += 1     
        elif score_mat[i][0] == 2 and score_mat[i][1] == 3:
            assemble_scores[2][3] += 1     
        elif score_mat[i][0] == 2 and score_mat[i][1] == 4:
            assemble_scores[2][4] += 1
        elif score_mat[i][0] == 3 and score_mat[i][1] == 0:
            assemble_scores[3][0] += 1
        elif score_mat[i][0] == 3 and score_mat[i][1] == 1:
            assemble_scores[3][1] += 1     
        elif score_mat[i][0] == 3 and score_mat[i][1] == 2:
            assemble_scores[3][2] += 1     
        elif score_mat[i][0] == 3 and score_mat[i][1] == 3:
            assemble_scores[3][3] += 1     
        elif score_mat[i][0] == 3 and score_mat[i][1] == 4:
            assemble_scores[3][4] += 1            
        elif score_mat[i][0] == 4 and score_mat[i][1] == 0:
            assemble_scores[4][0] += 1
        elif score_mat[i][0] == 4 and score_mat[i][1] == 1:
            assemble_scores[4][1] += 1     
        elif score_mat[i][0] == 4 and score_mat[i][1] == 2:
            assemble_scores[4][2] += 1     
        elif score_mat[i][0] == 4 and score_mat[i][1] == 3:
            assemble_scores[4][3] += 1     
        elif score_mat[i][0] == 4 and score_mat[i][1] == 4:
            assemble_scores[4][4] += 1    
            
    #calculate percentages and print the score matrix
    print ("**********************************")        
    print ("*                                *")       
    print ("*  SCORE MATRIX (% PROBABILITY)  *")
    print ("*                                *")
    print ("**********************************")
    score_matrix = PrettyTable([" ", 0, 1, 2, 3, 4])
    score_matrix.add_row([0,round(assemble_scores[0][0]/num_simulations*100,2),round(assemble_scores[0][1]/num_simulations*100,2),round(assemble_scores[0][2]/num_simulations*100,2),round(assemble_scores[0][3]/num_simulations*100,2),round(assemble_scores[0][4]/num_simulations*100,2)])
    score_matrix.add_row([1,round(assemble_scores[1][0]/num_simulations*100,2),round(assemble_scores[1][1]/num_simulations*100,2),round(assemble_scores[1][2]/num_simulations*100,2),round(assemble_scores[1][3]/num_simulations*100,2),round(assemble_scores[1][4]/num_simulations*100,2)])
    score_matrix.add_row([2,round(assemble_scores[2][0]/num_simulations*100,2),round(assemble_scores[2][1]/num_simulations*100,2),round(assemble_scores[2][2]/num_simulations*100,2),round(assemble_scores[2][3]/num_simulations*100,2),round(assemble_scores[2][4]/num_simulations*100,2)])
    score_matrix.add_row([3,round(assemble_scores[3][0]/num_simulations*100,2),round(assemble_scores[3][1]/num_simulations*100,2),round(assemble_scores[3][2]/num_simulations*100,2),round(assemble_scores[3][3]/num_simulations*100,2),round(assemble_scores[3][4]/num_simulations*100,2)])
    score_matrix.add_row([4,round(assemble_scores[4][0]/num_simulations*100,2),round(assemble_scores[4][1]/num_simulations*100,2),round(assemble_scores[4][2]/num_simulations*100,2),round(assemble_scores[4][3]/num_simulations*100,2),round(assemble_scores[4][4]/num_simulations*100,2)])
    print(score_matrix) 
    
    #calculate expected Pts and print a summary
    home_xPts = (home_win_probability / 100) * 3.0 + (draw_probability / 100) * 1.0 + (away_win_probability / 100) * 0.0
    away_xPts = (away_win_probability / 100) * 3.0 + (draw_probability / 100) * 1.0 + (home_win_probability / 100) * 0.0
    print ("**********************************")        
    print ("*                                *")       
    print ("*             SUMMARY            *")
    print ("*                                *")
    print ("**********************************")
    print(input_home_team, "win probability %:", home_win_probability, "xPts =", round(home_xPts,2))
    print(input_away_team, "win probability %:", away_win_probability, "xPts =", round(away_xPts,2))
    print("Draw probability %:", draw_probability)
    
elif choice == "csv":
    # this info will be used if the csv choice is selected
    teams = ()
    points = dict()
    formatted_season = ""
    teams_2122=('Manchester City', 'Liverpool', 'Chelsea', 'Tottenham', 'Arsenal',
                'Manchester Utd', 'West Ham', 'Leicester City', 'Brighton', 'Wolves',
                'Newcastle Utd', 'Crystal Palace', 'Brentford', 'Aston Villa', 'Southampton',
                'Everton', 'Leeds United', 'Burnley', 'Watford', 'Norwich City')
    pts_2122=dict({'Manchester City': 93, 'Liverpool': 92, 'Chelsea': 74, 'Tottenham': 71, 'Arsenal':69,
                   'Manchester Utd': 58, 'West Ham': 56, 'Leicester City': 52, 'Brighton': 51, 'Wolves': 51,
                   'Newcastle Utd': 49, 'Crystal Palace': 48, 'Brentford': 46, 'Aston Villa': 45, 'Southampton': 40,
                   'Everton': 39, 'Leeds United': 38, 'Burnley': 35, 'Watford': 23, 'Norwich City': 22})
    teams_2223=('Manchester City', 'Arsenal', 'Manchester Utd', 'Newcastle Utd', 'Liverpool',
                'Brighton', 'Aston Villa', 'Tottenham', 'Brentford', 'Fulham', 
                'Crystal Palace', 'Chelsea', 'Wolves', 'West Ham', 'Bournemouth',
                'Nottingham Forest', 'Everton', 'Leicester City', 'Leeds United', 'Southampton')
    pts_2223=dict({'Manchester City': 89, 'Arsenal': 84, 'Manchester Utd': 75, 'Newcastle Utd': 71, 'Liverpool': 67,
                   'Brighton': 62, 'Aston Villa': 61, 'Tottenham': 60, 'Brentford': 59, 'Fulham': 52,
                   'Crystal Palace': 45, 'Chelsea': 44, 'Wolves': 41, 'West Ham': 40, 'Bournemouth': 39,
                   'Nottingham Forest': 38, 'Everton': 36, 'Leicester City': 34, 'Leeds United': 31, 'Southampton':25})
    teams_2324=('Manchester City', 'Tottenham', 'Liverpool', 'West Ham', 'Arsenal', 
                'Brighton', 'Crystal Palace', 'Brentford', 'Nottingham Forest', 'Aston Villa', 
                'Manchester Utd', 'Chelsea', 'Fulham', 'Newcastle Utd', 'Wolves',
                'Bournemouth', 'Sheffield Utd', 'Everton', 'Luton Town', 'Burnley')
    # this dictionary will have to be updated throughout the season
    pts_2324=dict({'Liverpool': 48, 'Manchester City': 43, 'Arsenal': 43, 'Aston Villa': 43, 'Tottenham': 40, 
                   'West Ham' : 35, 'Manchester Utd' : 32, 'Brighton':31, 'Chelsea': 31, 'Newcastle Utd': 29,
                   'Wolves': 28, 'Bournemouth': 25, 'Fulham': 24, 'Brentford': 22, 'Crystal Palace': 21,
                   'Nottingham Forest': 20, 'Everton': 17, 'Luton Town': 16, 'Burnley': 12, 'Sheffield Utd': 10})
                
    season = input("* Select season (21/22, 22/23, 23/24): ")
    if season == "21/22":
        teams = teams_2122
        points = pts_2122
        formatted_season="2122"
    elif season == "22/23":
        teams = teams_2223
        points = pts_2223
        formatted_season="2223"
    elif season == "23/24":
        teams = teams_2324
        points = pts_2324
        formatted_season="2324"
    else:
        print("Invalid season.")
        sys.exit()
    
    print ("* Will read data from csv file.")
    csv_filename = input("* Add csv filename: ")
    print("**********************************")    
    
    ovl_xpts = 0
    ovl_xgf  = 0
    ovl_xga  = 0
    ovl_xgd  = 0
    
    ovl_xpts_dict = {}
    ovl_xgf_dict = {}
    ovl_xga_dict = {}
    ovl_xgd_dict = {}
    
    for i in teams:
        ovl_xpts_dict[i] = ovl_xpts
        ovl_xgf_dict[i]  = ovl_xgf
        ovl_xga_dict[i]  = ovl_xga
        ovl_xgd_dict[i]  = ovl_xgd
   
    df = pd.read_csv(csv_filename)
    for i in range(0, len(df)):
        print("* Game #", i+1, "*")
        
        # identify the team and its xG
        input_home_team = df.iloc[i]['Team-H']
        input_home_team_xg = df.iloc[i]['xG-H']
        input_away_team = df.iloc[i]['Team-A']
        input_away_team_xg = df.iloc[i]['xG-A']
        
        # print team info
        print("* Home team:", input_home_team)
        print("* Away team:", input_away_team)
        print("* Home team xG:", input_home_team_xg)
        print("* Away team xG:", input_away_team_xg)
        
        # print the simulation table and run simulations
        print ("********************")
        print ("*                  *")
        print ("* SIMULATION TABLE *")
        print ("*                  *")
        print ("********************")
        
        # variables to keep track of wins/losses/draws
        count_home_wins = 0
        count_home_loss = 0
        count_away_wins = 0
        count_away_loss = 0
        count_draws = 0
        score_mat = []
        tot_sim_time = 0
        
        # header for our table
        sim_table = PrettyTable(["SIMULATION #", "SIMULATION TIME (s)", input_home_team, input_away_team, "HOME WIN", "AWAY WIN", "DRAW", "SCORE MARGIN"])
       
        for i in range(num_simulations):
            #get simulation start time
            start_time = time.time()
            #run the sim - generate a random Poisson distribution
            target_home_goals_scored = np.random.poisson(input_home_team_xg)
            target_away_goals_scored = np.random.poisson(input_away_team_xg)
            home_win = 0
            away_win = 0
            draw = 0
            margin = 0
            # if more goals for home team => home team wins
            if target_home_goals_scored > target_away_goals_scored:
                count_home_wins += 1
                count_away_loss += 1
                home_win = 1
                margin = target_home_goals_scored - target_away_goals_scored
            # if more goals for away team => away team wins
            elif target_home_goals_scored < target_away_goals_scored:
                count_away_wins += 1
                count_home_loss += 1
                away_win = 1
                margin = target_away_goals_scored - target_home_goals_scored
            elif target_home_goals_scored == target_away_goals_scored:
                draw = 1
                count_draws += 1
                margin = target_away_goals_scored - target_home_goals_scored
            # add score to score matrix
            score_mat.append((target_home_goals_scored, target_away_goals_scored))
            #get end time
            end_time = time.time()
            #add the time to the total simulation time
            tot_sim_time += round((end_time - start_time),5)
            #add the info to the simulation table
            sim_table.add_row([i+1, round((end_time - start_time),5), target_home_goals_scored, target_away_goals_scored, home_win, away_win, draw, margin])
        print(sim_table)

        # calculate probabilities to win/lose/draw
        home_win_probability = round((count_home_wins/num_simulations * 100),2)
        away_win_probability = round((count_away_wins/num_simulations * 100),2)
        draw_probability = round((count_draws/num_simulations * 100),2)
    
        # print the simulation statistics
        print ("*************")
        print ("*           *")
        print ("* SIM STATS *")
        print ("*           *")
        print ("*************")
        sim_table_stats = PrettyTable(["Total # of sims", "Total time (s) for sims", "HOME WINS", "AWAY WINS", "DRAWS"])
        sim_table_stats.add_row([num_simulations, round(tot_sim_time,3), count_home_wins, count_away_wins, count_draws])
        sim_table_stats.add_row(["-", "-", str(home_win_probability)+"%", str(away_win_probability)+"%", str(draw_probability)+"%"])
        print(sim_table_stats)
        
        # get the score matrix
        total_scores = len(score_mat)
        max_score = 5
        assemble_scores = [[0 for x in range(max_score)] for y in range(max_score)]
        for i in range(total_scores):
            if score_mat[i][0] == 0 and score_mat[i][1] == 0:
                assemble_scores[0][0] += 1
            elif score_mat[i][0] == 0 and score_mat[i][1] == 1:
                assemble_scores[0][1] += 1
            elif score_mat[i][0] == 0 and score_mat[i][1] == 2:
                assemble_scores[0][2] += 1
            elif score_mat[i][0] == 0 and score_mat[i][1] == 3:
                assemble_scores[0][3] += 1  
            elif score_mat[i][0] == 0 and score_mat[i][1] == 4:
                assemble_scores[0][4] += 1    
            elif score_mat[i][0] == 1 and score_mat[i][1] == 0:
                assemble_scores[1][0] += 1
            elif score_mat[i][0] == 1 and score_mat[i][1] == 1:
                assemble_scores[1][1] += 1     
            elif score_mat[i][0] == 1 and score_mat[i][1] == 2:
                assemble_scores[1][2] += 1     
            elif score_mat[i][0] == 1 and score_mat[i][1] == 3:
                assemble_scores[1][3] += 1     
            elif score_mat[i][0] == 1 and score_mat[i][1] == 4:
                assemble_scores[1][4] += 1
            elif score_mat[i][0] == 2 and score_mat[i][1] == 0:
                assemble_scores[2][0] += 1
            elif score_mat[i][0] == 2 and score_mat[i][1] == 1:
                assemble_scores[2][1] += 1     
            elif score_mat[i][0] == 2 and score_mat[i][1] == 2:
                assemble_scores[2][2] += 1     
            elif score_mat[i][0] == 2 and score_mat[i][1] == 3:
                assemble_scores[2][3] += 1     
            elif score_mat[i][0] == 2 and score_mat[i][1] == 4:
                assemble_scores[2][4] += 1
            elif score_mat[i][0] == 3 and score_mat[i][1] == 0:
                assemble_scores[3][0] += 1
            elif score_mat[i][0] == 3 and score_mat[i][1] == 1:
                assemble_scores[3][1] += 1     
            elif score_mat[i][0] == 3 and score_mat[i][1] == 2:
                assemble_scores[3][2] += 1     
            elif score_mat[i][0] == 3 and score_mat[i][1] == 3:
                assemble_scores[3][3] += 1     
            elif score_mat[i][0] == 3 and score_mat[i][1] == 4:
                assemble_scores[3][4] += 1            
            elif score_mat[i][0] == 4 and score_mat[i][1] == 0:
                assemble_scores[4][0] += 1
            elif score_mat[i][0] == 4 and score_mat[i][1] == 1:
                assemble_scores[4][1] += 1     
            elif score_mat[i][0] == 4 and score_mat[i][1] == 2:
                assemble_scores[4][2] += 1     
            elif score_mat[i][0] == 4 and score_mat[i][1] == 3:
                assemble_scores[4][3] += 1     
            elif score_mat[i][0] == 4 and score_mat[i][1] == 4:
                assemble_scores[4][4] += 1     
            
        #calculate percentages and print the score matrix
        print ("**********************************")        
        print ("*                                *")       
        print ("*  SCORE MATRIX (% PROBABILITY)  *")
        print ("*                                *")
        print ("**********************************")
        score_matrix = PrettyTable([" ", 0, 1, 2, 3, 4])
        score_matrix.add_row([0,round(assemble_scores[0][0]/num_simulations*100,2),round(assemble_scores[0][1]/num_simulations*100,2),round(assemble_scores[0][2]/num_simulations*100,2),round(assemble_scores[0][3]/num_simulations*100,2),round(assemble_scores[0][4]/num_simulations*100,2)])
        score_matrix.add_row([1,round(assemble_scores[1][0]/num_simulations*100,2),round(assemble_scores[1][1]/num_simulations*100,2),round(assemble_scores[1][2]/num_simulations*100,2),round(assemble_scores[1][3]/num_simulations*100,2),round(assemble_scores[1][4]/num_simulations*100,2)])
        score_matrix.add_row([2,round(assemble_scores[2][0]/num_simulations*100,2),round(assemble_scores[2][1]/num_simulations*100,2),round(assemble_scores[2][2]/num_simulations*100,2),round(assemble_scores[2][3]/num_simulations*100,2),round(assemble_scores[2][4]/num_simulations*100,2)])
        score_matrix.add_row([3,round(assemble_scores[3][0]/num_simulations*100,2),round(assemble_scores[3][1]/num_simulations*100,2),round(assemble_scores[3][2]/num_simulations*100,2),round(assemble_scores[3][3]/num_simulations*100,2),round(assemble_scores[3][4]/num_simulations*100,2)])
        score_matrix.add_row([4,round(assemble_scores[4][0]/num_simulations*100,2),round(assemble_scores[4][1]/num_simulations*100,2),round(assemble_scores[4][2]/num_simulations*100,2),round(assemble_scores[4][3]/num_simulations*100,2),round(assemble_scores[4][4]/num_simulations*100,2)])
        print(score_matrix) 
        
        # calculate expected Pts
        home_xPts = (home_win_probability / 100) * 3.0 + (draw_probability / 100) * 1.0 + (away_win_probability / 100) * 0.0
        away_xPts = (away_win_probability / 100) * 3.0 + (draw_probability / 100) * 1.0 + (home_win_probability / 100) * 0.0
        
        # and print a summary
        print ("**********************************")        
        print ("*                                *")       
        print ("*             SUMMARY            *")
        print ("*                                *")
        print ("**********************************")
        print(input_home_team, "win probability %:", home_win_probability, "xPts =", round(home_xPts,2))
        print(input_away_team, "win probability %:", away_win_probability, "xPts =", round(away_xPts,2))
        print("Draw probability %:", draw_probability)
        print("**********************************")
        
        # write the final results to the csv file
        result_tuple_csv = (input_home_team, round(home_win_probability,2), round(home_xPts,2), input_away_team, round(away_win_probability,2), round(away_xPts,2), "\n")
        final_results_filename = "MonteCarloMatchSimResults" + formatted_season + ".csv"
        with open(final_results_filename, "a+") as myfile:
            myfile.write(",".join(map(str, result_tuple_csv)))
            
        # add the info to the dictionaries
        for team, xpts in ovl_xpts_dict.items():
            if team == input_home_team:
                ovl_xpts_dict.update({team: round((xpts + home_xPts),2)})
            elif team == input_away_team:
                ovl_xpts_dict.update({team: round((xpts + away_xPts),2)})
        for team, xgf in ovl_xgf_dict.items():
            if team == input_home_team:
                ovl_xgf_dict.update({team: round((xgf + input_home_team_xg),2)})
            elif team == input_away_team:
                ovl_xgf_dict.update({team: round((xgf + input_away_team_xg),2)})
        for team, xga in ovl_xga_dict.items():
            if team == input_home_team:
                ovl_xga_dict.update({team: round((xga + input_away_team_xg),2)})
            elif team == input_away_team:
                ovl_xga_dict.update({team: round((xga + input_home_team_xg),2)})
        for team, xgd in ovl_xgd_dict.items():
            if team == input_home_team:
                ovl_xgd_dict.update({team: round((xgd + (input_home_team_xg - input_away_team_xg)),2)})
            elif team == input_away_team:
                ovl_xgd_dict.update({team: round((xgd + (input_away_team_xg - input_home_team_xg)),2)})
else:
    print("Not a valid option. Exiting.")
    sys.exit()

if choice == "csv":
    # sort the xpts dictionary
    sorted_ovl_xpts_dict = sorted(ovl_xpts_dict.items(), key=lambda x:x[1], reverse=True)
    converted_ovl_xpts_dict = dict(sorted_ovl_xpts_dict)
    
    # generate the final table for Plotly
    final_table = []
    rank = 0
    for team, xpts in converted_ovl_xpts_dict.items():
        xgf = round(ovl_xgf_dict.get(team),2)
        xga = round(ovl_xga_dict.get(team),2)
        xgd = round(ovl_xgd_dict.get(team),2)
        pts = round(points.get(team),2)
        ptsdiff = round((pts - xpts),2)
        rank += 1
        team_stats = [rank, team, round(xpts,2), pts, ptsdiff, xgf, xga, xgd]
        final_table.append(team_stats)
        
    # first, make sure the list is in the correct format for printing
    final_table_manip = np.array([list(elem) for elem in final_table]).T.tolist()
    
    # Plotly image
    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b>RANK</b>', '<b>TEAM</b>', '<b>XPTS</b>', '<b>PTS</b>', '<b>PTSDIFF</b>', '<b>XGF</b>', '<b>XGA</b>', '<b>XGD</b>'],
                    line_color='darkslategray',
                    fill_color='#27408B',
                    align='center',
                    font_size=14,
                    font_color='black'),
        cells=dict(values=[list(elem) for elem in final_table_manip],
                line_color='darkslategray',
                fill_color='#FFF5EE',
                align='center',
                font_size=12)),
    ])
    
    # change figure layout, including size and title
    fig_name = "MC_Final_Table_" + formatted_season + ".html"
    fig.update_layout(width=1200, height=1000)
    fig.update_layout(
    title={
        'text': "<b>xPTS Table - Premier League Season " + season + "</b><br><sup><b>@TacticsBadger</b>, @CPFCInsights</b></sup><br><sup>xG data from fbref.com | xPTS calculated after 20,000 Monte Carlo Simulations | https://github.com/TacticsBadger/MonteCarloFootballMatchSim/</sup>",
        'y':0.95,
        'x':0.50,
        'xanchor': 'center',
        'yanchor': 'top',
        'font_size': 18})
    fig.write_html(fig_name)