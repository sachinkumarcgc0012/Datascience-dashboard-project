import os
from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

def load_and_preprocess_data():
    # Update filename to match your eye patient dataset file layout
    dataset_path = os.path.join(app.root_path, 'dataset', 'eye_patient_dataset.xlsx')
    
    # Reading excel (if your application processes the CSV conversion directly, use pd.read_csv)
    if not os.path.exists(dataset_path) and os.path.exists(dataset_path.replace('.xlsx', '.csv')):
        df = pd.read_csv(dataset_path.replace('.xlsx', '.csv'))
    else:
        df = pd.read_excel(dataset_path)
        
    # Remove duplicates
    df = df.drop_duplicates()
    # Handle missing values
    df = df.dropna()
    # Normalize string columns for consistent filtering
    string_columns = df.select_dtypes(include=['object']).columns
    df[string_columns] = df[string_columns].apply(lambda x: x.str.strip())
    return df

def calculate_summary_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Ensure there's data before calling numeric summary aggregations
    if df.empty:
        return {metric: {col: 0 for col in numeric_cols} for metric in ['mean', 'median', 'max', 'min', 'std']}
        
    summary = {
        'mean': df[numeric_cols].mean().to_dict(),
        'median': df[numeric_cols].median().to_dict(),
        'max': df[numeric_cols].max().to_dict(),
        'min': df[numeric_cols].min().to_dict(),
        'std': df[numeric_cols].std().to_dict()
    }
    return summary

def calculate_kpis(df):
    if df.empty:
        return {
            'total_patients': 0, 'avg_screen_time': 0, 'avg_eye_pressure': 0,
            'avg_eye_strain': 0, 'avg_vision_left': 0, 'avg_vision_right': 0
        }
        
    kpis = {
        'total_patients': len(df),
        'avg_screen_time': round(df['Screen_Time_Hours'].mean(), 1),
        'avg_eye_pressure': round(df['Eye_Pressure'].mean(), 1),
        'avg_eye_strain': round(df['Eye_Strain_Level'].mean(), 1),
        'avg_vision_left': round(df['Vision_Left_Eye'].mean(), 2),
        'avg_vision_right': round(df['Vision_Right_Eye'].mean(), 2)
    }
    return kpis

@app.route('/')
def index():
    # Load data
    df = load_and_preprocess_data()
    
    # Get filters from request matching the eye health dataset parameters
    gender_filter = request.args.get('gender', '')
    age_min = request.args.get('age_min', '')
    age_max = request.args.get('age_max', '')
    eye_disease_filter = request.args.get('eye_disease', '')
    risk_category_filter = request.args.get('risk_category', '')
    uses_glasses_filter = request.args.get('uses_glasses', '')
    surgery_history_filter = request.args.get('surgery_history', '')
    screen_min = request.args.get('screen_min', '')
    screen_max = request.args.get('screen_max', '')
    
    # Apply filters
    filtered_df = df.copy()
    
    if gender_filter:
        filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]
    if age_min:
        filtered_df = filtered_df[filtered_df['Age'] >= int(age_min)]
    if age_max:
        filtered_df = filtered_df[filtered_df['Age'] <= int(age_max)]
    if eye_disease_filter:
        filtered_df = filtered_df[filtered_df['Eye_Disease'] == eye_disease_filter]
    if risk_category_filter:
        filtered_df = filtered_df[filtered_df['Risk_Category'] == risk_category_filter]
    if uses_glasses_filter:
        filtered_df = filtered_df[filtered_df['Uses_Glasses'] == uses_glasses_filter]
    if surgery_history_filter:
        filtered_df = filtered_df[filtered_df['Surgery_History'] == surgery_history_filter]
    if screen_min:
        filtered_df = filtered_df[filtered_df['Screen_Time_Hours'] >= float(screen_min)]
    if screen_max:
        filtered_df = filtered_df[filtered_df['Screen_Time_Hours'] <= float(screen_max)]
    
    # Calculate KPIs and summary stats
    kpis = calculate_kpis(filtered_df)
    summary_stats = calculate_summary_stats(filtered_df)
    
    # Get top 20 records
    top_records = filtered_df.head(20).to_dict('records')
    
    # Get unique values for dropdown filters from the master dataset
    genders = sorted(df['Gender'].unique())
    eye_diseases = sorted(df['Eye_Disease'].unique())
    risk_categories = sorted(df['Risk_Category'].unique())
    
    return render_template('index.html',
                           kpis=kpis,
                           summary_stats=summary_stats,
                           top_records=top_records,
                           genders=genders,
                           eye_diseases=eye_diseases,
                           risk_categories=risk_categories,
                           filters={
                               'gender': gender_filter,
                               'age_min': age_min,
                               'age_max': age_max,
                               'eye_disease': eye_disease_filter,
                               'risk_category': risk_category_filter,
                               'uses_glasses': uses_glasses_filter,
                               'surgery_history': surgery_history_filter,
                               'screen_min': screen_min,
                               'screen_max': screen_max
                           })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)