from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from polls.models import Restaurant, Menu, Vote
from polls.serializers import (RestaurantSerializer,
                               MenuSerializer,
                               MenuResultSerializer,
                               VoteSerializer)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.order_by('id')
    serializer_class = RestaurantSerializer


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.order_by('date')
    serializer_class = MenuSerializer


class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.order_by('menu')
    serializer_class = VoteSerializer

    @action(detail=False, methods=['GET'])
    def today_menu(self, request):
        menus = Menu.objects.today_results()
        max_votes = -1
        winner = None
        for menu in menus:
            votes = menu.result
            if votes > max_votes:
                max_votes = votes
                winner = menu

        data = MenuSerializer(winner).data
        response = Response(data)
        return response

    @action(detail=False, methods=['GET'])
    def today_results(self, request):
        data = Menu.objects.today_results()
        data = MenuResultSerializer(data, many=True).data
        response = Response(data)
        return response
