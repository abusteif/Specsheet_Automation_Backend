from flask import Flask, request, send_file, abort
from flask_restful import Resource, Api
from flask_cors import CORS
from waitress import serve
from datetime import datetime
from json import JSONDecodeError
import logging

from Specsheet_Automation.classes.jira_operations_class import *
from Specsheet_Automation.helpers.specsheet_automation_helpers import cleanup_files
import io
from Specsheet_Automation.scripts.specsheet_automation import  validate_data, \
    extract_and_populate_specsheet, get_message_fields,  initialise_jira, create_jira_issue, create_defect
    # get_all_ie_from_jira, check_for_execution, extract_and_upload
from Specsheet_Automation.static_data.file_info import logs_file_path, jira_config_file
from Specsheet_Automation.static_data.jira_config import JIRA_ISSUE_TYPES, CONFIG_REFRESH_INTERVAL
from Specsheet_Automation.classes.jira_api import JiraApi

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*", "credentials": True}})
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=logs_file_path
)

class GenerateCookies(Resource):
    def get(self):
        print(request.remote_addr)
        for _ in range(MAX_RETRY_COUNT):
            try:
                jira_operations = JiraOperations()
                cookies = jira_operations.get_cookies()
                return {"token": cookies.get_dict()["crowd.token_key"]}
            except Exception as e:
                print(repr(e))
        else:
            return "Failed to generate Cookies", 408

# class JiraInitialise(Resource):
#     def put(self, projectId):
#         jira_token = request.headers.get("Authorization")
#         result = initialise_jira(projectId, jira_token)
#         if result[0]:
#             return 204, result[1]
#         else:
#             return 500, result[1]

class JiraIssue(Resource):

    def post(self):
        data = request.get_json()
        project_id = data["Project"]
        jira_token = request.headers.get("Authorization")
        initialise_jira(project_id, jira_token)
        issue_details = data
        response = create_jira_issue(issue_details, jira_token)
        return response["status"]

class JiraDefect(Resource):

    def post(self):
        data = request.get_json()
        try:
            jira_token = request.headers.get("Authorization")
        except KeyError:
            jira_token = None
        url = data["url"]
        summary = data["summary"]
        description = data["description"]
        return 200, create_defect(url, summary, description, jira_token)


class PopulateSpecsheet(Resource):

    def post(self):
        data = request.get_json()
        dut_name = data["device"]
        iot_cycle = data["iotCycle"]
        hex_data = data["hexData"]
        result = extract_and_populate_specsheet(hex_data, dut_name, iot_cycle)

        if result[0]:
            try:
                return_data = io.BytesIO()
                with open(result[2], "rb") as fo:
                    return_data.write(fo.read())
                return_data.seek(0)
                cleanup_files(result[1])
                return send_file(return_data,
                                 mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 attachment_filename="MSR0835_{}_{}.xlsx".format(dut_name, iot_cycle))
            except Exception as e:
                return "An error occurred while populating the Spec sheet: {}".format(repr(e)), 500
        else:
            return result[1], 422

# class UploadToJira(Resource):
#
#     def post(self):
#         # return "good", 201
#         data = request.get_json()
#         dut_name = data["device"]
#         iot_cycle = data["iotCycle"]
#         hex_data = data["hexData"]
#         message_type = data["messageType"]
#         sim_type = data["simType"]
#
#         jira_token = request.headers.get("Authorization")
#         result = extract_and_upload(hex_data, message_type, sim_type, dut_name, iot_cycle, jira_token)
#
#         if result[0]:
#             return "Successfully uploaded Spec sheet to Jira", 201
#         else:
#             return result[1], 400

class JiraProject(Resource):

    def get(self, projectKey):
        jira_token = request.headers.get("Authorization")
        jira_operations = JiraOperations(jira_token)
        result = jira_operations.get_project_id_from_project_key(projectKey)
        return result["text"], result["status"]

class Devices(Resource):

    def get(self, projectId):
        jira_token = request.headers.get("Authorization")
        jira_operations = JiraOperations(jira_token)
        result = jira_operations.get_all_versions(projectId)
        return result["text"], result["status"]


class IotCycles(Resource):

    def get(self):
        args = request.args
        jira_token = request.headers.get("Authorization")

        jira_operations = JiraOperations(jira_token)

        result = jira_operations.get_all_cycles(args["projectId"], args["deviceId"])
        if result["status"] != 200:
            return result["text"], result["status"]
        output = []
        for r in result["text"]:
            if isinstance(result["text"][r], dict):
                result["text"][r]["id"] = r
                output.append(result["text"][r])
        return output, 200

class Validate(Resource):
    def post(self):
        data = request.get_json()
        message_type = data["messageType"]
        hex_data = data["hexData"]
        result = validate_data(hex_data, message_type)
        if result[0]:
            return "Validation Successful", 200
        if result[1] == "Malformed HEX data":
            return result[1], 422
        return result[1], 400

class MSRFields(Resource):
    def get(self, messageType):
        return get_message_fields(messageType), 200

# class SpecsheetIEFromJira(Resource):
#     def get(self):
#         args = request.args
#         iot_cycle = args["iotCycle"]
#         dut_name = args["device"]
#         message_type = args["messageType"]
#         sim_type = args["simType"]
#         jira_token = request.headers.get("Authorization")
#
#         result = get_all_ie_from_jira(message_type, sim_type, dut_name, iot_cycle, jira_token)
#
#         if result[0]:
#             return result[1], 200
#         else:
#             # return abort(500)
#             if result[1] == 404:
#                 return "Test case not found", 404
#             return result[1], 500

# class ExecutionStatus(Resource):
#     def get(self):
#         args = request.args
#         dut_name = args["device"]
#         iot_cycle = args["iotCycle"]
#         message_type = args["messageType"]
#         sim_type = args["simType"]
#         jira_token = request.headers.get("Authorization")
#
#         status = check_for_execution(message_type, sim_type, dut_name, iot_cycle, jira_token)
#         if status[0]:
#             return status[1], 200
#         else:
#             return status[1], 500


api.add_resource(GenerateCookies, '/generateCookies')
api.add_resource(JiraIssue, '/jiraIssue')
api.add_resource(JiraDefect, '/jiraDefect')
api.add_resource(JiraProject, '/jiraProject/<string:projectKey>')
api.add_resource(Devices, '/devices/<string:projectId>')
api.add_resource(IotCycles, '/iotCycles')
api.add_resource(Validate, '/validate')
api.add_resource(PopulateSpecsheet, '/populateSpecsheet')
# api.add_resource(UploadToJira, '/uploadToJira')
api.add_resource(MSRFields, '/messageFields/<string:messageType>')
# api.add_resource(SpecsheetIEFromJira, '/specsheetIEFromJira')
# api.add_resource(ExecutionStatus, '/executionStatus')

if __name__ == '__main__':
    if DEV:
        app.run(host=ENVIRONMENT_URL, port=5001, debug=True)
    else:
        serve(app, host=ENVIRONMENT_URL, port=5000)

    # app.run(host='0.0.0.0', port=5000, debug=True)

