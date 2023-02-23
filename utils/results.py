#Your client side implementation should parse the json into a dict, search the keys for these types, and handle all these responses to react accordingly
#--Ex. failed attempts to access cloud services can be used for rollbacks & status reports
#--	   no allowance can be used to return an error message and redirect users to customer support & resource purchase pages

#Parse for the function names as strings
#Handle the them based on the string types here
from typing import Union, Dict, Any, Optional

def attempt_result(success: Union[bool, None]):
	if success is not None:	
		if success:
			return "succeeded"
		else:
			return "failed"
	else:
		return "N/A"

def allowed_result(allowed: Union[bool, None]):
	if allowed is not None:
		if allowed:
			return "ok"
		else:
			return "no"
	else:
		return "N/A"

def response(attempt: Optional[bool], allowed: Optional[bool], message: str = "Responses without messages are not allowed", data: Optional[Dict[str, Any]] = None, url: Optional[str] = None):
	response =  {"attempt": attempt_result(attempt), "allowed": allowed_result(allowed), "message": message}

	if data is not None:
		response.update(data)

	if url is not None:
		response.update({"url": url})
	
	return response
