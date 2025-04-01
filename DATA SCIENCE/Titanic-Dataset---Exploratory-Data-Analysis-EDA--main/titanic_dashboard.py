
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'corrected_titanic_dataset.csv'
df = pd.read_csv(file_path)

# Data Cleaning and Preprocessing
if 'Sex' in df.columns:
    df['Sex'] = df['Sex'].astype(str).str.lower().map({'male': 0, 'female': 1})
    mode_value = df['Sex'].mode()
    if not mode_value.empty:
        df['Sex'].fillna(mode_value.iloc[0], inplace=True)
    df['Sex'] = pd.to_numeric(df['Sex'], errors='coerce').astype('Int64')

if 'Age' in df.columns:
    df['Age'].fillna(df['Age'].median(), inplace=True)

if 'Embarked' in df.columns:
    df['Embarked'].fillna(df['Embarked'].mode().iloc[0], inplace=True)

if 'Cabin' in df.columns:
    df.drop(columns=['Cabin'], inplace=True)  # Drop due to excessive missing values

if 'SibSp' in df.columns and 'Parch' in df.columns:
    df['Family Size'] = df['SibSp'] + df['Parch'] + 1  # Including self

# Title
st.title("🚢 Titanic Dataset EDA Dashboard")

# Dataset Overview
st.header("📊 Dataset Overview")
st.write("Analyzing Titanic passengers based on survival factors.")

st.subheader("🔍 Sample Data")
st.write("Below is a preview of the dataset:")
st.write(df.head())

st.subheader("⚠️ Missing Values")
st.write("Checking for missing values in the dataset:")
st.write(df.isnull().sum())

# Univariate Analysis
st.header("📈 Exploratory Data Analysis (EDA)")

def plot_if_exists(df, column, plot_func, title, description, **kwargs):
    if column in df.columns:
        st.subheader(title)
        st.write(description)
        fig, ax = plt.subplots()
        plot_func(data=df, ax=ax, **kwargs)
        ax.set_title(title)
        st.pyplot(fig)

# Survival Count
plot_if_exists(df, 'Survived', sns.countplot, "💀 Survival Count", "This graph shows the count of passengers who survived (1) and those who did not (0). It helps in understanding the survival rate of passengers.", x='Survived')

# Pclass Distribution
plot_if_exists(df, 'Pclass', sns.countplot, "🎟️ Passenger Class Distribution", "This graph represents the distribution of passengers across different ticket classes (1st, 2nd, and 3rd). Higher-class passengers had better survival chances.", x='Pclass')

# Age Distribution
plot_if_exists(df, 'Age', sns.histplot, "🧑 Age Distribution", "This histogram shows the distribution of passengers' ages with a density curve. It helps in identifying age-related survival patterns.", x='Age', bins=30, kde=True)

# Fare Distribution
plot_if_exists(df, 'Fare', sns.histplot, "💰 Fare Distribution", "This histogram illustrates the distribution of ticket fares paid by passengers. Higher fares were generally associated with better survival chances.", x='Fare', bins=30, kde=True)

# Family Size Distribution
plot_if_exists(df, 'Family Size', sns.countplot, "👨‍👩‍👧‍👦 Family Size Distribution", "This count plot shows the distribution of family sizes among passengers. It helps to understand the impact of family size on survival.", x='Family Size')

# Heatmap for correlation
st.subheader("🔥 Feature Correlation")
st.write("This heatmap displays the correlation between numerical features, helping to identify relationships between variables affecting survival.")
numeric_df = df.select_dtypes(include=['number']).fillna(0)
numeric_df = numeric_df.drop(columns=['Embarked_C', 'Survived by Gender', 'Sex'], errors='ignore')  # Remove specified columns
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Correlation Matrix")
st.pyplot(fig)

# Additional Visualizations
if 'Age' in df.columns:
    df['Age Group'] = pd.cut(df['Age'], bins=[0, 12, 18, 40, 60, 100], labels=['Child', 'Teenager', 'Adult', 'Middle-aged', 'Senior'])
    plot_if_exists(df, 'Age Group', sns.countplot, "👶 Survival by Age Group", "This graph represents survival distribution across different age groups. Younger passengers had a higher survival rate compared to adults.", x='Age Group', hue='Survived')

# Key Insights
st.header("🔎 Key Insights")
st.write("""
- **👩 Women had a higher survival rate** than men due to the 'women and children first' policy.
- **🎟️ 1st class passengers had a better chance of survival** compared to lower classes.
- **🧒 Younger children and elderly passengers had a higher survival rate.**
- **💵 Higher ticket prices were associated with better survival rates.**
- **👨‍👩‍👧‍👦 Family size influenced survival; smaller families had better chances.**
- **📍 Passengers who embarked from certain locations had higher survival rates.**
""")

st.subheader("✅ Conclusion")
st.write("This analysis highlights the key factors that influenced survival rates. Further predictive modeling can be done to refine insights and potentially build a predictive model for survival probabilities.")
