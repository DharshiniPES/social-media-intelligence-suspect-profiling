import os
import re
import json
import requests
import streamlit as st

def verify_and_route_vehicle(registration_number):
    """
    Verify an Indian vehicle registration using the
    RapidAPI RTO Vehicle Details API.
    """

    # Normalize input string by removing spaces/hyphens and turning to uppercase
    clean_reg = re.sub(r"[^A-Za-z0-9]", "", registration_number).upper()

    # Validate standard Indian registration syntax
    if not re.match(r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$", clean_reg):
        return {
            "status": "Syntax Mismatch",
            "message": "Invalid Indian vehicle registration format.",
            "verified": False,
            "metadata": {}
        }

    # API key selection sequence (Environment variable fallback to active portal token)
    api_key = os.getenv("RAPIDAPI_KEY") 
    if not api_key:
            return {
                "status": "Configuration Error",
                "message": "RAPIDAPI_KEY not found in system environment variables.",
                "verified": False,
                "metadata": {}
            }

    url = "https://rto-vehicle-details5.p.rapidapi.com/address"

    # Set required authentication and payload content parameters
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "rto-vehicle-details5.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    # Map target parameter inside the JSON payload body using proper uppercase structure
    payload = {
        "Registration": clean_reg
    }

    try:
        # Execute active HTTP POST request to clear 403 authorization routing conflicts
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )
        
        # Streamlit live logging trace matrices
        st.write("Status Code:", response.status_code)
        st.code(response.text)

        if response.status_code == 200:
            data_payload = response.json()
            
            # Return standardized evidence dictionary schema to satisfy pipeline pipeline/intelligence_pipeline.py runs
            return {
                "status": "Verified Live",
                "message": "Vehicle details retrieved successfully.",
                "verified": True,
                "source": "Vehicle Verification API",
                "title": f"RTO Profile: {clean_reg}",
                "description": "Live query via RTO Vehicle Details Hub.",
                # Serialize the object into text formatting to shield downstream text-analyzers from NoneType errors
                "visible_text": json.dumps(data_payload, indent=2), 
                "metadata": data_payload
            }

        return {
            "status": "API Error",
            "message": f"RapidAPI returned {response.status_code}",
            "verified": False,
            "visible_text": f"Error payload returned: {response.text}",
            "metadata": {
                "response": response.text
            }
        }

    except requests.exceptions.Timeout:
        return {
            "status": "Timeout",
            "message": "RapidAPI request timed out.",
            "verified": False,
            "visible_text": "Connection to the cloud registry timed out.",
            "metadata": {}
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "Connection Error",
            "message": str(e),
            "verified": False,
            "visible_text": f"Connection exception: {str(e)}",
            "metadata": {}
        }