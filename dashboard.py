import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("nofluffjobs_offers.csv")

df['Wynagrodzenie do (PLN)'].fillna(df['Wynagrodzenie od (PLN)'], inplace=True)
df['Średnie wynagrodzenie (PLN)'] = (df['Wynagrodzenie od (PLN)'] + df['Wynagrodzenie do (PLN)']) / 2

st.title("📊 Analiza ofert pracy dla Java Developerów")

st.subheader("📌 Tabela z danymi o ofertach pracy")
st.dataframe(df)

st.subheader("📍 Średnie wynagrodzenie według lokalizacji")
avg_salary_by_location = df.groupby('Lokalizacja')['Średnie wynagrodzenie (PLN)'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 8))
avg_salary_by_location.plot(kind='bar', color='salmon', ax=ax)
ax.set_title('Średnie wynagrodzenie według lokalizacji')
ax.set_xlabel('Lokalizacja')
ax.set_ylabel('Średnie wynagrodzenie (PLN)')
ax.grid(True)
st.pyplot(fig)

st.subheader("📍 Ilość ofert per lokalizacja")
st.write(df['Lokalizacja'].value_counts())
