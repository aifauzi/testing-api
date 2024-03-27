from fastapi import FastAPI, HTTPException, Request, Response, Header

# kita bisa ambil data juga dari pandas
import pandas as pd

# bikin object FastAPI
app = FastAPI()

# read csv -> pastikan datanya sudah bersih (no missing value, no data invalid, dsb)
df = pd.read_csv('datasets.csv')

API_Key = "@johns321"

# buat alamat/endpoint

# alamat utama biasanya menggunakan '/'
@app.get('/')
def getMain():
    return {
        "message": "Main Page"
    }

# almat untuk ambil data pesan statis 'hello'
@app.get('/hello')
def getHello(request: Request):
    
    # mengakses header dari request
    headers = request.headers

    # return berbentuk json/dict
    return {
        "message": "hello",
        "request_header": headers.get("user-agent")
    }

# alamat contoh untuk melihat hasil response
@app.get('/hai')
def getHai(request: Request):
    response = Response(content="Hai")
    
    # define header response
    response.headers["custom-header"] = "Ini custom header"

    return response

# alamat yang hanya bisa diakses dengan API Key
@app.get('/secret')
def getSecret(api_key: str = Header(None)):
    if api_key is None or api_key != API_Key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {
        "message": "secret"
    }

# alamat untuk ambil semua data dari csv
@app.get('/all-data')
def getAll():
    # dataframe tidak bisa langsung di return
    return df.to_dict(orient='records')

# alamat untuk ambil data sesuai pencarian
@app.get('/search-data/{nama}')
def getSearch(nama: str):
    # filter nama dari dataframe
    filter = df[df['nama'] == nama]

    # error handling
    if filter.size == 0:
        raise HTTPException(status_code=404, detail=f"Name {nama} not found")
    return filter.to_dict(orient='records')

# alamat untuk menambah data baru
@app.post('/create-new')
def createNew(added_item: dict):
    #gambaran penambahan
    """
    dict added_new: {
    'nama': ...
    'age': ...
    'location': ...
    }
    """
    # menambah data baru/new row ke dataframe
    df.loc[len(df.index)] = added_item
    return df.to_dict(orient='records')

# untuk mengeksekusi API menggunakan uvicorn
# untuk menghentikan run gunakan ctrl + c
# hasil uvicorn -> menghasilkan ip local dan port number (8888)