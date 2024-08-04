import streamlit as st
import pickle
import pandas as pd
import numpy as np

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions',
       'Rising Pune Supergiant', 'Royal Challengers Bangalore',
       'Kolkata Knight Riders', 'Delhi Daredevils', 'Kings XI Punjab',
       'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers',
       'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants',
       'Delhi Capitals']

venue = ['Rajiv Gandhi International Stadium, Uppal',
       'Maharashtra Cricket Association Stadium',
       'Saurashtra Cricket Association Stadium', 'Holkar Cricket Stadium',
       'M Chinnaswamy Stadium', 'Wankhede Stadium', 'Eden Gardens',
       'Feroz Shah Kotla',
       'Punjab Cricket Association IS Bindra Stadium, Mohali',
       'Green Park', 'Punjab Cricket Association Stadium, Mohali',
       'Sawai Mansingh Stadium', 'MA Chidambaram Stadium, Chepauk',
       'Dr DY Patil Sports Academy', 'Newlands', "St George's Park",
       'Kingsmead', 'SuperSport Park', 'Buffalo Park',
       'New Wanderers Stadium', 'De Beers Diamond Oval',
       'OUTsurance Oval', 'Brabourne Stadium',
       'Sardar Patel Stadium, Motera', 'Barabati Stadium',
       'Vidarbha Cricket Association Stadium, Jamtha',
       'Himachal Pradesh Cricket Association Stadium', 'Nehru Stadium',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'Subrata Roy Sahara Stadium',
       'Shaheed Veer Narayan Singh International Stadium',
       'JSCA International Stadium Complex', 'Sheikh Zayed Stadium',
       'Sharjah Cricket Stadium', 'Dubai International Cricket Stadium',
       'M. A. Chidambaram Stadium', 'Feroz Shah Kotla Ground',
       'M. Chinnaswamy Stadium', 'Rajiv Gandhi Intl. Cricket Stadium',
       'IS Bindra Stadium', 'ACA-VDCA Stadium']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

selected_city = st.selectbox('Select Venue',sorted(venue))

col11,col12,col13,col14 = st.columns(4)

st.write('First Innings Score')
with col11:
    score1 = st.number_input('Score',min_value=0,max_value=720)
with col12:
    overs1 = st.number_input('Overs',min_value=0,max_value=20)
with col13:
    balls1 = st.number_input('Balls',min_value=0,max_value=5)
with col14:
    wickets1 = st.number_input('Wickets',min_value=0,max_value=10)

st.write('Second Innings Score')
col3,col4,col5,col6 = st.columns(4)
with col3:
    score = st.number_input('Score ',min_value=0,max_value=score1+7)
with col4:
    overs = st.number_input('Overs ',min_value=0,max_value=20)
with col5:
    balls12 = st.number_input('Balls ',min_value=0,max_value=5)
with col6:
    wickets = st.number_input('Wickets ',min_value=0,max_value=9)

if st.button('Predict Probability'):
    if score==0:
            run_rate = (score1*6)/(overs1*6)+balls1
            target = score1+(run_rate*(20-overs1)*(0.11*(10-wickets1)))
            print(wickets1)
            balls_left = 119
            wickets_left = 10
            st.write(f'Target : {target}')
            score = 1
            balls = 1
            df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'venue':[selected_city],
                               'runs_left':[(np.round(target)-score)],'balls_left':[balls_left],
                               'wickets_left':[wickets_left]}
            )
            print(df.values)
            result = pipe.predict_proba(df)
            loss = result[0][0]
            win = result[0][1]
            st.header(bowling_team + "- " + str(round(win * 100)) + "%")
            st.header(batting_team + "- " + str(round(loss * 100)) + "%")
    else:
        runs_left = score1 - score
        balls_left = 120 - ((overs*6)+balls12)
        wickets = 10 - wickets
        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'venue':[selected_city],
                                 'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets]})
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(bowling_team + "- " + str(round(win*100)) + "%")
        st.header(batting_team + "- " + str(round(loss*100)) + "%")