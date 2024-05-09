from corporate_assets.views import *
from django.urls import path


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('user_login/', user_login, name='user_login'),
    path('company_assets_list/', company_assets_list, name='company_assets_list'),
    path('get_company_ID/',get_company_ID, name='get_company_ID'),
    path('add_asset/', add_asset, name='add_asset'),
    path('asset/<int:asset_id>/', retrieve_asset, name='retrieve-asset'),
    path('asset/<int:asset_id>/update/', update_asset, name='update-asset'),
    path('asset/<int:asset_id>/delete/', delete_asset, name='delete-asset'),
]