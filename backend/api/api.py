import os
from http import HTTPStatus
from db import *
from flask import Flask
from flask_restx import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from parsers import *
from typing import Optional
from politiapi import PolitiAPI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
JWT_SECRET_KEY = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

api = Api(app)

jwt = JWTManager(app)

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
      access_token = create_access_token(identity=phone_number)
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
    user = verify_login(phone_number, password)
    if user:
      access_token = create_access_token(identity=user.phone_number)
      return {"access_token": access_token}
    api.abort(401, "Wrong username/password")
    
@api.route('/protected')
class Protected(Resource):
  @jwt_required()
  def get(self):
      # Access the identity of the current user with get_jwt_identity
      current_user = get_jwt_identity()
      return {"logged_in_as": current_user}

@api.route('/add/date')
@api.expect(add_date_parser)
class AddDate(Resource):
  @jwt_required()
  def post(self):
    current_user = get_jwt_identity()
    args = add_date_parser.parse_args()
    dates = args.get('dates')
    branches = args.get('branches')
    add_date(phone_number=current_user, date_str=dates, branch=branches)
    return {"logged_in_as": current_user}

if __name__ == '__main__':
    app.run(debug=True)