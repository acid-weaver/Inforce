from django.urls import path

from polls.views import (RestaurantViewSet,
                         MenuViewSet,
                         VoteViewSet)


restaurant_list = RestaurantViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

restaurant_detail = RestaurantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

menu_list = MenuViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

menu_detail = MenuViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

vote_list = VoteViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

vote_detail = VoteViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

today_menu = VoteViewSet.as_view({
    'get': 'today_menu',
})

today_results = VoteViewSet.as_view({
    'get': 'today_results',
})


urlpatterns = [
    path('restaurants/', restaurant_list, name='restaurant-list'),
    path('restaurants/<int:pk>/', restaurant_detail, name='restaurant-detail'),

    path('menus/', menu_list, name='menu-list'),
    path('menus/<int:pk>/', menu_detail, name='menu-detail'),

    path('votes/', vote_list, name='vote-list'),
    path('votes/<int:pk>/', vote_detail, name='vote-detail'),

    path('today_menu/', today_menu, name='today-menu'),
    path('results', today_results, name='today-results')
]
