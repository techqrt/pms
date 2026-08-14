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
    path("occupancy/summary/", PropertyViewController.occupancy_summary, name="property_occupancy_summary"),
    path("occupancy/get_all/", PropertyViewController.occupancy_list, name="property_occupancy_list"),
    path("rental-report/summary/", PropertyViewController.rental_report_summary, name="property_rental_report_summary"),
    path("rental-report/get_all/", PropertyViewController.rental_report_list, name="property_rental_report_list"),
    path("assign/", PropertyViewController.assign, name="assign_property"),
    path("assignment/update/", PropertyViewController.update_assignment, name="update_assignment"),
    path("assignment/get/", PropertyViewController.get_assignment, name="get_assignment"),
    path("assignment/get_all/", PropertyViewController.get_all_assignments, name="get_all_assignments"),
    path("assignment/count/", PropertyViewController.assignment_count, name="assignment_count"),
]
