def generatePreferences(ws):
    """This function iterates over every row of the worksheet creating a comprehensive list with its values.
    -Maps a list with the alternatives with its value in a dictionary
    -Creates a list of tuples so tuples can be easily sorted.
    -First the list of tuples is ordered by the alternatives. So when two alternatives have the same value
    the alternative with higher rank will go first in order.
    -Then the list of tuples is ordered by the values, so the values with higher rank are first in order.
    -Once the list of tuples is ordered, a list of only the alternatives is created
    -This list is appended to the preference dictionary.

    Return a dictionary with agent and its corresponding list of preferences.
    
    Keyword arguments:
    ws -- data obtained from the openpyxl
    
    """
    preference_dict={}
    
    for i in range(1,ws.max_row+1):
        values= [ws.cell(row=i, column=x).value for x in range(1,len(ws[1])+1)]
        alternatives=[alt for alt in range(1,ws.max_column+1)]
        dictionary=dict(zip(alternatives,values))
        tuple_list=[(k,v) for k,v in dictionary.items()]
        tuple_list_ordered_by_key= sorted(tuple_list, key=lambda tup: tup[0], reverse=True)
        tuple_list_ordered_by_value= sorted(tuple_list_ordered_by_key, key=lambda tup: tup[1], reverse=True)
        single_list=[tuple_list_ordered_by_value[x][0] for x in range(0,len(tuple_list_ordered_by_value))]
        preference_dict[i]=single_list
    return preference_dict

def dictatorship(preferenceProfile,agent):
    """This function only checks if the agent selected actually exists in the preference profile dictionary.
    If it does, simply selects the winner directly from the dictionary.
    
    Return an integer as the winning alternative.
    
    Keyword arguments:
    preferenceProfile -- dictionary created by generatePreferences
    agent -- any agent (as long as it exists in the dictionary)
    """
    try:
        if agent not in preferenceProfile.keys():
            first_agent=str([agent for agent in preferenceProfile.keys()][0])
            last_agent= str([agent for agent in preferenceProfile.keys()][-1])
            raise ValueError('Invalid agent selected, please choose between '+ first_agent +' and '+ last_agent)
    except Exception as exp:
        print(exp)
    else:
        return preferenceProfile[agent][0]
    
def plurality(preferences,tieBreak):
    """This function creates a list with the most valued alternatives, that is the alternatives 
    in the first position of every agent.
    It counts the the most valued. Creates a list of the result of the count and passes this list to
    the points evaluation function.

    Return the result of the points evaluation fuction

    Keyword arguments:
    preferences -- dictionary created by generatePreferences
    tieBreak -- any integer (as long as it exists in the agents)

    """
    point_assignation=[0 for alt in range(1,len(preferences[1])+1)]
    
    for agent in preferences:
        point_assignation[preferences[agent][0]-1]+=1
            
    return pointsEvaluation(point_assignation,preferences,tieBreak)
    
def veto(preferences,tieBreak):
    """This function creates an array of zeros in the beginning, here the points for
    every alternative will be summed.
    It iterates through the preferences dictionary adding 1 point to each alternative (in the point assignation array)
    except for the last one in every agent. Then passes the point assignation array to the points evaluation function.

    Return the result of the points evaluation fuction

    Keyword arguments:
    preferences -- dictionary created by generatePreferences
    tieBreak -- any integer (as long as it exists in the agents)

    """
    point_assignation=[0 for alt in range(1,len(preferences[1])+1)]
    
    for agent in preferences:
        for position in preferences[agent][:-1]:
            point_assignation[position-1]+=1
            
    return pointsEvaluation(point_assignation,preferences,tieBreak)
                               
def borda(preferences,tieBreak):
    """This function creates an array of zeros in the beginning, here the points for
    every alternative will be summed.
    It iterates through the preferences dictionary and adds point the point assignation array. 
    Zero points to the least valued alternative, the next more valued alternative will get 1 point and so on until
    the most valued alternative will get one point less than the number of alternatives available.
    Then passes the point assignation array to the points evaluation function.

    Return the result of the points evaluation fuction

    Keyword arguments:
    preferences -- dictionary created by generatePreferences
    tieBreak -- any integer (as long as it exists in the agents)

    """
    
    point_assignation=[0 for alt in range(1,len(preferences[1])+1)]
    
    for agent in preferences:
        for pref_pos in preferences[agent]:
            position=preferences[agent][pref_pos-1]
            point_assignation[position-1]+= len(preferences[agent])-(pref_pos)
    return pointsEvaluation(point_assignation,preferences,tieBreak)

