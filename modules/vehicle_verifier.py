import requests
import re

def verify_and_route_vehicle(registration_number):
    """
    Sequentially cycles through 5 distinct live RapidAPI gateways.
    Handles form-urlencoded data layouts alongside standard application/json payloads.
    """
    clean_reg = re.sub(r'[^a-zA-Z0-9]', '', registration_number).upper()
    
    # Strictly validate Indian standard layout syntax
    is_valid_syntax = bool(re.match(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$', clean_reg))
    if not is_valid_syntax:
        return {
            "status": "Syntax Mismatch",
            "message": "Provided registration format does not align with standard RTO rules.",
            "verified": False,
            "metadata": {}
        }

    # 📋 THE MASTER 5-API POOL
    api_pool = [
        {
            "name": "Flash AI (v5) - Primary Node",
            "url": "https://rto-vehicle-details5.p.rapidapi.com/address",
            "host": "rto-vehicle-details5.p.rapidapi.com",
            "method": "GET",
            "param_key": "registration",
            "content_type": "json"
        },
        {
            "name": "RTO Challan API",
            "url": "https://rto-challan-api.p.rapidapi.com/bus_api/public/api/v1/vaahan/searchChallanDetails",
            "host": "rto-challan-api.p.rapidapi.com",
            "method": "POST",
            "param_key": "vehicle_number", # Standard default parameter key for challan lookups
            "content_type": "form"
        },
        {
            "name": "Vehicle RC Information V2",
            "url": "https://vehicle-rc-information-v2.p.rapidapi.com/",
            "host": "vehicle-rc-information-v2.p.rapidapi.com",
            "method": "POST",
            "param_key": "vehicle_number",
            "content_type": "json"
        },
        {
            "name": "Vehicle PUC API",
            "url": "https://vehicle-puc-api.p.rapidapi.com/",
            "host": "vehicle-puc-api.p.rapidapi.com",
            "method": "POST",
            "param_key": "vehicle_number",
            "content_type": "json"
        },
        {
            "name": "Kyc Hub Node",
            "url": "https://kyc-hub-vehicle-verification.p.rapidapi.com/v1/vehicle", 
            "host": "kyc-hub-vehicle-verification.p.rapidapi.com",
            "method": "GET",
            "param_key": "registration_number",
            "content_type": "json"
        }
    ]

    api_key = "19d2b2bdcemsh4d13904b7f42b0dp136b77jsnb2d3b0d02ec4"
    error_logs = []

    # 🔄 CYCLE THROUGH THE LIVE ENDPOINTS
    for api in api_pool:
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": api["host"]
        }
        
        try:
            if api["method"] == "GET":
                querystring = {api["param_key"]: clean_reg}
                response = requests.get(api["url"], headers=headers, params=querystring, timeout=5)
            else:
                # Differentiate format strategies based on what the snippet requested
                if api["content_type"] == "form":
                    headers["Content-Type"] = "application/x-www-form-urlencoded"
                    form_data = {api["param_key"]: clean_reg}
                    response = requests.post(api["url"], headers=headers, data=form_data, timeout=5)
                else:
                    headers["Content-Type"] = "application/json"
                    json_data = {api["param_key"]: clean_reg}
                    response = requests.post(api["url"], headers=headers, json=json_data, timeout=5)

            if response.status_code == 200:
                return {
                    "status": "Verified Live",
                    "message": f"Real-time records successfully pulled via {api['name']}.",
                    "verified": True,
                    "metadata": response.json()
                }
            else:
                error_logs.append(f"{api['name']} dropped (Status {response.status_code}: {response.text.strip()})")
                continue
                
        except Exception as e:
            error_logs.append(f"{api['name']} experienced connection failure: {str(e)}")
            continue

    # 🛑 NESTED FAILURE FALLBACK ENGINE LOWER FLOOR (Pure live log extraction)
    return {
        "status": "All Live Gateways Exhausted",
        "message": "Could not extract data payload. Every cloud node returned an issue profile.",
        "verified": False,
        "metadata": {
            "Gateway Error Trails": error_logs
        }
    }