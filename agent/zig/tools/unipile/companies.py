"""
Unipile API - LinkedIn Companies

This file contains functions for interacting with LinkedIn companies via the Unipile API.
"""

import json
from typing import List, Dict, Any, Optional, Union
from .config import get_base_url, get_headers, make_request, ensure_account_id
from .cleaners.companies import clean_company_profile, clean_company_search_results

# Types
class LinkedInCompanyLocation:
    is_headquarter: bool
    city: str
    country: str
    street: List[str]
    postalCode: Optional[str]
    area: Optional[str]

class LinkedInCompany:
    object: str
    provider: str
    provider_id: str
    entity_urn: str
    name: str
    description: Optional[str]
    founded_year: Optional[int]
    locations: List[LinkedInCompanyLocation]
    messaging: Optional[Dict[str, Any]]
    activities: Optional[List[str]]
    website: Optional[str]
    employee_count: Optional[int]
    employee_count_range: Optional[Dict[str, Optional[int]]]
    industry: Optional[List[str]]
    logo: Optional[str]
    logo_large: Optional[str]

"""
Get details about a LinkedIn company

@param identifier - The LinkedIn company identifier (e.g., "linkedin")
@param account_id - Optional account ID (will use env var if not provided)
@returns The LinkedIn company profile
"""
async def get_company_profile(
    identifier: str,
    account_id: Optional[str] = None,
    raw: bool = False
) -> Any:
    if not identifier:
        raise Exception('Company identifier is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/linkedin/company/{identifier}?account_id={id_to_use}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_company_profile(response)

"""
Search for LinkedIn companies

@param keywords - The search keywords
@param account_id - Optional account ID (will use env var if not provided)
@param limit - Optional limit for the number of results
@returns LinkedIn company search results
"""
async def search_companies(
    keywords: str,
    account_id: Optional[str] = None,
    limit: Optional[int] = None,
    raw: bool = False
) -> Any:
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
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_company_search_results(response)