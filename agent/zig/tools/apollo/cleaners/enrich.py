"""
This file contains functions to clean and format the raw data from the Apollo API
into a more readable and LLM-friendly format.
"""

from .helpers import clean_person, clean_organization

def clean_people_enrichment(response):
    """
    Cleans the response from the peopleEnrichment API call.
    
    Args:
        response: The raw JSON response from the peopleEnrichment API.
    
    Returns:
        A formatted string summarizing the enriched person data.
    """
    if not response or not response.get("person"):
        return {"person": None}
    return {
        "person": clean_person(response["person"])
    }

def clean_bulk_people_enrichment(response):
    """
    Cleans the response from the bulkPeopleEnrichment API call.
    
    Args:
        response: The raw JSON response from the bulkPeopleEnrichment API.
    
    Returns:
        A formatted string summarizing the enriched people data.
    """
    if not response or not response.get("matches") or len(response.get("matches", [])) == 0:
        return {"matches": []}
    return {
        "matches": [clean_person(match) for match in response["matches"]]
    }

def clean_organization_enrichment(response):
    """
    Cleans the response from the organizationEnrichment API call.
    
    Args:
        response: The raw JSON response from the organizationEnrichment API.
    
    Returns:
        A formatted string summarizing the enriched organization data.
    """
    if not response or not response.get("organization"):
        return {"organization": None}
    return {
        "organization": clean_organization(response["organization"])
    }

def clean_bulk_organization_enrichment(response):
    """
    Cleans the response from the bulkOrganizationEnrichment API call.
    
    Args:
        response: The raw JSON response from the bulkOrganizationEnrichment API.
    
    Returns:
        A formatted string summarizing the enriched organizations data.
    """
    if not response or not response.get("organizations") or len(response.get("organizations", [])) == 0:
        return {"organizations": []}
    return {
        "organizations": [clean_organization(org) for org in response["organizations"]]
    }