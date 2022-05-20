from flask import Flask, request, send_file, abort
from flask_restful import Resource, Api
from flask_cors import CORS
from waitress import serve
import logging
import time

from Specsheet_Automation.classes.jira_operations_class import JiraOperations
from Specsheet_Automation.helpers.specsheet_automation_helpers import cleanup_files
import io
from Specsheet_Automation.scripts.specsheet_automation import validate_data, \
    extract_and_populate_specsheet, get_message_fields

from Specsheet_Automation.scripts.jira_automation import initialise_jira, create_jira_issue, create_defect, \
    get_vendors_from_local, get_device_types_from_local, get_user, get_devices_for_vendor, \
    get_testing_request_types_from_local, get_testing_priorities_from_local, get_wda_test_scopes_from_local, \
    get_funding_from_local, get_releases_for_device, update_jira_issue
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
                time.sleep(1)
        else:
            return "Failed to generate Cookies", 408

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
        issue_details = data["issueDetails"]
        result = create_jira_issue("device", issue_details, jira_token)
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500

    def put(self):
        data = request.get_json()
        jira_token = request.headers.get("Authorization")
        issue_details = data["issueDetails"]
        jira_ticket_id = data["jiraTicketId"]
        # return "a", 204

        result = update_jira_issue("device", issue_details, jira_ticket_id, jira_token)
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500

class Release(Resource):

    def post(self):
        data = request.get_json()
        jira_token = request.headers.get("Authorization")
        issue_details = data["issueDetails"]
    #     return  {
    #     "key": "WDAFY20-2440",
    #     "summary": "ACME Device Register test model (test market name)"
    # }, 201

        result = create_jira_issue("release", issue_details, jira_token)
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500

class IOTCycle(Resource):

    def post(self):
        data = request.get_json()
        jira_token = request.headers.get("Authorization")
        issue_details = data["issueDetails"]
        # print(data)
        # return "ok", 201

        result = create_jira_issue("iotCycle", issue_details, jira_token)
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500

class Defect(Resource):

    def post(self):
        data = request.get_json()
        jira_token = request.headers.get("Authorization")
        issue_details = data["issueDetails"]
        url = data["url"]
        result = create_defect(issue_details, url, jira_token)
        # return "ok", 201
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500

class User(Resource):

    def get(self, dnumber):

        jira_token = request.headers.get("Authorization")
        result = get_user(dnumber, jira_token)
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500

class EpicCapabilityMapping(Resource):

    def post(self):
        data = request.get_json()
        jira_token = request.headers.get("Authorization")
        epic = data["epic"]
        capability = data["capability"]
        project_id = data["projectId"]
        print(epic, capability)
        details = {
            "parentLink": epic,
            "project_id": project_id
        }
        result = update_jira_issue("release", details, epic, jira_token)
        print(result)
        if result[0]:
            return result[1]["text"], result[1]["status"]
        else:
            return result[1], 500


class DevicesForVendor(Resource):
    def get(self, projectId, vendor):
        jira_token = request.headers.get("Authorization")
        result = get_devices_for_vendor(vendor, jira_token, projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

class ReleasesForDevice(Resource):
    def get(self, projectId, deviceTicketId):
        fields_to_return = request.args.get("extraFieldsToReturn", None)
        if fields_to_return:
            fields_to_return = fields_to_return.split(",")
        jira_token = request.headers.get("Authorization")
        result = get_releases_for_device(deviceTicketId, jira_token, projectId, fields_to_return)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

# class JiraIssueFields(Resource):
#     def put(self):
#         data = request.get_json()
#         jira_token = request.headers.get("Authorization")
#         issue_details = data["issueDetails"]
#         issue_id = data["issueId"]
#         result = update_issue_details(issue_id, issue_details, jira_token)
#         # print(result)
#         if result[0]:
#             return result[1]["text"], result[1]["status"]
#         else:
#             return result[1], 500

class Vendors(Resource):
    def get(self, projectId):
        result = get_vendors_from_local(projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

class TestingPriorities(Resource):
    def get(self, projectId):
        result = get_testing_priorities_from_local(projectId)
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

class TestingRequestTypes(Resource):
    def get(self, projectId):
        result = get_testing_request_types_from_local(projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

class WDATestScope(Resource):
    def get(self, projectId):
        result = get_wda_test_scopes_from_local(projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500
class Funding(Resource):
    def get(self, projectId):
        result = get_funding_from_local(projectId)
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

api.add_resource(GenerateCookies, '/generateCookies')
# api.add_resource(JiraIssue, '/jiraIssue')
api.add_resource(Device, '/device')
api.add_resource(Release, '/release')
api.add_resource(IOTCycle, '/iotCycle')

# api.add_resource(JiraIssueFields, '/jiraIssueFields')
api.add_resource(Defect, '/defect')
api.add_resource(JiraProject, '/jiraProject/<string:projectKey>')
api.add_resource(Devices, '/devices/<string:projectId>')
api.add_resource(IotCycles, '/iotCycles')
api.add_resource(Validate, '/validate')
api.add_resource(EpicCapabilityMapping, '/epicCapabilityMapping')
api.add_resource(PopulateSpecsheet, '/populateSpecsheet')
api.add_resource(MSRFields, '/messageFields/<string:messageType>')
api.add_resource(JiraInitialise, '/jiraInitialise')
api.add_resource(Vendors, '/vendors/<string:projectId>')
api.add_resource(WDATestScope, '/wdaTestScopes/<string:projectId>')
api.add_resource(DeviceTypes, '/deviceTypes/<string:projectId>')
api.add_resource(Funding, '/funding/<string:projectId>')
api.add_resource(TestingPriorities, '/testingPriorities/<string:projectId>')
api.add_resource(User, '/user/<string:dnumber>')
api.add_resource(DevicesForVendor, '/devicesForVendor/<string:projectId>/<string:vendor>')
api.add_resource(ReleasesForDevice, '/releasesForDevice/<string:projectId>/<string:deviceTicketId>')
api.add_resource(TestingRequestTypes, '/testingRequestTypes/<string:projectId>')

if __name__ == '__main__':
    if DEV:
        app.run(host=ENVIRONMENT_URL, port=5001, debug=True)
    else:
        serve(app, host=ENVIRONMENT_URL, port=5000)

    # app.run(host='0.0.0.0', port=5000, debug=True)

