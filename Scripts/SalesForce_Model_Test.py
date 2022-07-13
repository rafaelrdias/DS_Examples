# The OCI SDK must be installed for this example to function properly.
# Installation instructions can be found here: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/pythonsdk.htm

import requests
import oci
from oci.signer import Signer

config = oci.config.from_file("~/.oci/config") # replace with the location of your oci config file
auth = Signer(
  tenancy=config['tenancy'],
  user=config['user'],
  fingerprint=config['fingerprint'],
  private_key_file_location=config['key_file'],
  pass_phrase=config['pass_phrase'])

endpoint = 'https://modeldeployment.us-ashburn-1.oci.customer-oci.com/ocid1.datasciencemodeldeployment.oc1.iad.amaaaaaatsbrckqaz47rhokku67kiun6qxjll2cxepq4hl3xb35pbaior4hq/predict'
body = {"BATHROOMS":{"513":1.0},"BEDROOMS":{"513":1.0},"BEDS":{"513":1.0},"CLEANING_FEE":{"513":20.0}} # payload goes here

requests.post(endpoint, json=body, auth=auth).json()