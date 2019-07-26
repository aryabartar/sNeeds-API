from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key[
    'api-key'] = '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'

# create an instance of the API class
api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
create_contact = sib_api_v3_sdk.CreateContact(
    email="bartararya77@gmail.com",
)  # CreateContact | Values to create a contact

try:
    # Create a contact
    api_response = api_instance.create_contact(create_contact)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->create_contact: %s\n" % e)
