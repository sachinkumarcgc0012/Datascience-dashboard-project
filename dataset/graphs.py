import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Dataset
def load_data():
    df = pd.read_excel("dataset/eye_patient_dataset.xlsx")

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove missing values
    df = df.dropna()

    return df


# Generate Graphs
def generate_all_graphs(df):

    sns.set_style("whitegrid")

    # Create folder for graphs
    os.makedirs("graphs", exist_ok=True)

    # 1. Gender Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Gender")
    plt.title("Gender Distribution")
    plt.savefig("graphs/gender_distribution.png")
    plt.close()

    # 2. Age Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Age"], bins=20, kde=True)
    plt.title("Age Distribution")
    plt.savefig("graphs/age_distribution.png")
    plt.close()

    # 3. Eye Disease Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x="Eye_Disease")
    plt.title("Eye Disease Distribution")
    plt.xticks(rotation=45)
    plt.savefig("graphs/eye_disease_distribution.png")
    plt.close()

    # 4. Risk Category Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Risk_Category")
    plt.title("Risk Category Distribution")
    plt.savefig("graphs/risk_category_distribution.png")
    plt.close()

    # 5. Screen Time vs Eye Strain
    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="Screen_Time_Hours",
        y="Eye_Strain_Level"
    )
    plt.title("Screen Time vs Eye Strain")
    plt.savefig("graphs/screen_time_vs_eye_strain.png")
    plt.close()

    # 6. Eye Pressure Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Eye_Pressure"], bins=15, kde=True)
    plt.title("Eye Pressure Distribution")
    plt.savefig("graphs/eye_pressure_distribution.png")
    plt.close()

    # 7. Uses Glasses
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Uses_Glasses")
    plt.title("Glasses Usage")
    plt.savefig("graphs/glasses_usage.png")
    plt.close()

    # 8. Surgery History
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Surgery_History")
    plt.title("Surgery History")
    plt.savefig("graphs/surgery_history.png")
    plt.close()

    # 9. Eye Disease vs Risk Category
    plt.figure(figsize=(12, 6))
    sns.countplot(
        data=df,
        x="Eye_Disease",
        hue="Risk_Category"
    )
    plt.title("Eye Disease vs Risk Category")
    plt.xticks(rotation=45)
    plt.savefig("graphs/disease_vs_risk.png")
    plt.close()

    # 10. Correlation Heatmap
    numeric_cols = [
        "Age",
        "Vision_Left_Eye",
        "Vision_Right_Eye",
        "Screen_Time_Hours",
        "Eye_Pressure",
        "Eye_Strain_Level"
    ]

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        df[numeric_cols].corr(),
        annot=True,
        cmap="Blues"
    )

    plt.title("Correlation Heatmap")
    plt.savefig("graphs/correlation_heatmap.png")
    plt.close()

    print("All graphs generated successfully!")
    print("Graphs saved in 'graphs' folder.")


# Main Program
if __name__ == "__main__":

    print("Loading Eye Patient Dataset...")

    df = load_data()

    print("Dataset Loaded Successfully!")
    print(df.head())

    print("Generating Graphs...")

    generate_all_graphs(df)