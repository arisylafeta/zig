def clean_person(person):
    name = person.get("name")
    title = person.get("title")
    headline = person.get("headline")
    linkedin_url = person.get("linkedin_url")
    city = person.get("city")
    state = person.get("state")
    country = person.get("country")
    organization = person.get("organization")
    employment_history = person.get("employment_history")

    cleaned_person = {
        "name": name,
        "title": title,
        "headline": headline,
        "linkedin_url": linkedin_url,
        "location": f"{city}, {state}, {country}" if city and state and country else None,
        "current_organization": clean_organization(organization) if organization else None,
        "employment_history": [
            {
                "title": job.get("title"),
                "organization_name": job.get("organization_name"),
                "start_date": job.get("start_date"),
                "end_date": job.get("end_date", "Present")
            }
            for job in employment_history
        ] if employment_history else None
    }

    # remove None fields
    cleaned_person = {k: v for k, v in cleaned_person.items() if v is not None}

    return cleaned_person

def clean_organization(org):
    name = org.get("name")
    website_url = org.get("website_url")
    linkedin_url = org.get("linkedin_url")
    primary_domain = org.get("primary_domain")
    founded_year = org.get("founded_year")
    annual_revenue_printed = org.get("annual_revenue_printed")  # from enrichment
    organization_revenue_printed = org.get("organization_revenue_printed")  # from search
    estimated_num_employees = org.get("estimated_num_employees")
    industry = org.get("industry")
    keywords = org.get("keywords")
    short_description = org.get("short_description")
    total_funding_printed = org.get("total_funding_printed")
    latest_funding_stage = org.get("latest_funding_stage")

    cleaned_org = {
        "name": name,
        "website_url": website_url,
        "linkedin_url": linkedin_url,
        "domain": primary_domain,
        "founded_year": founded_year,
        "revenue": annual_revenue_printed or organization_revenue_printed,
        "employees": estimated_num_employees,
        "industry": industry,
        "latest_funding": latest_funding_stage,
        "total_funding": total_funding_printed,
        "description": short_description,
        "keywords": keywords[:10] if keywords else None
    }

    # remove None fields
    cleaned_org = {k: v for k, v in cleaned_org.items() if v is not None}

    return cleaned_org