"""
Unipile API - LinkedIn Companies

This file contains functions for interacting with LinkedIn companies via the Unipile API.
"""
import json
from typing import List, Dict, Any, Optional
from .config import get_base_url, get_headers, make_request, ensure_account_id
from langchain_core.tools import tool

# Types
# class LinkedInCompanyLocation:
#     is_headquarter: bool
#     city: str
#     country: str
#     street: List[str]
#     postalCode: Optional[str]
#     area: Optional[str]

# class LinkedInCompany:
#     object: str
#     provider: str
#     provider_id: str
#     entity_urn: str
#     name: str
#     description: Optional[str]
#     founded_year: Optional[int]
#     locations: List[LinkedInCompanyLocation]
#     messaging: Optional[Dict[str, Any]]
#     activities: Optional[List[str]]
#     website: Optional[str]
#     employee_count: Optional[int]
#     employee_count_range: Optional[Dict[str, Optional[int]]]
#     industry: Optional[List[str]]
#     logo: Optional[str]
#     logo_large: Optional[str]

@tool
async def get_company_profile(
    identifier: str,
    account_id: Optional[str] = None
) -> Any:
    """Retrieves detailed information about a LinkedIn company profile using the company's identifier.

    This function fetches comprehensive details about a LinkedIn company, including its name, 
    description, industry, employee count, locations, website, and other profile information.

    See https://docs.unipile.com/reference/linkedin-company-profile

    Args:
        identifier (str): The LinkedIn company identifier, which can be the company's public name 
                         in the URL (e.g., "linkedin" from linkedin.com/company/linkedin) or 
                         their unique provider ID.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided, 
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.

    Returns:
        Any: The raw API response containing the company profile information.

    Raises:
        Exception: If the company identifier is not provided or if there's an API error.
    """
    if not identifier:
        raise Exception('Company identifier is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/linkedin/company/{identifier}?account_id={id_to_use}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    return response


async def search_companies(
    keywords: str,
    account_id: Optional[str] = None,
    limit: Optional[int] = None
) -> Any:
    """Searches for LinkedIn companies based on provided keywords.

    This function allows you to search for companies on LinkedIn using specific keywords
    and returns a list of matching company profiles. The search results can be limited
    to control the number of returned items.

    See https://docs.unipile.com/reference/linkedin-search-companies

    Args:
        keywords (str): The search terms to find relevant companies. Can include company names,
                       industries, locations, or other identifying information.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        limit (Optional[int]): Maximum number of search results to return. Defaults to 10 if not specified.

    Returns:
        Any: The raw API response containing a list of company objects matching the search criteria.

    Raises:
        Exception: If no search keywords are provided or if there's an API error.
    """
    if not keywords:
        raise Exception('Search keywords are required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/linkedin/search?account_id={id_to_use}"
    
    response = await make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps({
            'api': 'classic',
            'category': 'companies',
            'keywords': keywords,
            'account_id': id_to_use,
            'limit': limit or 10
        })
    })
    
    return response