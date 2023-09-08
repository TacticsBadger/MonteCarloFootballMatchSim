# Copyright   : @TacticsBadger, TacticsNotAntics: https://tacticsnotantics.org
# Version 1.0 : November 17, 2021
# Last Updated: January 08, 2022
'''
Brief: Monte Carlo simulations for predicting match outcomes.
Needs user input: keyboard or csv. 
'''
import sys
import math
import time
import pandas as pd
import numpy as np
from prettytable import PrettyTable

print("***************** Tactics Not Antics ******************")
print("*****          Monte Carlo Match Simulator        *****")
print("*****        Version 1.0: November 17, 2021       *****")
print("*****        Last Update: January  08, 2021       *****")
print("*******************************************************")
print("******************* PL TEAMS 2021-22 ******************")
print("* Arsenal | Aston Villa | Brentford     | Brighton    *")
print("* Burnley | Chelsea     | Crystal Palace| Everton     *")
print("* Leeds   | Leicester   | Liverpool     | Man City    *")
print("* Man Utd | Newcastle   | Norwich City  | Southampton *")
print("* West Ham| Tottenham   | Watford       | Wolves      *")
print("*******************************************************")

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
    print ("Reading data from csv file.")
    csv_filename = input("* Add csv filename: ")
    df = pd.read_csv(csv_filename)
    print("**********************************")
    for i in range(0, len(df)):
        print("* Game #", i+1, "*")
        print("* Home team:", df.iloc[i]['Team-H'])
        print("* Away team:", df.iloc[i]['Team-A'])
        print("* Home team xG:", df.iloc[i]['xG-H'])
        print("* Away team xG:", df.iloc[i]['xG-A'])
        input_home_team = df.iloc[i]['Team-H']
        input_home_team_xg = df.iloc[i]['xG-H']
        input_away_team = df.iloc[i]['Team-A']
        input_away_team_xg = df.iloc[i]['xG-A']
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
        print("**********************************")
        result_tuple_csv = (input_home_team, round(home_win_probability,2), round(home_xPts,2), input_away_team, round(away_win_probability,2), round(away_xPts,2), "\n")
        with open("MonteCarloMatchSimResults.csv", "a+") as myfile:
            myfile.write(",".join(map(str, result_tuple_csv)))
else:
    print("Not a valid option. Exiting.")
    sys.exit()



