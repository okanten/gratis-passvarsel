from flask_restx import reqparse

reg_parser = reqparse.RequestParser(bundle_errors=True)
reg_parser.add_argument('phone_number', type=str, required=True)
reg_parser.add_argument('password', type=str, required=True)

login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument('phone_number', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)
