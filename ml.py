import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Page config for a 'cute' look
st.set_page_config(page_title='Student Success Predictor', page_icon='🎓', layout='centered')

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 20px; }
    .reportview-container .main .block-container{ padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title('🎓 Student Performance AI')
st.markdown('### Predictive Insights & Performance Dashboard')

# Load Model
model = joblib.load('best_student_model.pkl')

# Sidebar Info
st.sidebar.header('📊 Model Stats')
st.sidebar.info('**Best Model:** XGBoost\n**R² Score:** 0.8613\n**MAE:** 4.82')
st.sidebar.markdown('---')
st.sidebar.write('Top Features Used:')
st.sidebar.caption('Study Hours, Mental Health, Attendance, Social Media, Sleep, Exercise')

tabs = st.tabs(['🚀 Prediction Prototype', '📈 Model Details'])

with tabs[0]:
    st.subheader('Test the Model')
    st.write('Enter student habits below to predict their final exam score.')

    col1, col2 = st.columns(2)
    with col1:
        study = st.slider('Study Hours/Day', 0.0, 10.0, 4.0)
        mental = st.slider('Mental Health Rating (1-10)', 1, 10, 5)
        attendance = st.slider('Attendance %', 0, 100, 85)
    with col2:
        social = st.slider('Social Media Hours', 0.0, 10.0, 2.0)
        sleep = st.slider('Sleep Hours', 0.0, 12.0, 7.0)
        exercise = st.slider('Exercise Frequency (Days/Week)', 0, 7, 3)

    if st.button('Predict Exam Score'):
        input_data = np.array([[study, mental, attendance, social, sleep, exercise]])
        prediction = model.predict(input_data)[0]

        st.success(f'### Predicted Exam Score: {prediction:.2f}')
        
        # Risk Score Logic
        if prediction < 40:
            risk_level = "High Risk ⚠️"
            risk_desc = "High probability of failure. Immediate intervention recommended."
            risk_color = "red"
        elif prediction < 60:
            risk_level = "Medium Risk 🟠"
            risk_desc = "Student needs improvement to ensure passing."
            risk_color = "orange"
        elif prediction < 80:
            risk_level = "Low Risk 🟢"
            risk_desc = "Student is performing well but has room for growth."
            risk_color = "blue"
        else:
            risk_level = "Safe / Excellent 🌟"
            risk_desc = "Outstanding performance predicted!"
            risk_color = "green"
            st.balloons()

        st.markdown(f"**Risk Level:** :{risk_color}[{risk_level}]")
        st.info(risk_desc)

with tabs[1]:
    st.subheader('Why this model works?')
    st.write('The **Ensemble Mixed** strategy selected 6 key features that balanced statistical dependency and correlation.')
    st.json({
        'Algorithm': 'XGBoost Regression',
        'Optimization': 'GridSearchCV',
        'Selected_Features': ['study_hours_per_day', 'mental_health_rating', 'attendance_percentage', 'social_media_hours', 'sleep_hours', 'exercise_frequency']
    })

