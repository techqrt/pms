from django.urls import path
from pms_apps.property.controller import PropertyViewController

urlpatterns = [

    path("create/", PropertyViewController.create, name="create_property"),
    path("update/", PropertyViewController.update, name="update_property"),
    path("delete/", PropertyViewController.delete, name="delete_property"),
    path("delete_many/", PropertyViewController.delete_many, name="delete_many_properties"),
    path("get/", PropertyViewController.get, name="get_property"),
    path("get_all/", PropertyViewController.get_all, name="get_all_properties"),
    path("count/", PropertyViewController.count, name="count_properties"),
    path("assign/", PropertyViewController.assign, name="assign_property"),
    path("assignment/get/", PropertyViewController.get_assignment, name="get_assignment"),
    path("assignment/get_all/", PropertyViewController.get_all_assignments, name="get_all_assignments"),
]
