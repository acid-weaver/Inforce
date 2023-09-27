import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(client):
    user = User.objects.create_user('test', '12345test',
                                    first_name='Name',
                                    last_name='Surname')
    token = Token.objects.get_or_create(user=user)
    client.login(username='test', password='12345test')
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token[0]))
    return client


@pytest.fixture
def admin(client):
    user = User.objects.create_superuser('test_admin', '12345test',
                                         first_name='Name',
                                         last_name='Surname')
    token = Token.objects.get_or_create(user=user)
    client.login(username='test_admin', password='12345test')
    client.credentials(HTTP_AUTHORIZATION='Token ' + str(token[0]))
    return client
