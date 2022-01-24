from fastapi import FastAPI
from typing import Optional, Any, List
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase
from typing import List, Optional

import starlette.responses as _responses


import uvicorn as uvicorn
import numpy as np


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "yash"), max_connection_lifetime=1)
session = graphdb.session()

@app.get('/')
async def root():
    return _responses.RedirectResponse("/docs")

@app.post('/addParentNode',tags=["Organisation"])
async def addParentNode():
    q2 = '''CREATE (ParentNode: ParentNode{name:"Survey"}) '''
    result = session.run(q2)
    data = result.data()
    json_data = jsonable_encoder(data)
    return ("Parent node added")

@app.post('/modelDetails/{name}/{desc}',tags=["Organisation"])
async def modelDetails(name: str, desc: str):
    q2 = '''MATCH(P: ParentNode)
            CREATE (P) -[:hasModel]->(M: Model{name: $name, desc: $desc})'''
    x = {"name": name, "desc":desc}
    result = session.run(q2,x)
    data = result.data()
    json_data = jsonable_encoder(data)
    return ("Model node added")

@app.get('/getModelDetails',tags=["Organisation"])
async def getModelDetails():
    q2 = '''MATCH(P: ParentNode) -[:hasModel]->(Model: Model)
            RETURN Model'''
    x = {}
    result = session.run(q2,x)
    data = result.data()
    json_data = jsonable_encoder(data)
    return (json_data)

@app.put('/modelDetails/{name}/{timesUsed}',tags=["Organisation"])
async def modelDetails(name: str, timesUsed: Optional[int] = None):
    q2 = '''MATCH(P: ParentNode) -[:hasModel]->(Model: Model{name: $name})
            SET Model.timesUsed = $timesUsed'''
    x = {"name": name, "timesUsed":timesUsed}
    result = session.run(q2,x)
    data = result.data()
    json_data = jsonable_encoder(data)
    return ("Model node updated")

@app.post('/organisationDetails/{sector}/{name}',tags=["Organisation"])
async def organisationDetails(sector: str, name: str):
    q2 = '''MATCH(P: ParentNode)
            CREATE (P) -[:hasOrganisation]->(O: Organisation{sector: $sector, name: $name})'''
    x = {"name": name, "sector":sector}
    result = session.run(q2,x)
    data = result.data()
    json_data = jsonable_encoder(data)
    return ("Organisation node added")

@app.post('/dimensionDetails/{dimensionTitle}/{description}/{weight}/{cutoff}',tags=["Organisation"])
async def dimensionDetails(dimensionTitle: str, description: str, weight: str, cutoff: str):
    q2 = '''MATCH(O: Organisation)
            CREATE (O) -[:hasDimension]->(D: Dimension{dimensionTitle: $dimensionTitle, description: $description,
            weight: $weight, cutoff: $cutoff})'''
    x = {"dimensionTitle": dimensionTitle, "description":description, "weight": weight, "cutoff": cutoff}
    result = session.run(q2,x)
    data = result.data()
    json_data = jsonable_encoder(data)
    return ("Organisation node added")












session.close()
graphdb.close()

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5000)