from fastapi import FastAPI, HTTPException
# menggunakan pandas -> memproses csv -> untuk menjadi sumber data (dalam bentuk dataframe)
import pandas as pd

# bikin object FastAPI
app = FastAPI()

# read csv -> pastikan dataset csv itu sudah dalam keadaan bersih -> data cleaning
# tidak ada missing value, tidak ada type data invalid, dsb..
df = pd.read_csv("Dataset.csv")

# define alamat/endpoint

# alamat utama -> '/'
@app.get('/')
def getMain():
    return {
        "message": "Main Page"
    }

# alamat untuk mengambil data pesan "hello"
@app.get('/hello')
def getHello():
    # return json/dictionary
    return {
        "message": "Hello"
    }

# alamat untuk mengambil semua data dari file csv/dataframe
@app.get('/all-data')
def getAll():
    # gabisa langsung return dataframe, harus di convert ke dictionary
    return df.to_dict(orient='records')

# alamat untuk mengambil data sesuai pencarian
@app.get('/search-data/{name}')
def getSearch(name:str):
    # filter nama dari dataframe
    filterDf = df[df['name'] == name]

    # error handling
    if filterDf.size == 0:
        raise HTTPException(status_code=404, detail=f"nama {name} tidak ditemukan")

    # return hasil filter
    return filterDf.to_dict(orient='records')

# alamat untuk menambah data baru
@app.post('/create-new')
def createNew(added_item:dict):
    """
    gambaran payload:
    dict added_item: {
        "name": ...,
        "age": ...,
        "location: ...
    }
    """

    # menambahkan data baru/new row ke dataframe
    df.loc[len(df.index)] = added_item

    # return dataframe terbaru
    return df.to_dict(orient='records')

# ketika running uvicorn -> ip local/localhost + port number
# port number: 8000
# stop uvicorn ctrl + C / command + C