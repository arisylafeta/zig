from .cleaners.search import (
    clean_people_search,
    clean_organization_search,
    clean_organization_job_postings
)
from .config import apollo_config, ApolloError
import json
import requests

"""
The parameters for the people_search function.
See https://docs.apollo.io/reference/people-search

Parameters:
    q_person_name (str, optional): The name of the person you want to find.
    person_titles (list, optional): Job titles held by the people you want to find.
    include_similar_titles (bool, optional): Whether to include similar titles. Default is True.
    person_locations (list, optional): The location where people live.
    person_seniorities (list, optional): The job seniority that people hold within their current employer.
    organization_locations (list, optional): The location of the company headquarters for a person's current employer.
    q_organization_domains_list (list, optional): The domain name for the person's employer.
    contact_email_status (list, optional): The email statuses for the people you want to find.
    organization_ids (list, optional): The Apollo IDs for the companies (employers) you want to include.
    organization_num_employees_ranges (list, optional): The number range of employees working for the person's current company.
    q_keywords (str, optional): A string of words over which we want to filter the results.
    page (int, optional): The page number of the Apollo data that you want to retrieve. Default is 1.
    per_page (int, optional): The number of search results that should be returned for each page. Default is 10.
    raw (bool, optional): Whether to return the raw API response.
"""

async def people_search(params):
    """
    Searches for people in the Apollo database.
    See https://docs.apollo.io/reference/people-search
    
    Args:
        params: The search parameters.
    
    Returns:
        The search results.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    
    raw = params.pop("raw", False)
    
    response = requests.post(
        f"{endpoint}/v1/mixed_people/search",
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
            "Failed to fetch people search results"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_people_search(raw_data)

"""
The parameters for the organization_search function.
This is not an exhaustive list.
See https://docs.apollo.io/reference/organization-search

Parameters:
    q_organization_name (str, optional): The name of the organization you want to find.
    organization_locations (list, optional): The location of the company headquarters.
    q_organization_domains (list, optional): The domain name for the organization.
    organization_num_employees_ranges (list, optional): The number range of employees working for the organization.
    organization_industries (list, optional): The industries of the organization.
    page (int, optional): The page number of the Apollo data that you want to retrieve. Default is 1.
    per_page (int, optional): The number of search results that should be returned for each page. Default is 10.
    raw (bool, optional): Whether to return the raw API response.
"""

async def organization_search(params):
    """
    Searches for organizations in the Apollo database.
    See https://docs.apollo.io/reference/organization-search
    
    Args:
        params: The search parameters.
    
    Returns:
        The search results.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    
    raw = params.pop("raw", False)
    
    response = requests.post(
        f"{endpoint}/v1/mixed_companies/search",
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
            "Failed to fetch organization search results"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_organization_search(raw_data)

"""
The parameters for the organization_job_postings function.
See https://docs.apollo.io/reference/organization-job-postings

Parameters:
    organization_id (str): The Apollo ID for the company.
    page (int, optional): The page number of the Apollo data that you want to retrieve. Default is 1.
    per_page (int, optional): The number of search results that should be returned for each page. Default is 10.
    raw (bool, optional): Whether to return the raw API response.
"""

async def organization_job_postings(params):
    """
    Retrieves the current job postings for a company.
    See https://docs.apollo.io/reference/organization-job-postings
    
    Args:
        params: The parameters.
    
    Returns:
        The job postings.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    organization_id = params.get("organization_id")
    page = params.get("page", 1)
    per_page = params.get("per_page", 10)
    raw = params.get("raw", False)
    
    url = f"{endpoint}/v1/organizations/{organization_id}/job_postings"
    params = {
        "api_key": api_key,
        "page": str(page),
        "per_page": str(per_page)
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
            "Failed to fetch organization job postings"
        )
    
    raw_data = response.json()
    if raw:
        return raw_data
    return clean_organization_job_postings(raw_data)