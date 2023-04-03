from django.urls import path

from . import views

urlpatterns = [
    path(
        "image",
        views.gallery_add_get_delete_image_view,
        name="gallery-add-get-delete-image",
    ),
    path(
        "",
        views.gallery_get_list_images_view,
        name="gallery-get-list-images",
    ),
    path(
        "delete",
        views.gallery_delete_all_images_view,
        name="gallery-delete-all-images",
    ),
]
