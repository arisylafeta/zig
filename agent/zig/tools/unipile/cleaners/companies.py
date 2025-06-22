"""
Unipile API - LinkedIn Companies Response Cleaners

This file contains functions for cleaning and formatting LinkedIn company responses
from the Unipile API to make them suitable for feeding to an LLM.
"""

from typing import Any, Dict, List, Optional

def clean_company_profile(company_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format a company profile response
    
    Args:
        company_profile: The raw company profile response from the API
    
    Returns:
        A cleaned and formatted company profile
    """
    if not company_profile:
        return None

    headquarters = None
    if company_profile.get("locations"):
        for loc in company_profile["locations"]:
            if loc.get("is_headquarter"):
                headquarters = loc
                break

    return {
        "id": company_profile.get("id"),
        "entityUrn": company_profile.get("entity_urn"),
        "name": company_profile.get("name"),
        "description": company_profile.get("description"),
        "publicIdentifier": company_profile.get("public_identifier"),
        "industry": company_profile.get("industry") or [],
        "website": company_profile.get("website"),
        "employeeCount": company_profile.get("employee_count"),
        "employeeCountRange": company_profile.get("employee_count_range"),
        "foundedYear": company_profile.get("founded_year"),
        "headquarters": headquarters,
        "locations": [
            {
                "city": loc.get("city"),
                "country": loc.get("country"),
                "isHeadquarter": loc.get("is_headquarter")
            }
            for loc in company_profile.get("locations", [])
        ] if company_profile.get("locations") else [],
        "hashtags": [tag.get("title") for tag in company_profile.get("hashtags", [])] if company_profile.get("hashtags") else [],
        "logoUrl": company_profile.get("logo_large") or company_profile.get("logo"),
        "profileUrl": company_profile.get("profile_url"),
        "followersCount": company_profile.get("follower_count")
    }

def clean_company_search_results(search_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format company search results
    
    Args:
        search_results: The raw company search results from the API
    
    Returns:
        Cleaned and formatted company search results
    """
    if not search_results or not search_results.get("items"):
        return {"companies": []}

    return {
        "companies": [
            {
                "name": company.get("name"),
                "description": company.get("description") or company.get("summary"),
                "industry": company.get("industry") or [],
                "location": company.get("location"),
                "logoUrl": company.get("logo_large") or company.get("logo"),
                "profileUrl": company.get("profile_url"),
                "publicIdentifier": company.get("public_identifier"),
                "id": company.get("id"),
                "followersCount": company.get("followers_count"),
                "jobOffersCount": company.get("job_offers_count")
            }
            for company in search_results.get("items", [])
        ],
        "paging": search_results.get("paging"),
        "cursor": search_results.get("cursor")
    }