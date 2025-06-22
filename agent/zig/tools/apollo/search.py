from .config import apollo_config, ApolloError
import requests
from langchain.tools import tool
from .translation.search import extract_people_search_data

from typing import Dict, List, Any

@tool
async def people_search(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Searches for people in the Apollo database.

    See https://docs.apollo.io/reference/people-search

    Args:
        params (Dict[str, Any]): The search parameters.  Possible keys:
            q_person_name (str, optional): The name of the person you want to find.
            person_titles (List[str], optional): Job titles held by the people you want to find.
            include_similar_titles (bool, optional): Whether to include similar titles. Default is True.
            person_locations (List[str], optional): The location where people live.
            person_seniorities (List[str], optional): The job seniority that people hold within their current employer.
            organization_locations (List[str], optional): The location of the company headquarters for a person's current employer.
            q_organization_domains_list (List[str], optional): The domain name for the person's employer.
            contact_email_status (List[str], optional): The email statuses for the people you want to find.
            organization_ids (List[str], optional): The Apollo IDs for the companies (employers) you want to include.
            organization_num_employees_ranges (List[str], optional): The number range of employees working for the person's current company.
            q_keywords (str, optional): A string of words over which we want to filter the results.
            page (int, optional): The page number of the Apollo data that you want to retrieve. Default is 1.
            per_page (int, optional): The number of search results that should be returned for each page. Default is 10.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a person.

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]

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
    return extract_people_search_data(raw_data)

@tool
async def organization_search(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Searches for organizations in the Apollo database.

    See https://docs.apollo.io/reference/organization-search

    Args:
        params (Dict[str, Any]): The search parameters. Possible keys:
            q_organization_name (str, optional): The name of the organization you want to find.
            organization_locations (List[str], optional): The location of the company headquarters.
            q_organization_domains (List[str], optional): The domain name for the organization.
            organization_num_employees_ranges (List[str], optional): The number range of employees working for the organization.
            organization_industries (List[str], optional): The industries of the organization.
            page (int, optional): The page number of the Apollo data that you want to retrieve. Default is 1.
            per_page (int, optional): The number of search results that should be returned for each page. Default is 10.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents an organization.

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]

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
    return raw_data

@tool
async def organization_job_postings(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Retrieves the current job postings for a company.

    See https://docs.apollo.io/reference/organization-job-postings

    Args:
        params (Dict[str, Any]): The search parameters. Possible keys:
            organization_id (str): The Apollo ID for the company.
            page (int, optional): The page number of the Apollo data that you want to retrieve. Default is 1.
            per_page (int, optional): The number of search results that should be returned for each page. Default is 10.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a job posting.           

    Raises:
        ApolloError: If the Apollo API returns an error.
    """
    api_key = apollo_config["apiKey"]
    endpoint = apollo_config["endpoint"]
    organization_id = params.get("organization_id")
    page = params.get("page", 1)
    per_page = params.get("per_page", 10)

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
    return raw_data
