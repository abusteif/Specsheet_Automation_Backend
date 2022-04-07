from flask import Flask, request, send_file, abort
from flask_restful import Resource, Api
from flask_cors import CORS
from waitress import serve
import logging

from Specsheet_Automation.classes.jira_operations_class import JiraOperations
from Specsheet_Automation.helpers.specsheet_automation_helpers import cleanup_files
import io
from Specsheet_Automation.scripts.specsheet_automation import validate_data, \
    extract_and_populate_specsheet, get_message_fields

from Specsheet_Automation.scripts.jira_automation import initialise_jira, create_jira_issue, create_defect, \
    get_vendors_from_local, get_device_types_from_local
from Specsheet_Automation.static_data.file_info import logs_file_path
from Specsheet_Automation.static_data.configuration import MAX_RETRY_COUNT, ENVIRONMENT_URL, DEV

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

class JiraInitialise(Resource):
    def put(self):
        data = request.get_json()
        force_update = data["forceUpdate"]
        project_id = data["projectId"]
        jira_token = request.headers.get("Authorization")
        result = initialise_jira(project_id, jira_token, force_update=force_update)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

# class JiraIssue(Resource):
#
#     def post(self):
#         data = request.get_json()
#         jira_token = request.headers.get("Authorization")
#         issue_details = data
#         response = create_jira_issue("issue_details, jira_token)
#         return response["status"]

class Device(Resource):

    def post(self):
        data = request.get_json()
        jira_token = request.headers.get("Authorization")
        issue_details = data
        result = create_jira_issue("device", issue_details, jira_token)
        if result[0]:
            return result[1], 201
        else:
            return result[1], 500

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
        project_id = args["projectId"]
        device_id = args["deviceId"]
        result = jira_operations.get_all_cycles(project_id, device_id)
        if result["status"] != 200:
            return result["text"], result["status"]
        output = []
        for r in result["text"]:
            if isinstance(result["text"][r], dict):
                result["text"][r]["id"] = r
                output.append(result["text"][r])
        return output, 200

class Vendors(Resource):
    def get(self, projectId):
        result = get_vendors_from_local(projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

class DeviceTypes(Resource):
    def get(self, projectId):
        result = get_device_types_from_local(projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

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


api.add_resource(GenerateCookies, '/generateCookies')
# api.add_resource(JiraIssue, '/jiraIssue')
api.add_resource(Device, '/device')
api.add_resource(JiraDefect, '/jiraDefect')
api.add_resource(JiraProject, '/jiraProject/<string:projectKey>')
api.add_resource(Devices, '/devices/<string:projectId>')
api.add_resource(IotCycles, '/iotCycles')
api.add_resource(Validate, '/validate')
api.add_resource(PopulateSpecsheet, '/populateSpecsheet')
api.add_resource(MSRFields, '/messageFields/<string:messageType>')
api.add_resource(JiraInitialise, '/jiraInitialise')
api.add_resource(Vendors, '/vendors/<string:projectId>')
api.add_resource(DeviceTypes, '/deviceTypes/<string:projectId>')

if __name__ == '__main__':
    if DEV:
        app.run(host=ENVIRONMENT_URL, port=5001, debug=True)
    else:
        serve(app, host=ENVIRONMENT_URL, port=5000)

    # app.run(host='0.0.0.0', port=5000, debug=True)

