import http.cookiejar
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets


SEARCH_URL = 'https://search.211colorado.org/search'
SEARCH_PAGE_URL = 'https://search.211colorado.org/search?terms=food&page=1&location=Colorado&service_area=colorado'
ZIP_LOOKUP_URL = 'https://api.zippopotam.us/us/{zip_code}'
COLORADO_CENTER = {'lat': 39.5500507, 'lng': -105.7820674}
ZIP_FALLBACK_TERM = 'help'
DEFAULT_MARKER_LIMIT = 60
MAX_MARKER_LIMIT = 100
DEFAULT_SEARCH_PER_PAGE = 75
PIN_SPREAD_STEP_DEGREES = 0.01
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

CATEGORY_CONFIG = {
    'food': {
        'query': 'food',
    },
    'shelter': {
        'query': 'shelter',
    },
    'clothing': {
        'query': 'clothing',
    },
    'transportation': {
        'query': 'transportation',
    },
    'healthcare': {
        'query': 'healthcare',
    },
}


def _is_zip_code(query):
    return bool(re.fullmatch(r'\d{5}', query))


def _lookup_zip_coordinates(zip_code):
    request = urllib.request.Request(
        ZIP_LOOKUP_URL.format(zip_code=urllib.parse.quote(zip_code)),
        headers={'User-Agent': 'Mozilla/5.0'},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode('utf-8', 'ignore'))

    place = payload['places'][0]
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
        'per_page': DEFAULT_SEARCH_PER_PAGE,
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


def _normalize_category(raw_category):
    return (raw_category or '').strip().lower()


def _safe_float(raw_value, fallback):
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return fallback


def _coerce_int(raw_value, default, minimum, maximum):
    try:
        parsed = int(raw_value)
    except (TypeError, ValueError):
        parsed = default

    return max(minimum, min(maximum, parsed))


def _distance_miles(origin, destination):
    origin_lat = math.radians(origin['lat'])
    origin_lng = math.radians(origin['lng'])
    destination_lat = math.radians(destination['lat'])
    destination_lng = math.radians(destination['lng'])

    delta_lat = destination_lat - origin_lat
    delta_lng = destination_lng - origin_lng

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(origin_lat) * math.cos(destination_lat) * math.sin(delta_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(3958.8 * c, 2)


def _coords_from_211_result(result):
    postal_code = (result.get('postal_code') or '').strip()
    if not postal_code:
        return None

    try:
        return _lookup_zip_coordinates(postal_code)
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, ValueError, json.JSONDecodeError):
        return None


def _build_211_category_markers(category, origin, limit):
    category_query = CATEGORY_CONFIG[category]['query']
    results, total_results = _search_211_colorado(category_query)

    markers = []
    for index, result in enumerate(results):
        coords = _coords_from_211_result(result)
        if not coords:
            continue

        marker = {
            'source': '211',
            'source_id': f'211-{category}-{index}',
            'name': result.get('name') or 'Resource',
            'category': category,
            'address': result.get('address') or '',
            'lat': coords['lat'],
            'lng': coords['lng'],
            'phone': result.get('phone') or '',
            'website': result.get('website') or '',
            'description': result.get('description') or '',
            'distance_miles': _distance_miles(origin, coords),
        }
        markers.append(marker)

    markers.sort(key=lambda marker: (marker['distance_miles'], marker['name']))
    return _spread_overlapping_markers(markers[:limit]), total_results


def _spread_overlapping_markers(markers):
    grouped_markers = {}

    for marker in markers:
        key = (round(marker['lat'], 5), round(marker['lng'], 5))
        grouped_markers.setdefault(key, []).append(marker)

    spread_markers = []
    for group in grouped_markers.values():
        if len(group) == 1:
            spread_markers.append(group[0])
            continue

        for index, marker in enumerate(group):
            angle = (2 * math.pi * index) / len(group)
            offset_lat = math.sin(angle) * PIN_SPREAD_STEP_DEGREES
            offset_lng = math.cos(angle) * PIN_SPREAD_STEP_DEGREES

            spread_marker = dict(marker)
            spread_marker['lat'] = round(marker['lat'] + offset_lat, 6)
            spread_marker['lng'] = round(marker['lng'] + offset_lng, 6)
            spread_marker['original_lat'] = marker['lat']
            spread_marker['original_lng'] = marker['lng']
            spread_markers.append(spread_marker)

    spread_markers.sort(key=lambda marker: (marker['distance_miles'], marker['name']))
    return spread_markers


def map_markers_api(request):
    category = _normalize_category(request.GET.get('category'))
    if category not in CATEGORY_CONFIG:
        return JsonResponse(
            {
                'error': 'Invalid category value.',
                'valid_categories': sorted(CATEGORY_CONFIG.keys()),
            },
            status=400,
        )

    origin = {
        'lat': _safe_float(request.GET.get('lat'), COLORADO_CENTER['lat']),
        'lng': _safe_float(request.GET.get('lng'), COLORADO_CENTER['lng']),
    }
    marker_limit = _coerce_int(
        request.GET.get('limit'),
        DEFAULT_MARKER_LIMIT,
        minimum=1,
        maximum=MAX_MARKER_LIMIT,
    )

    warnings = []
    resource_markers = []
    total_211_results = 0

    try:
        resource_markers, total_211_results = _build_211_category_markers(category, origin, marker_limit)
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, ValueError, json.JSONDecodeError):
        warnings.append('resource_211_unavailable')

    return JsonResponse(
        {
            'category': category,
            'origin': origin,
            'limit': marker_limit,
            'counts': {
                'from_211': len(resource_markers),
                'total_211_results': total_211_results,
                'returned': len(resource_markers),
            },
            'warnings': warnings,
            'markers': resource_markers,
        }
    )


def find_resources(request):
    raw_query = (request.GET.get('q') or '').strip()
    results = []
    total_results = 0
    search_error = ''

    if raw_query:
        try:
            results, total_results = _search_211_colorado(raw_query)
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, ValueError, json.JSONDecodeError):
            search_error = 'Unable to reach the 2-1-1 Colorado database right now.'

    favorited_names = []
    if request.user.is_authenticated:
        favorited_names = list(request.user.favorites.values_list('name', flat=True))

    return render(
        request,
        'resources/find_resources.html',
        {
            'active_tab': 'main',
            'query': raw_query,
            'results': results,
            'total_results': total_results,
            'search_error': search_error,
            'favorited_names': favorited_names,
        }
    )

def find_resources_map(request):
    return render(
        request,
        'resources/find_resources_map.html',
        {
            'active_tab': 'map',
            'colorado_center': COLORADO_CENTER,
        },
    )

def find_resources_personalized(request):
    return render(request, 'resources/find_resources_personalized.html', {'active_tab': 'personalized'})


class ResourceViewSet(viewsets.ModelViewSet):
    pass