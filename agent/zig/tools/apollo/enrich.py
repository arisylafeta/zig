from .config import apollo_config, ApolloError
import json
import requests
from langchain_core.tools import tool

from typing import Dict, List, Any

@tool
async def people_enrichment(params: Dict[str, Any]) -> Dict[str, Any]:
    """Enriches data for a single person in the Apollo database.

    See https://docs.apollo.io/reference/people-enrichment

    Args:
        params (Dict[str, Any]): The parameters to identify the person. Possible keys:
            first_name (str, optional): The person's first name.
            last_name (str, optional): The person's last name.
            name (str, optional): The person's full name.
            domain (str, optional): The domain name of the person's current employer.
            email (str, optional): The email address of the person.
            linkedin_url (str, optional): The LinkedIn profile URL of the person.
            reveal_personal_emails (bool, optional): Whether to reveal personal emails. Default is False.
            reveal_phone_number (bool, optional): Whether to reveal phone numbers. Default is False.

    Returns:
        Dict[str, Any]: A dictionary containing the enriched person data.

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    
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
    return raw_data

@tool
async def bulk_people_enrichment(params: Dict[str, Any]) -> Dict[str, Any]:
    """Enriches data for up to 10 people in a single API call.

    See https://docs.apollo.io/reference/bulk-people-enrichment

    Args:
        params (Dict[str, Any]): The parameters for bulk enrichment. Possible keys:
            details (List[Dict[str, Any]]): An array of person details to enrich.
                Each object should include one or more of the following fields:
                first_name (str, optional): The person's first name.
                last_name (str, optional): The person's last name.
                name (str, optional): The person's full name.
                domain (str, optional): The domain name of the person's current employer.
                email (str, optional): The email address of the person.
                linkedin_url (str, optional): The LinkedIn profile URL of the person.
            reveal_personal_emails (bool, optional): Whether to reveal personal emails for all people in the request. Default is False.
            reveal_phone_number (bool, optional): Whether to reveal phone numbers for all people in the request. Default is False.

    Returns:
        Dict[str, Any]: A dictionary containing the enriched data for the people.

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    
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
    return raw_data


@tool
async def organization_enrichment(params: Dict[str, Any]) -> Dict[str, Any]:
    """Enriches data for a single organization in the Apollo database.

    See https://docs.apollo.io/reference/organization-enrichment

    Args:
        params (Dict[str, Any]): The parameters to identify the organization. Possible keys:
            domain (str): The domain name of the organization to enrich.

    Returns:
        Dict[str, Any]: A dictionary containing the enriched organization data.

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    domain = params.get("domain")
    
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
    return raw_data

@tool
async def bulk_organization_enrichment(params: Dict[str, Any]) -> Dict[str, Any]:
    """Enriches data for up to 10 organizations in a single API call.

    See https://docs.apollo.io/reference/bulk-organization-enrichment

    Args:
        params (Dict[str, Any]): The parameters for bulk enrichment. Possible keys:
            domains (List[str]): An array of domain names to enrich (up to 10).

    Returns:
        Dict[str, Any]: A dictionary containing the enriched data for the organizations.

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    domains = params.get("domains", [])
    
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
    return raw_data