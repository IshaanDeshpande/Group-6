import http.cookiejar
import json
import re
import urllib.error
import urllib.parse
import urllib.request

from django.shortcuts import render
from rest_framework import viewsets


SEARCH_URL = 'https://search.211colorado.org/search'
SEARCH_PAGE_URL = 'https://search.211colorado.org/search?terms=food&page=1&location=Colorado&service_area=colorado'
ZIP_LOOKUP_URL = 'https://api.zippopotam.us/us/{zip_code}'
COLORADO_CENTER = {'lat': 39.5500507, 'lng': -105.7820674}
ZIP_FALLBACK_TERM = 'help'
OUTSIDE_COLORADO_ERROR = 'Sorry, this zip code is outside of colorado and is not currently in our database.'
HOMELESSNESS_KEYWORDS = (
    'homeless',
    'homelessness',
    'shelter',
    'emergency shelter',
    'transitional housing',
    'rapid rehousing',
    'supportive housing',
    'street outreach',
    'rental assistance',
    'eviction',
    'housing',
    'rent',
)


def _is_zip_code(query):
    return bool(re.fullmatch(r'\d{5}', query))


class OutsideColoradoZipError(Exception):
    pass


def _lookup_zip_coordinates(zip_code):
    request = urllib.request.Request(
        ZIP_LOOKUP_URL.format(zip_code=urllib.parse.quote(zip_code)),
        headers={'User-Agent': 'Mozilla/5.0'},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode('utf-8', 'ignore'))

    places = payload.get('places') or []
    if not places:
        raise KeyError('No ZIP data found')

    state_abbreviation = (places[0].get('state abbreviation') or '').upper()
    if state_abbreviation != 'CO':
        raise OutsideColoradoZipError()

    place = places[0]
    return {
        'lat': float(place['latitude']),
        'lng': float(place['longitude']),
    }


def _format_result(item):
    address_parts = [
        item.get('address_1') or '',
        item.get('city') or '',
        item.get('state') or '',
        item.get('postal_code') or '',
    ]
    address = ', '.join(part for part in address_parts if part).replace(', ,', ',')

    phone = ''
    for phone_source in (
        item.get('phones') or [],
        item.get('site_phones') or {},
        item.get('agency_phones') or {},
    ):
        if isinstance(phone_source, list):
            for phone_value in phone_source:
                if phone_value:
                    phone = phone_value
                    break
        elif isinstance(phone_source, dict):
            for key in ('phone_1', 'phone_hotline', 'phone_toll_free'):
                if phone_source.get(key):
                    phone = phone_source[key]
                    break
        if phone:
            break

    website = item.get('website') or item.get('agency_website') or item.get('program_site_website') or ''
    if website and not website.startswith(('http://', 'https://')):
        website = f'http://{website}'

    return {
        'name': item.get('name') or item.get('agency_name') or 'Resource',
        'agency_name': item.get('agency_name') or '',
        'description': item.get('description') or '',
        'address': address,
        'phone': phone,
        'website': website,
        'county': item.get('county') or '',
        'postal_code': item.get('postal_code') or '',
    }


def _rank_homelessness_relevance(result, query):
    haystack = ' '.join(
        value.lower()
        for value in (
            result.get('name') or '',
            result.get('agency_name') or '',
            result.get('description') or '',
            result.get('address') or '',
            result.get('county') or '',
        )
    )

    score = 0

    if query:
        query_lower = query.lower()
        if query_lower in haystack:
            score += 20

    for index, keyword in enumerate(HOMELESSNESS_KEYWORDS):
        if keyword in haystack:
            score += max(0, 12 - index)

    if result.get('name') and any(keyword in result['name'].lower() for keyword in ('shelter', 'homeless', 'housing')):
        score += 8

    if result.get('description') and any(keyword in result['description'].lower() for keyword in ('homeless', 'shelter', 'housing', 'rent', 'eviction')):
        score += 5

    return score


def _search_211_colorado(query):
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    page_request = urllib.request.Request(SEARCH_PAGE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    page_html = opener.open(page_request, timeout=30).read().decode('utf-8', 'ignore')
    csrf_match = re.search(r'name="csrf-token" content="([^"]+)"', page_html)
    csrf_token = csrf_match.group(1) if csrf_match else ''

    location = query if _is_zip_code(query) else 'Colorado'
    coords = _lookup_zip_coordinates(query) if _is_zip_code(query) else COLORADO_CENTER
    terms = [ZIP_FALLBACK_TERM] if _is_zip_code(query) else [query]

    payload = {
        'page': 1,
        'per_page': 25,
        'location': location,
        'service_area': 'colorado',
        'submitted_through_form': True,
        'terms': terms,
        'coords': coords,
        'taxonomy_code': [],
        'taxonomies': [],
        'related_terms': [],
        'notices': {'hark': False},
    }

    search_request = urllib.request.Request(
        SEARCH_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-Token': csrf_token,
            'Referer': SEARCH_PAGE_URL,
        },
        method='POST',
    )

    with opener.open(search_request, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8', 'ignore'))

    formatted_results = [
        _format_result(item)
        for item in result.get('results', [])
    ]
    formatted_results.sort(
        key=lambda resource: (
            -_rank_homelessness_relevance(resource, query),
            resource.get('name') or '',
        )
    )

    return formatted_results, result.get('total_results', 0)


def find_resources(request):
    raw_query = (request.GET.get('q') or '').strip()
    results = []
    total_results = 0
    search_error = ''

    if raw_query:
        try:
            results, total_results = _search_211_colorado(raw_query)
        except OutsideColoradoZipError:
            search_error = OUTSIDE_COLORADO_ERROR
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, ValueError, json.JSONDecodeError):
            search_error = 'Unable to reach the 2-1-1 Colorado database right now.'

    return render(
        request,
        'resources/find_resources.html',
        {
            'active_tab': 'main',
            'query': raw_query,
            'results': results,
            'total_results': total_results,
            'search_error': search_error,
        },
    )

def find_resources_map(request):
    return render(request, 'resources/find_resources_map.html', {'active_tab': 'map'})

def find_resources_personalized(request):
    return render(request, 'resources/find_resources_personalized.html', {'active_tab': 'personalized'})


class ResourceViewSet(viewsets.ModelViewSet):
    pass
