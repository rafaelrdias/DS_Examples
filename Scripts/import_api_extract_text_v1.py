#subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'oci'])

import sys
import subprocess
import requests
import re
import oci
import ocifs
import base64
import ads

from PIL import Image
from ads.dataset.factory import DatasetFactory
from oci.object_storage import ObjectStorageClient
from ads.common.auth import default_signer

ads.set_auth(auth='resource_principal')

namespace = "id3xxxxxxxxx"
bucket_name = "xxxxxxxxxximages"

config = oci.config.from_file("./decompressed_artifact/config")

ai_vision_client = oci.ai_vision.AIServiceVisionClient(config = config)

rps = oci.auth.signers.get_resource_principals_signer()
oci_client = ObjectStorageClient({}, signer=rps)

fs = ocifs.OCIFileSystem(config="~/.oci/config")

img_list = fs.glob("oci://light_p2p_images@id3xxxxxxxxx/*")

name_list = []
for i, item in enumerate(img_list):
    name = item.rsplit('/', 1)[1]
    name_list.append(name)
    
code_list = []
for i in range(0, len(img_list)):
    codigo = img_list[i]
    s = [float(s) for s in re.findall(r'-?\d+\.?\d*', codigo)]
    code_list.append(int(s[1]))

imagens_validas = []
imagens_invalidas = []

validos = 0
invalidos = 0

for i in code_list:
            put_object_response = oci_client.put_object(
                            namespace_name=namespace,
                            bucket_name=bucket_name,
                            object_name= i,
                            put_object_body = file,
                            content_type='image/jpeg')
            
            imagens_validas.append(i)
            validos += 1
                
fs = ocifs.OCIFileSystem({}, signer=rps)

img_list = fs.glob("oci://images@id3xxxxxxxx/*")

name_list = []
for i, item in enumerate(img_list):
    name = item.rsplit('/', 1)[1]
    name_list.append(name)
    
code_list = []
for i in range(0, len(img_list)):
    codigo = img_list[i]
    s = [float(s) for s in re.findall(r'-?\d+\.?\d*', codigo)]
    code_list.append(int(s[1]))

for i, file in enumerate(img_list):
        with fs.open(file) as f:
            content = f.read()
            
            encoded_string = base64.b64encode(content, altchars=None)
            decoded_string = encoded_string.decode("utf-8", "ignore")

            analyze_document_response = ai_vision_client.analyze_document(
                    analyze_document_details=oci.ai_vision.models.AnalyzeDocumentDetails(
                    compartment_id = "ocid1.compartment.oc1..aaaaaaaal63rmctoojg7q2pvdpeuqknebyaqg3h7gcci6whf74ht7tfapl4q",
                    features=[
                        oci.ai_vision.models.DocumentTextDetectionFeature(
                            feature_type="TEXT_DETECTION")],
                    language='ENG',
                    document=oci.ai_vision.models.InlineDocumentDetails(
                    source="INLINE",
                    data=decoded_string)))

            words = str([word.text for page in analyze_document_response.data.pages for word in page.words])
            name = f"{name_list[i]}.txt"  
            
            words_str_1 = words.replace("',",'')
            words_str_2 = words_str_1.replace("'",'')
            words_str_3 = words_str_2.replace("[",'')
            words_str_4 = words_str_3.replace("]",'')

            put_object_response = oci_client.put_object(
                                        namespace_name='id3xxxxxxxxx',
                                        bucket_name='texts',
                                        object_name=name,
                                        put_object_body = words_str_4,
                                        content_type="text/plain")

            print("Documento", name, "upado!")