import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle

# pickle_in = open('logisticRegr.pkl', 'rb')
# classifier = pickle.load(pickle_in)

st.sidebar.header('Course Recommendation')
select = st.sidebar.selectbox('Select Form', ['Form 1'], key='2')
if not st.sidebar.checkbox("Hide", True, key='2'):
    st.title('Course Recommandation System')
    # Coursename = st.text_input("Name:")
    Coursename = st.selectbox('Select the Course', ('Embedded and Real Time Operating Systems(Youtube)',
           'CompTIA A+ (220-1002): Cert Prep 5 Troubleshooting Operating Systems (Linkedln Learning)',
           'Introduction to Operating Systems(Udacity)',
           'Embedded Hardware and Operating Systems(Coursera)',
           'Operating Systems(SWAYAM)', 'Advanced Operating Systems(Udacity)',
           'Getting Started with Junos Operating System(Coursera)',
           'Become a Master of Operating Systems at comfort of your Home (Udemy)',
           'Operating System(Youtube -GateSmasher)',
           'Operating Systems Concept and Design Principles for Beginner(Udemy)',
           'Cybersecurity Roles and Operating System Security(EDX)',
           'SCCM Current Branch: Deploy and Maintain Operating Systems(Pluralsight)',
           'Windows Operating Systems for CompTIA A+ (220-902)(Pluralsight)',
           'Introduction to Operating Systems(Swayam)',
           'Configuration Manager: Maintain Inventory and Operating Systems(Linkedln Learning)',
           'Computer Hardware and Operating Systems(EDX)',
           'Operating System(Udemy)',
           'Juniper Networks JNCIA-Junos: Junos Operating System Fundamentals(PluralaSight)',
           'Operating Systems from scratch - Part 2(Udemy)',
           'Linux Operating System Fundamentals(Udemy)',
           'Real Time Operating System(SWAYAM)',
           'Operating Azure Stack Hub(PLuralSight)',
           'Other Operating Systems & Technologies for CompTIA A+ (220-902)(Pluralsight)',
           'Operating Systems from scratch - Part 1(Udemy)',
           'Hello (Real) World with ROS – Robot Operating System(EDX)',
           'Operating Systems and You: Becoming a Power User(Coursera)',
           'Understanding Computer Systems(FutureLearn)',
           'Using Python to Interact with the Operating System(Coursera)',
           'Operating Running Systems(PluraSight)'))
    test1Score = st.number_input("Test 1 Score :")
    count1 = st.number_input("Test 1 Count :")
    test2Score = st.number_input("Test 2 Score :")
    count2 = st.number_input("Test 2 Count :")
    test3Score = st.number_input("Test 3 Score :")
    count3 = st.number_input("Test 3 Count :")
    # glucose = st.number_input("Plasma Glucose Concentration :")
    # bp =  st.number_input("Diastolic blood pressure (mm Hg):")
    # skin = st.number_input("Triceps skin fold thickness (mm):")
    # insulin = st.number_input("2-Hour serum insulin (mu U/ml):")
    # bmi = st.number_input("Body mass index (weight in kg/(height in m)^2):")
    # dpf = st.number_input("Diabetes Pedigree Function:")
    # age = st.number_input("Age:")

    submit = st.button('Recommend')

    if submit:
        test1 = pd.read_csv("Class1.csv")
        test2 = pd.read_csv("Class2.csv")
        test3 = pd.read_csv("Class3.csv")
        # df.rename(columns={'AssignmentOneCurrentScore': 'AssignmentOneAverage'}, inplace=True)
        # df.rename(columns={'AssignmentTwoCurrentScore': 'AssignmentTwoAverage'}, inplace=True)
        # df.rename(columns={'AssignmentThreeCurrentScore': 'AssignmentThreeAverage'}, inplace=True)
        # #df.head()

        t=(test1Score*count1+test2Score*count2+test3Score*count3)//(count1+count2+count3)
        if(t>=0 and t<=40):
            testdataframe=test1
        elif(t>=41 and t<=70):
            testdataframe=test2
        else:
            testdataframe=test3
        # dicti = {'Student ID': ['-123q'],
        #          'AssignmentOneAverage': [1],
        #          'AssignmentOneAttempt': [76],
        #          'AssignmentTwoAverage': [42],
        #          'AssignmentTwoAttempt': [2],
        #          'AssignmentThreeAverage': [76],
        #          'AssignmentThreeAttempt': [2],
        #          'Gender': [1],
        #          'Course': ["rgreereh"],
        #          'Rating': [7]
        #          }
        # class1 = pd.DataFrame(dicti)
        # class2 = pd.DataFrame(dicti)
        # class3 = pd.DataFrame(dicti)
        #
        # for i in range(0, 15000):
        #     t = df["AssignmentOneAverage"][i] * df["AssignmentOneAttempt"][i] + df["AssignmentTwoAverage"][i] * \
        #         df["AssignmentTwoAttempt"][i] + df["AssignmentThreeAverage"][i] * df["AssignmentThreeAttempt"][i]
        #     s = df["AssignmentOneAttempt"][i] + df["AssignmentTwoAttempt"][i] + df["AssignmentThreeAttempt"][i]
        #     q = t // s
        #     if (q >= 0 and q <= 40):
        #         class1.loc[len(class1.index)] = df.loc[i]
        #     elif (q >= 41 and q <= 70):
        #         class2.loc[len(class2.index)] = df.loc[i]
        #     else:
        #         class3.loc[len(class3.index)] = df.loc[i]
        #
        # class2 = class2.drop([0])
        # class1 = class1.drop([0])
        # #print(class2)

        course_ratingCount = (testdataframe.
            groupby(by=['Course'])['Rating'].
            count().
            reset_index().
            rename(columns={'Rating': 'totalRatingCount'})
        [['Course', 'totalRatingCount']]
            )
        course_ratingCount.tail()

        rating_with_totalRatingCount = testdataframe.merge(course_ratingCount, left_on='Course', right_on='Course', how='left')
        rating_with_totalRatingCount.head()

        popularity_threshold = 5
        rating_popular_course = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
        #rating_popular_course.head()

        # rating_popular_course.shape

        ## First lets create a Pivot matrix
        mapp = {}
        course_features_df = rating_popular_course.pivot_table(index='Course', columns='Student ID',
                                                               values='Rating').fillna(0)
        course_features_df.head()
        for i in range(0, len(course_features_df)):
            mapp[course_features_df.index[i]] = i

        from scipy.sparse import csr_matrix

        course_features_df_matrix = csr_matrix(course_features_df.values)

        from sklearn.neighbors import NearestNeighbors

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(course_features_df_matrix)
        #Coursename=str(Coursename)
        query_index = mapp[Coursename]
        # print(query_index)
        distances, indices = model_knn.kneighbors(course_features_df.iloc[query_index, :].values.reshape(1, -1),
                                                  n_neighbors=6)
        course_features_df.iloc[query_index, :].values.reshape(1, -1)

        for i in range(0, len(distances.flatten())):
            if i == 0:
                st.write('Recommendations for {0}:\n'.format(course_features_df.index[query_index]))
            else:
                st.write('{0}: {1}'.format(i, course_features_df.index[indices.flatten()[i]]))

