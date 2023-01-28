from fastapi import FastAPI
from db_connect import get_db

app = FastAPI()


@app.get('/prediction-2022/')
async def get_prediction(ticker: str, n: int=0):
    try:
        db = get_db()
        coll = db['prediction-2022']
        record = coll.find_one({'ticker': ticker}, {'_id': 0})
        if record is None:
            return {'message': 'not found'}
        else:
            return {'message': 'success', 'result': record}
    except:
        print('Internal server error')
        return {'message': 'Internal server error'}
