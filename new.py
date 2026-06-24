import pandas as pd
import numpy as np

def generate_eye_patient_dataset(num_records=10000):

    np.random.seed(42)

    patient_ids = [f'EP{i:06d}' for i in range(1, num_records + 1)]

    age = np.random.randint(5, 90, num_records)

    gender = np.random.choice(
        ['Male', 'Female', 'Other'],
        num_records,
        p=[0.48, 0.48, 0.04]
    )

    vision_left = np.round(np.random.uniform(0.1, 1.5, num_records), 1)
    vision_right = np.round(np.random.uniform(0.1, 1.5, num_records), 1)

    screen_time = np.round(np.random.uniform(1, 14, num_records), 1)

    eye_pressure = np.random.randint(10, 31, num_records)

    eye_disease = np.random.choice(
        ['None', 'Cataract', 'Glaucoma', 'Dry Eye', 'Myopia'],
        num_records,
        p=[0.40, 0.15, 0.10, 0.15, 0.20]
    )

    glasses = np.random.choice(
        ['Yes', 'No'],
        num_records,
        p=[0.65, 0.35]
    )

    surgery_history = np.random.choice(
        ['Yes', 'No'],
        num_records,
        p=[0.15, 0.85]
    )

    eye_strain = np.random.randint(1, 11, num_records)

    def risk_category(row):
        risk = 0

        if row['Eye_Pressure'] > 21:
            risk += 2

        if row['Eye_Disease'] in ['Glaucoma', 'Cataract']:
            risk += 2

        if row['Screen_Time_Hours'] > 8:
            risk += 1

        if row['Eye_Strain_Level'] > 7:
            risk += 1

        if risk <= 2:
            return "Low"
        elif risk <= 4:
            return "Medium"
        else:
            return "High"

    df = pd.DataFrame({
        'Patient_ID': patient_ids,
        'Age': age,
        'Gender': gender,
        'Vision_Left_Eye': vision_left,
        'Vision_Right_Eye': vision_right,
        'Screen_Time_Hours': screen_time,
        'Eye_Pressure': eye_pressure,
        'Eye_Disease': eye_disease,
        'Uses_Glasses': glasses,
        'Surgery_History': surgery_history,
        'Eye_Strain_Level': eye_strain
    })

    df['Risk_Category'] = df.apply(risk_category, axis=1)

    return df


if __name__ == "__main__":

    print("Generating Eye Patient Dataset...")

    dataset = generate_eye_patient_dataset(10000)

    print(dataset.head())

    import os
    os.makedirs("dataset", exist_ok=True)

    dataset.to_excel("dataset/eye_patient_dataset.xlsx", index=False)

    print("Eye Patient Dataset saved successfully!")