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