def harmonic(preferences,tieBreak):
    """This function creates an array of zeros in the beginning, here the points for
    every alternative will be summed.
    It iterates through the preferences dictionary and adds point the point assignation array. 
    The points will be assigned according to the number of alternatives available, 
    the most valued alternative will get 1 point, the second alternative will get 1/2 and so on
    until the last alternative will get 1/the number of alternatives.
    Then passes the point assignation array to the points evaluation function.

    Return the result of the points evaluation fuction

    Keyword arguments:
    preferences -- dictionary created by generatePreferences
    tieBreak -- any integer (as long as it exists in the agents)

    """
    
    point_assignation=[0 for alt in range(1,len(preferences[1])+1)]
    
    for agent in preferences:
        for pref_pos in preferences[agent]:
            position=preferences[agent][pref_pos-1]
            point_assignation[position-1]+= 1/(pref_pos)
            
    return pointsEvaluation(point_assignation,preferences,tieBreak)
    
def scoringRule(preferences,scoreVector,tieBreak):
    """
    This function creates an array of zeros in the beginning, here the points for
    every alternative will be summed.
    Then takes the scoreVector from the user and orders it in descending way,so the value with the highest rank
    appears first.
    It iterates through every agent and every alternative in the agent, assigning the hihgest value in the
    scoreVector to the most valued alternative, the second highest value in the vector to the second most valued
    alternative by the agent and so on until it assigns the lowest value in the vector to the least valued
    alternative by the agent.
    It passes the array that contains the points of the alternatives to the points evaluation function.
    
    Return an integer that is the winner

    Keyword arguments:
    preferences -- dictionary created by generatePreferences
    scoreVector -- a list of values with the same length that the number of alternatives
    tieBreak -- any integer (as long as it exists in the agents)

    """
    try:
        if len(scoreVector) != len(preferences[1]):
            raise ValueError('Invalid scoreVector, vector length must be'+ str(len(preferences[1]) ))
    except Exception as exp:
        return (exp)
    else:


        point_assignation=[0 for alt in range(1,len(preferences[1])+1)]
        ordered_scoreVector= sorted(scoreVector, reverse=True)
        sV_index=0
        
        for agent in preferences:
            sV_index=0
            for pref_pos in preferences[agent]:
                point_assignation[pref_pos-1]+= ordered_scoreVector[sV_index]
                sV_index+=1
                
        return pointsEvaluation(point_assignation,preferences,tieBreak)

def rangeVoting(values,tieBreak):
    """
    This function generates the preferences dictionary from the values inputted. Creates an
    empty list to assign the points fo each alternative. It sums the points of every alternative
    and appends them to the points assignation list. Then it passes the points assignation list 
    to the points evaluation function.

    Return an integer that is the winner

    Keyword arguments:
    values -- data obtained from the openpyxl
    tieBreak -- any integer (as long as it exists in the agents)  

    """
    preferences=generatePreferences(values)
    point_assignation=[]
    for alternative in range(1,values.max_column+1):
        col_values= sum([values.cell(row=x, column=alternative).value for x in range(1,values.max_row+1)])
        point_assignation.append(col_values)
    
    return pointsEvaluation(point_assignation,preferences,tieBreak)
    
def STV(preferences,tieBreak):
    """This function enters in a while loop that looks for the alternatives that either
    do not appear in the first position or are the least frequent in the first position.
    Creates a new preferences dictionary that does not include the alternatives that either
    do not appear in the first position or are the least frequent in the first position.
    After creating the new dictionary it enter the loop repeatedly. It exits the loop when 
    the preferences of the agents are empty. It evaluates the first position right before it
    gets empty, if only one alternative was contained that is the winner if more than one
    were contained there is a tie and tieBreaking conditions will be used.

    Return an integer that is the winner

    Keyword arguments:
    preferences -- dictionary created by generatePreferences
    tieBreak -- any integer (as long as it exists in the agents)

    """

    from collections import Counter
    initial_preferences=preferences.copy()
    
    flag=3
    while flag>1:

        alternatives=sorted([alt for alt in initial_preferences[1]],reverse=False)
        first_position=[ initial_preferences[i][0] for i in initial_preferences ]
        not_appear_first_position= [alt for alt in alternatives if alt not in first_position]
        
        
        first_position_count=Counter(first_position)
        first_position_single_list=[count for alt, count in first_position_count.items()]
        min_count=min(first_position_single_list)
        first_position_count_tuples=[(alt, count) for alt, count in first_position_count.items()]
        least_frequent_first_position=[alt for (alt, count) in first_position_count_tuples if count== min_count]
    
        new_preferences={}
        if len(not_appear_first_position)>0:
            for agent in preferences:
                new_rank=[alt for alt in initial_preferences[agent] if alt not in not_appear_first_position]
                new_preferences[agent]=new_rank
        else:
            for agent in preferences:
                new_rank=[alt for alt in initial_preferences[agent] if alt not in least_frequent_first_position]
                new_preferences[agent]=new_rank
        
        
        initial_preferences=new_preferences.copy()
        flag=len(new_preferences[1])
         
        
        if len(new_preferences[1])==0:
            break
        
        new_first_position=[ new_preferences[i][0] for i in new_preferences ]
        new_first_position_count=Counter(new_first_position)
    
    winning_alternatives_tuples=[(alt,count) for (alt,count) in new_first_position_count.items()]
    winning_alternatives_tuples_ordered_by_count= sorted(winning_alternatives_tuples, key=lambda tup: tup[1], reverse=True)   
        
    if len(winning_alternatives_tuples_ordered_by_count)==1:
        
        winner=winning_alternatives_tuples_ordered_by_count[0][0]
        return winner
    else:
        
        winning_alternatives_tuples_ordered_by_alternative= sorted(winning_alternatives_tuples, key=lambda tup: tup[0], reverse=True)   
        
        if tieBreak == 'max':
            
            return winning_alternatives_tuples_ordered_by_alternative[0][0]
        
        elif tieBreak == 'min':
            return winning_alternatives_tuples_ordered_by_alternative[-1][0]
        
        else:
            try:
                if tieBreak not in preferences.keys():
                    first_agent=str([agent for agent in preferences.keys()][0])
                    last_agent= str([agent for agent in preferences.keys()][-1])
                    raise ValueError('Invalid agent selected, please choose between '+ first_agent +' and '+ last_agent)
            except Exception as exp:
                print(exp)
            
            else:
                winning_alternatives=[alt for (alt,points) in winning_alternatives_tuples]
                for votes in preferences[tieBreak]:
                    if votes in winning_alternatives:
                        return votes
        
