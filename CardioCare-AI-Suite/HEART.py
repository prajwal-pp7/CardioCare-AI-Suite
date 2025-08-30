import numpy as np
import pickle
import streamlit as st
import pandas as pd
import os
import random

st.set_page_config(
    page_title="CardioCare AI Suite",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

RECORDS_FILE='patient_records.csv'

def load_records_df():
    if os.path.exists(RECORDS_FILE):
        return pd.read_csv(RECORDS_FILE)
    else:
        return pd.DataFrame(columns=['Patient ID','Patient Name','Contact Info','Age','Sex','Prediction Result','Confidence Score'])

def save_records_df(df):
    df.to_csv(RECORDS_FILE,index=False)

@st.cache_resource
def load_model():
    model_filename="PROM_model.pkl"
    try:
        with open(model_filename,"rb") as file:
            model=pickle.load(file)
        return model
    except FileNotFoundError:
        st.error(f"FATAL ERROR: Model file '{model_filename}' not found. The app cannot function.")
        return None

model = load_model()

def page_home():
    st.title("Welcome to CardioCare AI Hospital")
    st.markdown("#### Your trusted partner in advanced")
    st.markdown("---")
    try:
        st.image("image_cac28b.jpg",use_column_width='auto') 
        st.success("Use the navigation menu on the left to access our tools and information.")
    except FileNotFoundError:
        st.error("Error: The hospital image ('image_cac28b.jpg') was not found. Please make sure it's in the project folder.")

def page_prediction():
    st.title("❤️ Heart Health Prediction Tool")
    st.markdown("Enter patient data below to generate a risk assessment.")
    st.markdown("---")
    col1, col2, col3=st.columns(3)
    with col1:
        age=st.slider("Age",1,100,50)
        sex=st.radio("Sex",("Male","Female"))
        cp=st.selectbox("Chest Pain Type",("Typical Angina","Atypical Angina","Non-Anginal Pain","Asymptomatic"))
    with col2:
        trestbps=st.slider("Resting Blood Pressure (mm Hg)",90,200,120)
        chol=st.slider("Serum Cholesterol (mg/dl)",120,570,240)
        fbs=st.radio("Fasting Blood Sugar > 120 mg/dl", ("No","Yes"))
    with col3:
        restecg=st.selectbox("Resting ECG",("Normal","ST-T Wave Abnormality","Left Ventricular Hypertrophy"))
        thalach=st.slider("Max Heart Rate Achieved",70,220,150)
        exang=st.radio("Exercise Induced Angina",("No","Yes"))
    with st.expander("Advanced Clinical Inputs"):
        adv_col1, adv_col2,adv_col3=st.columns(3)
        with adv_col1:
            oldpeak=st.number_input("ST Depression (Oldpeak)",0.0,6.2,1.0,0.1)
        with adv_col2:
            slope=st.selectbox("Slope of Peak Exercise ST Segment",("Upsloping","Flat","Downsloping"))
            ca=st.selectbox("Major Vessels Colored by Fluoroscopy",(0, 1, 2, 3, 4))
        with adv_col3:
            thal=st.selectbox("Thalassemia Stress Test", (0, 1, 2, 3), help="1: Normal, 2: Fixed Defect, 3: Reversible Defect")
    if st.button("Analyze Patient Data",type="primary",use_container_width=True):
        if model is None: return
        sex_num=1 if sex== "Male" else 0
        fbs_num=1 if fbs== "Yes" else 0
        exang_num=1 if exang== "Yes" else 0
        cp_map={"Typical Angina": 0, "Atypical Angina": 1,"Non-Anginal Pain": 2,"Asymptomatic": 3}
        restecg_map={"Normal": 0, "ST-T Wave Abnormality": 1,"Left Ventricular Hypertrophy": 2}
        slope_map={"Upsloping": 0, "Flat": 1,"Downsloping": 2}
        user_input=np.array([[age,sex_num,cp_map[cp],trestbps,chol,fbs_num,restecg_map[restecg],thalach,exang_num,oldpeak,slope_map[slope],ca,thal]])
        prediction=model.predict(user_input)
        prediction_proba=model.predict_proba(user_input)
        disease_proba_index=np.where(model.classes_ == 1)[0][0]
        confidence=prediction_proba[0][disease_proba_index]*100
        result_text="High Risk" if prediction[0] == 1 else "Low Risk"
        st.session_state.last_prediction = {'Age': age,'Sex': sex,'Prediction Result': result_text,'Confidence Score': f"{confidence:.2f}%"}
        st.markdown("---"); st.header("Prediction Result")
        if result_text=="High Risk": st.error(f"High Risk of Heart Disease Detected (Confidence: {confidence:.2f}%)")
        else: st.success(f"Low Risk of Heart Disease Detected (Confidence: {100-confidence:.2f}%)")
    if 'last_prediction' in st.session_state:
        st.markdown("---"); st.subheader("Save Patient Record")
        with st.form("save_form"):
            patient_id=st.text_input("Patient ID"); patient_name=st.text_input("Patient Name"); contact_info=st.text_input("Patient Email or Phone")
            if st.form_submit_button("Save Record"):
                if not all([patient_id, patient_name, contact_info]): st.warning("Please fill all fields.")
                else:
                    df=load_records_df()
                    new_record={'Patient ID': patient_id, 'Patient Name': patient_name, 'Contact Info': contact_info, **st.session_state.last_prediction}
                    new_df=pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                    save_records_df(new_df)
                    st.success(f"Record for {patient_id} saved!")
                    del st.session_state.last_prediction

def page_records():
    st.title("📄 Patient Record Lookup")
    df=load_records_df()
    search_id=st.text_input("Enter Patient ID to Search")
    if st.button("Search"):
        if search_id:
            record=df[df['Patient ID']==search_id]
            if not record.empty:
                st.session_state.found_record=record.iloc[0].to_dict()
                st.session_state.otp=str(random.randint(100000, 999999))
                st.info(f"Record found. Verification OTP sent."); st.warning(f"**DEMO ONLY:** Your OTP is **{st.session_state.otp}**")
            else: st.error("No record found.")
        else: st.warning("Please enter a Patient ID.")
    if 'otp' in st.session_state:
        entered_otp=st.text_input("Enter the 6-digit OTP to view record")
        if st.button("Verify OTP"):
            if entered_otp==st.session_state.otp:
                st.success("Verification Successful!"); st.subheader(f"Record for Patient ID: {st.session_state.found_record['Patient ID']}"); st.json(st.session_state.found_record)
                del st.session_state.otp; del st.session_state.found_record
            else: st.error("Invalid OTP.")
    st.markdown("---"); st.subheader("All Saved Records")
    st.dataframe(df)

def page_doctors():
    st.title("🩺 Meet Our Cardiology Team")
    st.markdown("Our team of world-class cardiologists is dedicated to your health.")
    st.markdown("---")
    
    doctors_data = {
        "Doctor Name": ["Dr. Sandhya Singh","Dr. Aditi Singh","Dr. Priya Meena"],
        "Degree": ["MD, FACC", "MBBS, DM (Cardiology)","MD, PhD"],
        "Specialization": ["Chief of Cardiology, Interventional Cardiology","Electrophysiology","Preventive Cardiology"],
        "Timings": ["Mon-Fri (9 AM - 7 PM)","Mon, Wed, Fri (1 PM - 5 PM)","Tue, Thu (11 AM - 3 PM)"]
    }
    df_doctors = pd.DataFrame(doctors_data)
    df_doctors.index = range(1, len(df_doctors) + 1)
    st.table(df_doctors)

def page_locations():
    st.title("📍 Our Hospital Locations")
    st.markdown("Providing quality cardiac care across the region.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Main Campus (Aligarh)")
        st.markdown("""
        - **Address:** Aligarh, UP
        - **Phone:** +91 7721974793
        - **Services:** Full-service cardiac hospital, 24/7 Emergency
        """)
        map_data_main=pd.DataFrame({'lat':[27.9014],'lon':[78.0773]})
        st.map(map_data_main,zoom=12)
    with col2:
        st.subheader("Kanpur Heart Clinic (Replica)")
        st.markdown("""
        - **Address:** Moti Jheel
        - **Phone:** +91 7712797439
        - **Services:** Outpatient consultations, Diagnostic services
        """)
        map_data_replica=pd.DataFrame({'lat':[26.4724], 'lon':[80.3031]})
        st.map(map_data_replica, zoom=12)

def page_contact():
    st.title("📞 Contact & Hours")
    st.markdown("---")
    
    st.header("CardioCare AI Hospital")
    st.markdown("""
    - **Head of Cardiology:** Dr. Sandhya Singh
    - **Institution:** CardioCare
    - **Address:** Aligarh, UP
    - **Phone:** +91 7721974793
    - **Email:** 210401@iitk.ac.in
    """)
    
    st.header("Operating Hours")
    st.markdown("""
    - **Monday - Friday:** 8:00 AM - 10:00 PM
    - **Saturday:** 9:00 AM - 9:00 PM
    - **Sunday:** Closed
    - **Emergency Services:** 24/7
    """)

def main():
    st.sidebar.image("logo.jpg", width=250)
    st.sidebar.title("Navigation Menu")
    page_options = ["Home", "Heart Disease Prediction","Patient Record Lookup","Meet Our Doctors","Hospital Locations","Contact & Hours"]
    page = st.sidebar.radio("Go to", page_options)

    st.sidebar.subheader("Project Resources")
    st.sidebar.markdown("- [View Source on GitHub](https://github.com/prajwal-pp7/CardioCare-AI-Suite)")
    
    pages = {
        "Home": page_home,
        "Heart Disease Prediction": page_prediction,
        "Patient Record Lookup": page_records,
        "Meet Our Doctors": page_doctors,
        "Hospital Locations": page_locations,
        "Contact & Hours": page_contact
    }
    pages[page]()

if __name__ == '__main__':
    main()