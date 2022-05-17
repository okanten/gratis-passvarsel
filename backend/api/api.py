from http import HTTPStatus
from db import *
from flask import Flask
from flask_restx import Api, Resource
from parsers import *
from typing import Optional
from politiapi import PolitiAPI


app = Flask(__name__)
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(app, authorizations=authorizations)


politi_api = PolitiAPI()


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
    api.abort(404, "No available slots for that date")

@api.route('/register/user')
@api.expect(reg_parser)
class RegisterUser(Resource):
  def post(self):
    args = reg_parser.parse_args()
    phone_number = args['phone_number']
    password = args['password']
    if create_user(phone_number, password):
      return {"message": "success"}
    api.abort(HTTPStatus.CONFLICT, "User exists, banned or otherwise prohibited from creating a user")

@api.route('/login')
@api.expect(login_parser)
class LoginUser(Resource):
  def post(self):
    args = login_parser.parse_args()
    phone_number = args['phone_number']
    password = args['password']
    if not check_if_user_exists(phone_number):
      api.abort(403, "User does not exist")
    if verify_login(phone_number, password):
      # generate JWT
      return {"message": "Successfully logged in!"}
    api.abort(401, "Wrong username/password")
    

if __name__ == '__main__':
    app.run(debug=True)