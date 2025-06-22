from .cleaners.enrich import (
    clean_people_enrichment,
    clean_bulk_people_enrichment,
    clean_organization_enrichment,
    clean_bulk_organization_enrichment
)
from .config import apollo_config, ApolloError
import json
import requests

"""
The parameters for the people_enrichment function.
See https://docs.apollo.io/reference/people-enrichment

Parameters:
    first_name (str, optional): The person's first name.
    last_name (str, optional): The person's last name.
    name (str, optional): The person's full name.
    domain (str, optional): The domain name of the person's current employer.
    email (str, optional): The email address of the person.
    linkedin_url (str, optional): The LinkedIn profile URL of the person.
    reveal_personal_emails (bool, optional): Whether to reveal personal emails. Default is False.
    reveal_phone_number (bool, optional): Whether to reveal phone numbers. Default is False.
    raw (bool, optional): Whether to return the raw API response.
"""

async def people_enrichment(params):
    """
    Enriches data for a single person.
    See https://docs.apollo.io/reference/people-enrichment
    
    Args:
        params: The parameters to identify the person.
    
    Returns:
        The enriched person data.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    
    raw = params.pop("raw", False)
    
    response = requests.post(
        f"{endpoint}/v1/people/match",
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        },
        json={
            "api_key": api_key,
            **params
        }
    )
    
    if not response.ok:
        error_body = response.text
        raise ApolloError(
            response.status_code,
            error_body,
            "Failed to fetch person enrichment data"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_people_enrichment(raw_data)

"""
The parameters for the bulk_people_enrichment function.
See https://docs.apollo.io/reference/bulk-people-enrichment

Parameters:
    details (list): An array of person details to enrich.
                   Each object should conform to the PeopleEnrichmentParameters interface.
    reveal_personal_emails (bool, optional): Whether to reveal personal emails for all people in the request. Default is False.
    reveal_phone_number (bool, optional): Whether to reveal phone numbers for all people in the request. Default is False.
    raw (bool, optional): Whether to return the raw API response.
"""

async def bulk_people_enrichment(params):
    """
    Enriches data for up to 10 people in a single API call.
    See https://docs.apollo.io/reference/bulk-people-enrichment
    
    Args:
        params: The parameters for bulk enrichment.
    
    Returns:
        The enriched data for the people.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    
    raw = params.pop("raw", False)
    
    response = requests.post(
        f"{endpoint}/v1/people/bulk_match",
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        },
        json={
            "api_key": api_key,
            **params
        }
    )
    
    if not response.ok:
        error_body = response.text
        raise ApolloError(
            response.status_code,
            error_body,
            "Failed to fetch bulk person enrichment data"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_bulk_people_enrichment(raw_data)

"""
The parameters for the organization_enrichment function.
See https://docs.apollo.io/reference/organization-enrichment

Parameters:
    domain (str): The domain name of the organization to enrich.
    raw (bool, optional): Whether to return the raw API response.
"""

async def organization_enrichment(params):
    """
    Enriches data for a single organization.
    See https://docs.apollo.io/reference/organization-enrichment
    
    Args:
        params: The parameters to identify the organization.
    
    Returns:
        The enriched organization data.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    domain = params.get("domain")
    raw = params.get("raw", False)
    
    url = f"{endpoint}/v1/organizations/enrich"
    params = {
        "api_key": api_key,
        "domain": domain
    }
    
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        },
        params=params
    )
    
    if not response.ok:
        error_body = response.text
        raise ApolloError(
            response.status_code,
            error_body,
            "Failed to fetch organization enrichment data"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_organization_enrichment(raw_data)

"""
The parameters for the bulk_organization_enrichment function.
See https://docs.apollo.io/reference/bulk-organization-enrichment

Parameters:
    domains (list): An array of domain names to enrich.
    raw (bool, optional): Whether to return the raw API response.
"""

async def bulk_organization_enrichment(params):
    """
    Enriches data for up to 10 organizations in a single API call.
    See https://docs.apollo.io/reference/bulk-organization-enrichment
    
    Args:
        params: The parameters for bulk enrichment.
    
    Returns:
        The enriched data for the organizations.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    domains = params.get("domains", [])
    raw = params.get("raw", False)
    
    response = requests.post(
        f"{endpoint}/v1/organizations/bulk_enrich",
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        },
        json={
            "api_key": api_key,
            "domains": domains
        }
    )
    
    if not response.ok:
        error_body = response.text
        raise ApolloError(
            response.status_code,
            error_body,
            "Failed to fetch bulk organization enrichment data"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_bulk_organization_enrichment(raw_data)