import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


pytestmark = pytest.mark.django_db

class HomeTestPage:
    def test_homepage_url(self,client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200
