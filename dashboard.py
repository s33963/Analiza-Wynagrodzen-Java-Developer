
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("nofluffjobs_offers.csv")

df['Wynagrodzenie do (PLN)'].fillna(df['Wynagrodzenie od (PLN)'], inplace=True)
df['Wynagrodzenie od (PLN)'] = df['Wynagrodzenie od (PLN)'].astype(str).str.replace(" ", "").str.replace(",", "").astype(float)
df['Wynagrodzenie do (PLN)'] = df['Wynagrodzenie do (PLN)'].astype(str).str.replace(" ", "").str.replace(",", "").astype(float)
df['Średnie wynagrodzenie (PLN)'] = (df['Wynagrodzenie od (PLN)'] + df['Wynagrodzenie do (PLN)']) / 2

st.title("Analiza ofert pracy i wynagrodzeń")

st.subheader("Tabela z danymi o ofertach pracy")
st.dataframe(df)

st.subheader("Ilość ofert per lokalizacja")
location_counts = df['Lokalizacja'].value_counts()
st.dataframe(location_counts)

st.subheader("Rozkład średnich wynagrodzeń")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['Średnie wynagrodzenie (PLN)'], bins=30, color='skyblue', edgecolor='black')
ax.set_title('Rozkład średnich wynagrodzeń')
ax.set_xlabel('Średnie wynagrodzenie (PLN)')
ax.set_ylabel('Liczba ofert')
ax.grid(True)
st.pyplot(fig)

st.subheader("Średnie wynagrodzenie według lokalizacji")
location_stats = df.groupby('Lokalizacja').agg({'Średnie wynagrodzenie (PLN)': 'mean', 'Tytuł': 'count'}).rename(columns={'Tytuł': 'Liczba ofert'})
location_stats = location_stats.sort_values(by='Liczba ofert', ascending=False)

fig, ax = plt.subplots(figsize=(12, 8))
location_stats['Średnie wynagrodzenie (PLN)'].plot(kind='bar', color='salmon', ax=ax)
ax.set_title('Średnie wynagrodzenie według lokalizacji')
ax.set_xlabel('Lokalizacja')
ax.set_ylabel('Średnie wynagrodzenie (PLN)')
ax.grid(True)
st.pyplot(fig)