def pointsEvaluation(point_assignation,preferences,tieBreak):
    """This function takes a list called point assignation determined returned by the
    voting rule function (scoringRule,plurality, veto, borda, harmonic) and obtains the maximum points 
    the alternatives obtained.
    Checks if the maximum is repeated. If the max is not repeated that means ther is only one winner.
    If the max is repeated, there is a tie, and calls a tieBreak function.
    
    Return an integer as the winner (if no tie)

    Keyword arguments:
    point_assignation -- list of the points for every alternative created by voting functions
    preferences -- dictionary created by generatePreferences
    tieBreak -- any integer (as long as it exists in the agents)
    """
    max_points=max(point_assignation)
    max_repeated=[x for x in point_assignation if x==max_points]
    points_tuple=[(alt+1, point_assignation[alt]) for alt in range(0,len(point_assignation)) ]
    points_tuple_ordered_by_points= sorted(points_tuple, key=lambda tup: tup[1], reverse=True)
    if len(max_repeated)==1:     
        winner=points_tuple_ordered_by_points[0][0]
        return winner
    else:
        return tieBreaking(tieBreak,preferences,points_tuple,max_points)
    
def tieBreaking(tieBreak,preferences,points_tuple,max_points):
    """This function determines the winning alternatives, a list of tuples with 
    the alternatives that reached the maximum points as well as its points.
    If 'max' is selected as tieBreak the winner is the alternative with highest rank.
    If 'min' is selected as tieBreak the winner is the alternative with lowest rank.
    If neither 'max' or 'min' is selected it checks if the tieBreaker is an agent (is contained in the keys of the preferences),
    in the case that the tieBreaker is not an agent an exception is raised.
    If the numerical tieBreaker is an agent the function iterates through the elements contained in the agent preferences and when 
    it finds one that is the winning alternatives list that is the winner (the first one it finds is the hight rank of preferences of
    that agent)

    Return an integer as the winner.

    Keyword arguments:
    tieBreak -- any integer (as long as it exists in the agents)  
    preferences -- dictionary created by generatePreferences
    points_tuple -- list of tuples containing every alternative and its points created by points evaluation
    max_points_list -- maximum of points reached by alternatives
    
    """

    winning_alternatives_tuples=[(alt,count) for (alt,count) in points_tuple if count== max_points]
    winning_alternatives_tuples_ordered_by_alternative= sorted(winning_alternatives_tuples, key=lambda tup: tup[0], reverse=True)   
        
    if tieBreak == 'max':
          
        return winning_alternatives_tuples_ordered_by_alternative[0][0]
        
    elif tieBreak == 'min':
        return winning_alternatives_tuples_ordered_by_alternative[-1][0]
    else:
        try:
            if tieBreak not in preferences.keys():
                first_agent=str([agent for agent in preferences.keys()][0])
                last_agent= str([agent for agent in preferences.keys()][-1])
                raise ValueError('Invalid agent selected, please choose between '+ first_agent +' and '+ last_agent)
        except Exception as exp:
            return(exp)
        else:
                
            winning_alternatives=[alt for (alt,count) in points_tuple if count== max_points]
                
            for votes in preferences[tieBreak]:
                if votes in winning_alternatives:
                    return votes
