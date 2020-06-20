from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse
import numpy as np
import pandas as pd
import csv , io

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            #messages.success(request,'You are looged in')
            return redirect ('dashboard')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect ('login')    
            
    else:
        return render(request,'accounts/login.html')    
        

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        min_length = 8

        if len(password) < min_length:
            messages.error(request,'Password length must be greater than 8')
            return redirect ('register')
            

        # check for digit
        if not any(char.isdigit() for char in password):
            messages.error(request,'Password must contain atleast 1 digit')
            return redirect ('register')
           

        # check for letter
        if not any(char.isalpha() for char in password):
            messages.error(request,'Password must contain atleast 1 letter')
            return redirect ('register')

          

        if password == password2:

            if User.objects.filter(username = username).exists():
                messages.error(request,'Username already exixts')
                return redirect ('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request,'Email already exixts')
                    return redirect ('register')
                else:
                    user = User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
                    user.save()
                    messages.success(request, ' You are successfully registered')
                    return redirect('login')   
        else:
            messages.error(request,'Password do not match')
            return redirect('register')
        
    else:
        return render(request,'accounts/register.html') 
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        #messages.success(request,'You are logged out')
        return redirect('index')

def dashboard(request):
    if request.method == 'POST':
        x = request.POST['team1']
        y = request.POST['team2']
        import pandas as pd
        fifa_df = pd.read_csv('data.csv')
         
        #data_html = data.to_html()

        useful_features = ['Name',
                   'Age',
                   'Photo', 
                   'Nationality', 
                   'Flag',
                   'Overall',
                   'Potential', 
                   'Club', 
                   'Club Logo', 
                   'Value',
                   'Wage',
                   'Preferred Foot',
                   'International Reputation',
                   'Weak Foot',
                   'Skill Moves',
                   'Work Rate',
                   'Body Type',
                   'Position',
                   'Joined', 
                   'Contract Valid Until',
                   'Height',
                   'Weight',
                   'Crossing', 
                   'Finishing',
                   'HeadingAccuracy',
                   'ShortPassing', 
                   'Volleys', 
                   'Dribbling',
                   'Curve',
                   'FKAccuracy',
                   'LongPassing',
                   'BallControl',
                   'Acceleration',
                   'SprintSpeed',
                   'Agility',
                   'Reactions', 
                   'Balance',
                   'ShotPower', 
                   'Jumping',
                   'Stamina', 
                   'Strength',
                   'LongShots',
                   'Aggression',
                   'Interceptions',
                   'Positioning', 
                   'Vision', 
                   'Penalties',
                   'Composure',
                   'Marking',
                   'StandingTackle', 
                   'SlidingTackle',
                   'GKDiving',
                   'GKHandling',
                   'GKKicking',
                   'GKPositioning',
                   'GKReflexes']


        df = pd.DataFrame(fifa_df , columns = useful_features)

        team1 = df.loc[(df['Club'] == x) & (df['Overall'] >= 70)]

        team2 = df.loc[(df['Club'] == y) & (df['Overall'] >= 70)]

        dream_team = team1.append(team2, ignore_index=True)

        goalKeeper = dream_team.loc[(dream_team['Position'] == 'GK')] [['Name', 'GKDiving' , 'GKHandling' , 'GKKicking' , 'GKPositioning','GKReflexes']]

        x = goalKeeper.mean(axis=1)

        player_features = ['Crossing', 'Finishing', 'HeadingAccuracy',
       'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
       'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed',
       'Agility', 'Reactions', 'Balance', 'ShotPower', 'Jumping',
       'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
       'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking',
       'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
       'GKKicking', 'GKPositioning', 'GKReflexes']

        df_postion  = pd.DataFrame()  # This will create empty pandas dataframe.

        for position_name, features in dream_team.groupby(dream_team['Position'])[player_features].mean().iterrows():
            top_features = dict(features.nlargest(5))
            df_postion[position_name] = tuple(top_features)
        df_postion.head()

        posi = []
        player = []
        club_l = []

        for col in df_postion.columns:
            tmp_df = pd.DataFrame()
            #print(col)
            
            l = [df_postion[col].values]
            #print(l)       #sare columns ki values ek array mai aa gyi
            
            l = l[0] 
            #print(l)
            
            l = list(l) # isse l list ban gyi
            #print(l)
            
            l.append('Name')  #sari rows mai ek feature aur add kiya name
            #print(l)
            
            tmp_df = pd.DataFrame.copy(dream_team[dream_team['Position'] == col][l])
            
            #print(tmp_df)
            
            
            tmp_df['mean'] = np.mean(tmp_df.iloc[: , :-1] , axis = 1)
            #print(tmp_df) #players ki key features ka mean nikala hai
            
            
            name = tmp_df['Name'][tmp_df['mean'] == tmp_df['mean'].max()].values[0]
            #print(name)  #har position pr maximum mean wala player print hoga(total 27 honge).
            
            
            club = df['Club'][df['Name'] == str(name)].values[0]
            #print(club)    #club name of above selected players
            
            posi.append(col)
            
            
            player.append(name)

            
            club_l.append(club)
            #print('{0} \nClub : {1}'.format(name ,club ) )
            
            
        
        gk = ['GK']
        forward = ['LS', 'ST', 'RS','LF', 'CF', 'RF','LW','RW']
        midfeilder = ['LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM',
                    'RCM', 'RM', 'LDM', 'CDM', 'RDM' ]
        defenders = ['LWB','RWB', 'LB', 'LCB', 'CB','RCB','RB']

        
        name = []
        position = []
        club = []
        #goal_keeper = []
        #striker = []
        #midfield = []
        #backline = []
        
        for p , n , c in zip(posi , player , club_l):
            if p in gk:
                name.append(n)
                position.append(p)
                club.append(c)
                #goal_keeper.append(n)
                #goal_keeper.append(p)
                #goal_keeper.append(c)
        
        for p , n , c in zip(posi , player , club_l):
            if p in forward:
                name.append(n)
                position.append(p)
                club.append(c)
                #striker.append(n)
                #striker.append(p)
                #striker.append(c)
        
        for p , n , c in zip(posi , player , club_l):
            if p in midfeilder:
                name.append(n)
                position.append(p)
                club.append(c)
                #midfield.append(n)
                #midfield.append(p)
                #midfield.append(c)
                
                
        
        for p , n , c in zip(posi , player , club_l):
            if p in defenders:
                name.append(n)
                position.append(p)
                club.append(c)
                #backline.append(n)
                #backline.append(p)
                #backline.append(c)
        
        
        return render(request, 'accounts/dashboard.html', {'final_team':zip(name,position,club)})
        #return render(request, 'accounts/dashboard.html', {'goal_keeper':goal_keeper, 'striker':striker, 'midefield':midfield,'backline':backline})         

                
        
    return render(request,'accounts/dashboard.html')