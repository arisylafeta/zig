from .config import apollo_config, ApolloError
import aiohttp
from langchain.tools import tool
from .translation.search import extract_people_search_data, PeopleSearchData

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class PeopleSearchParams(BaseModel):
    person_titles: Optional[List[str]] = Field(default=None, description="Job titles held by the people you want to find")
    include_similar_titles: Optional[bool] = Field(default=True, description="Whether to include similar titles")
    person_locations: Optional[List[str]] = Field(default=None, description="The location where people live")
    person_seniorities: Optional[List[str]] = Field(default=None, description="The job seniority that people hold within their current employer")
    organization_locations: Optional[List[str]] = Field(default=None, description="The location of the company headquarters for a person's current employer")
    q_organization_domains_list: Optional[List[str]] = Field(default=None, description="The domain name for the person's employer")
    contact_email_status: Optional[List[str]] = Field(default=None, description="The email statuses for the people you want to find")
    organization_ids: Optional[List[str]] = Field(default=None, description="The Apollo IDs for the companies (employers) you want to include")
    organization_num_employees_ranges: Optional[List[str]] = Field(default=None, description="The number range of employees working for the person's current company")
    q_keywords: Optional[str] = Field(default=None, description="A string of words over which we want to filter the results")
    page: Optional[int] = Field(default=1, description="The page number of the Apollo data that you want to retrieve")
    per_page: Optional[int] = Field(default=10, description="The number of search results that should be returned for each page")


@tool
async def people_search(params: PeopleSearchParams) -> List[PeopleSearchData]:
    """Searches for people in the Apollo database.

    See https://docs.apollo.io/reference/people-search

    Args:
        params (Dict[str, Any]): The search parameters.  Possible keys:
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

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{endpoint}/v1/mixed_people/search",
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
            },
            json={
                "api_key": api_key,
                **params.model_dump(exclude_none=True)
            }
        ) as response:
            if response.status >= 400:
                error_body = await response.text()
                raise ApolloError(
                    response.status,
                    error_body,
                    "Failed to fetch people search results"
                )

            raw_data = await response.json()
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

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{endpoint}/v1/mixed_companies/search",
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
            },
            json={
                "api_key": api_key,
                **params
            }
        ) as response:
            if response.status >= 400:
                error_body = await response.text()
                raise ApolloError(
                    response.status,
                    error_body,
                    "Failed to fetch organization search results"
                )

            raw_data = await response.json()
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
    request_params = {
        "api_key": api_key,
        "page": str(page),
        "per_page": str(per_page)
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
            },
            params=request_params
        ) as response:
            if response.status >= 400:
                error_body = await response.text()
                raise ApolloError(
                    response.status,
                    error_body,
                    "Failed to fetch organization job postings"
                )

            raw_data = await response.json()
            return raw_data
