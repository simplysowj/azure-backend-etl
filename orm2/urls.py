from django.urls import path
from .views import UploadBusinessExcel, BusinessStatistics,business_list_create, business_update_delete, Profit, USA, BusinessCreateView,Revenue,StartScript, StopScript,TopBusinessesByRevenue,BusinessAnalytics,TopCountriesByRevenue,ProfitByCountry

urlpatterns = [
    #path('upload/', UploadBusinessExcel.as_view(), name='upload_business_excel'),
    path('business/', business_list_create, name='business-list-create'),
    path('business/<int:pk>/', business_update_delete, name='business-update-delete'),
    path('start-script/', StartScript.as_view(), name='start_script'),
    path('stop-script/', StopScript.as_view(), name='stop_script'),
    path('forminsert/', BusinessCreateView.as_view(), name='business-create'),
    path('analytics/', BusinessAnalytics.as_view(), name='business_analytics'),
    path('business/stats/', BusinessStatistics.as_view(), name='business_stats'),
    path('data/', Profit.as_view(), name='api_data'),
    path('usa/', USA.as_view(), name='api_usa'),
    path('revenue/', Revenue.as_view(), name='api_revenue'),
    path('upload-excel/', UploadBusinessExcel.as_view(), name='upload-excel'),
    path('topbyrevenue/', TopCountriesByRevenue.as_view(), name='topbyrevenue'),
    path('profitbycountry/', ProfitByCountry.as_view(), name='profitbycountry'),
    path('top_businesses_by_revenue/', TopBusinessesByRevenue.as_view(), name='top_businesses_by_revenue'),

]
