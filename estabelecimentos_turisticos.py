import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import sqlite3

df = pd.read_csv("https://opendata.arcgis.com/api/v3/datasets/84912bbcfc7041eba5722a6f52b6bddf_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1")
conn = sqlite3.connect("turismo.db")
cur = conn.cursor()
df.to_sql("estabelecimentos_turismo_data", conn, if_exists="replace")

df = pd.read_sql("SELECT * FROM estabelecimentos_turismo_data", conn)
print(df)
print("\n")
print(df.describe(include="all"))
print("\n\033[32mDESCRIPTIVE STATISTICS - Sucessful\033[0m")

query = """
        SELECT Denominacao, TipologiaET, Distrito, Concelho, Website
        FROM estabelecimentos_turismo_data
        WHERE Situacao='ETExistente' AND Website != 'None'
        ORDER BY Denominacao DESC
        LIMIT 50
"""

main_attr = pd.read_sql(query, conn)
print("\n")
print(main_attr)
print("\n\033[32mMAIN ATTRIBUTES - Sucessful\033[0m")

query2 = """
        SELECT DISTINCT(TipologiaET) AS Tipologia, Distrito, COUNT(*) AS Numero
        FROM estabelecimentos_turismo_data
        WHERE Situacao='ETExistente' AND Website != 'None'
        GROUP BY Tipologia, Distrito
        ORDER BY Numero DESC
        LIMIT 10
"""

et_types = pd.read_sql(query2, conn)
print("\n")
print(et_types)
print("\n\033[32mET TYPES - Sucessful\033[0m")

query2 = """
        SELECT DISTINCT(TipologiaET) AS Tipologia, COUNT(TipologiaET) AS Numero
        FROM estabelecimentos_turismo_data
        WHERE Situacao='ETExistente' AND Website != 'None'
        GROUP BY Tipologia
        ORDER BY Numero DESC
        LIMIT 5
"""

dist_types = pd.read_sql(query2, conn)
print("\n")
print(dist_types)
print("\n\033[32mNUMBER OF ET TYPES - Sucessful\033[0m")

plt.figure(figsize=(8, 6))

pal = sns.color_palette("Blues")
pal = pal[::-1]

sns.set_style("whitegrid")
plt.pie(dist_types['Numero'], labels=dist_types['Tipologia'], autopct='%1.1f%%', startangle=140, colors=pal)
plt.title('Estabelecimentos por Tipologia')
plt.axis('equal')
plt.show()

sns.scatterplot(x="NrUnidAloj", y="NrTotalCamas", data="estabelecimentos_turismo_data")
plt.title("Número de camas por unidade de alojamento")
plt.show()