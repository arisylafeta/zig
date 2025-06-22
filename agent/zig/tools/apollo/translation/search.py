import json
from typing import Dict, List, Any, Optional


def extract_people_search_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract relevant fields from Apollo peopleSearch response according to requirements:
    1. First Name
    2. Last Name
    3. Linkedin Url
    4. Email Status
    5. Email if != email_not_unlocked@domain.com else "Unlock"
    6. From employment_history[0], get title, and organization name
    7. Location, as City, State
    
    Args:
        data: The raw peopleSearch response data
        
    Returns:
        List of dictionaries with extracted fields for each person
    """
    result = []
    
    for person in data.get("people", []):
        # Extract basic information
        first_name = person.get("first_name", "")
        last_name = person.get("last_name", "")
        linkedin_url = person.get("linkedin_url", "")
        email_status = person.get("email_status", "")
        
        # Handle email according to requirement
        email = person.get("email", "")
        if email == "email_not_unlocked@domain.com":
            email = "Unlock"
            
        # Get employment history information if available
        employment_info = {"title": "", "organization": ""}
        if person.get("employment_history") and len(person["employment_history"]) > 0:
            employment = person["employment_history"][0]
            employment_info["title"] = employment.get("title", "")
            employment_info["organization"] = employment.get("organization_name", "")
            
        # Format location
        city = person.get("city", "")
        state = person.get("state", "")
        location = f"{city}, {state}" if city and state else city or state or ""
        
        # Create person entry
        person_data = {
            "first_name": first_name,
            "last_name": last_name,
            "linkedin_url": linkedin_url,
            "email_status": email_status,
            "email": email,
            "title": employment_info["title"],
            "organization": employment_info["organization"],
            "location": location
        }
        
        result.append(person_data)
        
    return result


def test_extract_people_search_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Test function to extract data from a peopleSearch.json file
    
    Args:
        file_path: Path to the peopleSearch.json file
        
    Returns:
        Extracted data
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return extract_people_search_data(data)

def main():
    file_path = "../../../tests/apollo/responses/peopleSearch.json"
    data = test_extract_people_search_data(file_path)
    print(data)

if __name__ == "__main__":
    main()