from flask import Flask
from flask_restx import Api, Resource
from typing import Optional
from controller import PolitiAPI


app = Flask(__name__)
api = Api(app)

politi_api = PolitiAPI()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route("/branches")
class GetBranches(Resource):
  def get(self):
    return politi_api.get_branches()  

@api.route('/schedules/<string:branch_id>')
class GetSchedules(Resource):
  def get(self, branch_id: str):
    return politi_api.get_schedule_date_list(branch_id)

@api.route('/schedules/<string:branch_id>/<string:date>')
class GetAvailableSlotsForBranchOnDate(Resource):
  def get(self, branch_id: str, date: str):
    dates = politi_api.get_available_time_for_date(branch_id, date)
    if dates:
      return dates
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "No available slots for that date"}

if __name__ == '__main__':
    app.run(debug=True)