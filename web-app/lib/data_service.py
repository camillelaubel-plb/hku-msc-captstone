import requests
import json
from datetime import timedelta, datetime
import sys
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

_lgr = logging.getLogger(__name__)


# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# session = requests.Session()
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount('http://', adapter)
# session.mount('https://', adapter)

api_endpoint = "https://test-generation-uh7bect6ia-de.a.run.app/ask-ai"

def submit_request(api_key, code, input_type, boundary, expected_output):
    _lgr.info(f'{datetime.now()} - [Start] submit_request')
    try:
        rsp = requests.post(api_endpoint, json={
            "apiKey": api_key,
            "code": code,
            "data": {
                "inputType": input_type,
                "boundary": boundary,
            },
            "result": {
                "expectedOutput": expected_output,
            }
        })
        _lgr.info(f"StatusCode = {rsp.status_code}")
        rsp_data = rsp.content.decode('utf-8')
        _lgr.info(f"Data = {rsp_data}")
        json_rsp_data = json.loads(rsp_data)
        return (rsp.status_code == 200, json_rsp_data)

        # fp = f"{os.path.dirname(__file__)}/sample_response.json"
        # fake_data = open(fp, "r")
        # json_rsp_data = json.loads(fake_data.read())
        # return (True, json_rsp_data)
    except:
        err_msg = str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1])
        _lgr.error(f"Failed to submit request: \n{err_msg}")
    _lgr.info(f'{datetime.now()} - [Done] submit_request')
    return (False, {"error": err_msg})
