from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class ResourceSearchTests(TestCase):
    @patch("apps.resources.views._search_211_colorado")
    def test_search_by_service_name_uses_211_database(self, search_211_mock):
        search_211_mock.return_value = ([
            {
                "name": "Community Kitchen",
                "agency_name": "Helping Hands",
                "description": "Hot meals and meal support.",
                "address": "123 Main St, Denver, CO 80202",
                "phone": "(303) 555-0101",
                "website": "helpinghands.org",
            }
        ], 1)

        response = self.client.get(reverse("resources:find_resources"), {"q": "kitchen"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Community Kitchen")
        self.assertContains(response, "Hot meals and meal support.")
        search_211_mock.assert_called_once_with("kitchen")

    @patch("apps.resources.views._search_211_colorado")
    def test_search_by_zip_code_uses_zip_query(self, search_211_mock):
        search_211_mock.return_value = ([
            {
                "name": "Food Pantry",
                "agency_name": "Summit Pet Food Pantry",
                "description": "Free groceries and pantry staples.",
                "address": "310 Wellington Rd, Breckenridge, CO 80424",
                "phone": "(970) 555-0101",
                "website": "summitpetfoodpantry.org",
            }
        ], 1)

        response = self.client.get(reverse("resources:find_resources"), {"q": "80424"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Food Pantry")
        self.assertContains(response, "80424")
        search_211_mock.assert_called_once_with("80424")

    def test_homelessness_related_results_rank_first(self):
        from apps.resources.views import _rank_homelessness_relevance

        homeless_resource = {
            "name": "Emergency Shelter",
            "agency_name": "Safe Haven",
            "description": "Temporary shelter for people experiencing homelessness.",
            "address": "99 Shelter Ave, Denver, CO 80203",
            "county": "Denver County",
        }
        generic_resource = {
            "name": "Community Library",
            "agency_name": "City Library",
            "description": "Free Wi-Fi and public computers.",
            "address": "1 Library Way, Denver, CO 80202",
            "county": "Denver County",
        }

        self.assertGreater(
            _rank_homelessness_relevance(homeless_resource, "help"),
            _rank_homelessness_relevance(generic_resource, "help"),
        )

<<<<<<< HEAD
    def test_map_markers_api_rejects_unknown_category(self):
        response = self.client.get(reverse("resources:map_markers_api"), {"category": "unknown"})

        self.assertEqual(response.status_code, 400)
        payload = response.json()
        self.assertIn("valid_categories", payload)

    def test_spread_overlapping_markers_offsets_duplicate_coordinates(self):
        from apps.resources.views import _spread_overlapping_markers

        markers = [
            {
                "source": "211",
                "source_id": "1",
                "name": "A",
                "category": "food",
                "address": "123 Main St",
                "lat": 39.7392,
                "lng": -104.9903,
                "phone": "",
                "website": "",
                "description": "",
                "distance_miles": 1.0,
            },
            {
                "source": "211",
                "source_id": "2",
                "name": "B",
                "category": "food",
                "address": "124 Main St",
                "lat": 39.7392,
                "lng": -104.9903,
                "phone": "",
                "website": "",
                "description": "",
                "distance_miles": 1.1,
            },
        ]

        spread = _spread_overlapping_markers(markers)

        self.assertEqual(len(spread), 2)
        self.assertNotEqual((spread[0]["lat"], spread[0]["lng"]), (spread[1]["lat"], spread[1]["lng"]))
        self.assertEqual(spread[0]["original_lat"], 39.7392)
        self.assertEqual(spread[0]["original_lng"], -104.9903)

    @patch("apps.resources.views._build_211_category_markers")
    def test_map_markers_api_returns_211_markers(self, resource_markers_mock):
        resource_markers_mock.return_value = ([
            {
                "source": "211",
                "source_id": "211-food-0",
                "name": "Food Pantry",
                "category": "food",
                "address": "123 Main St",
                "lat": 39.7392,
                "lng": -104.9903,
                "phone": "(303) 555-0101",
                "website": "https://example.org",
                "description": "Pantry support",
                "distance_miles": 1.2,
            }
        ], 1)

        response = self.client.get(reverse("resources:map_markers_api"), {"category": "food"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["category"], "food")
        self.assertEqual(payload["counts"]["returned"], 1)
        self.assertEqual(len(payload["markers"]), 1)
=======
    @patch("apps.resources.views._search_211_colorado")
    def test_non_colorado_zip_shows_outside_database_error(self, search_211_mock):
        from apps.resources.views import OutsideColoradoZipError

        search_211_mock.side_effect = OutsideColoradoZipError()

        response = self.client.get(reverse("resources:find_resources"), {"q": "90210"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Sorry, this zip code is outside of colorado and is not currently in our database.",
        )
>>>>>>> 5fe4348004f665276c5c77561ff6bee6e4c11571
