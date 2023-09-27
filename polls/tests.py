import pytest
import random
from datetime import date
from rest_framework.reverse import reverse
from model_bakery import baker

from polls.models import Restaurant, Menu, Vote
from polls.serializers import MenuSerializer
from users.models import User


pytestmark = pytest.mark.django_db


def test_restaurant_get(user):
    # list
    baker.make(Restaurant, _quantity=random.randrange(9, 19, 1))
    url = reverse("restaurant-list")
    response = user.get(url, format="json")

    assert response.status_code == 200
    assert len(response.data) == Restaurant.objects.all().count()

    # retrieve
    restaurant = baker.make(Restaurant)
    url = reverse("restaurant-detail", [restaurant.id])
    response = user.get(url, format="json")

    assert response.status_code == 200
    assert response.data['id'] == restaurant.id


def test_restaurant_create(user):
    body = {
        "name": "TestFood",
        "address": "Test st., 404",
    }
    url = reverse("restaurant-list")
    response = user.post(url, body, format="json")

    assert response.status_code == 201
    assert response.data['name'] == "TestFood"
    assert response.data['address'] == "Test st., 404"
    assert response.data['created_by'] == User.objects.get(username='test').id


def test_menu_create(user):
    restaurant = baker.make(Restaurant)
    body = {
        "date": date.today(),
        "dishes": "1.afg\n2.akdsjf\n3.fd",
        "restaurant": restaurant.id
    }
    url = reverse("menu-list")
    response = user.post(url, body)

    assert response.status_code == 201
    assert response.data['date'] == str(date.today())
    assert response.data['dishes'] == "1.afg\n2.akdsjf\n3.fd"
    assert response.data['restaurant'] == restaurant.id


def test_today_menu(user):
    menus = baker.make(Menu, date='2022-02-22', _quantity=random.randrange(9, 19, 1))
    menus = baker.make(Menu, date=date.today(), _quantity=random.randrange(9, 19, 1))
    max_votes = 0
    winners = []
    for menu in menus:
        votes = baker.make(Vote, menu=menu, _quantity=random.randrange(9, 19, 1))
        if len(votes) > max_votes:
            max_votes = len(votes)
            winners = [menu]
        elif len(votes) == max_votes:
            winners.append(menu)

    url = reverse("today-menu")
    response = user.get(url, format="json")

    assert response.data in MenuSerializer(winners, many=True).data


def test_today_results(user):
    menus = baker.make(Menu, date='2022-02-22', _quantity=random.randrange(9, 19, 1))
    menus = baker.make(Menu, date=date.today(), _quantity=random.randrange(9, 19, 1))
    data = []
    for menu in menus:
        votes = baker.make(Vote, menu=menu, _quantity=random.randrange(9, 19, 1))
        data_element = {"id": menu.id, "result": len(votes)}
        data.append(data_element)

    url = reverse("today-results")
    response = user.get(url)

    for element in response.data:
        data_element = {"id": element['id'], "result": element['result']}
        assert data_element in data
    assert len(response.data) == len(data)


def test_aninimous_user_no_access(client):
    url = reverse("today-results")
    response = client.get(url)

    assert response.status_code == 401

    url = reverse("today-menu")
    response = client.get(url)

    assert response.status_code == 401

    url = reverse("menu-list")
    response = client.get(url)

    assert response.status_code == 401

    url = reverse("restaurant-list")
    response = client.get(url)

    assert response.status_code == 401

    url = reverse("vote-list")
    response = client.get(url)

    assert response.status_code == 401
