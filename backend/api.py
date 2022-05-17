import fastapi
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from controller import PolitiAPI

origins = [
  "*"
]

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"],
)

politi_api = PolitiAPI()

@app.get("/branches")
def get_branches():
  return politi_api.get_branches()
  
"""
@app.get("/branches/{city_name}")
def get_branches_city(city_name: str):
  branches = politi_api.getBranches()
"""

@app.get("/schedules/{branch_id}")
def get_schedules(branch_id: str):
  return politi_api.get_schedule_date_list(branch_id)

@app.get("/schedules/{branch_id}/{date}")
def get_available_dates(branch_id: str, date: str, response: Response):
  dates = politi_api.get_available_time_for_date(branch_id, date)
  if dates:
    return dates
  response.status_code = status.HTTP_404_NOT_FOUND
  return {"message": "No available slots for that date"}


@app.post('/register')
def register_user(email: str, branch_id: str, date: str):
  pass