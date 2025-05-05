from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    TenantCreateView, TenantDetailView, TenantUpdateView, TenantDeleteView,
    LandlordCreateView, LandlordDetailView, LandlordUpdateView, LandlordDeleteView, LandlordListView,LandlordListAuthView,
    EmployeeCreateView, EmployeeCreateTokenView, EmployeeDetailView, EmployeeUpdateView, EmployeeDeleteView, EmployeeListView,
    AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView,
    LoginView, LandlordCreateByEmployeeView, LandlordDetailByEmployeeView, LandlordListByEmployeeView,LandlordUpdateByEmployeeView,LandlordDeleteByEmployeeView,TenantCreateByEmployeeView, TenantDetailByEmployeeView, TenantListByEmployeeView,TenantUpdateByEmployeeView,TenantDeleteByEmployeeView,
    AgentCreateByEmployeeView, AgentDetailByEmployeeView, AgentListByEmployeeView, AgentUpdateByEmployeeView, AgentDeleteByEmployeeView,
    BuildingCreateByEmployeeView, BuildingDetailByEmployeeView, BuildingListByEmployeeView, BuildingUpdateByEmployeeView, BuildingDeleteByEmployeeView,
    
    #booking by employee
    BookingCreateByEmployeeView, BookingDetailByEmployeeView, BookingListByEmployeeView, BookingUpdateByEmployeeView, BookingDeleteByEmployeeView,

    #review create without authentication
    ReviewCreateView,ReviewListPublicView,
    #review by employee
    ReviewCreateByEmployeeView, ReviewDetailByEmployeeView, ReviewListByEmployeeView, ReviewUpdateByEmployeeView, ReviewDeleteByEmployeeView,

    #booking by landlord
    BookingCreateByLandlordView, BookingDetailByLandlordView, BookingListByLandlordView, BookingUpdateByLandlordView, BookingDeleteByLandlordView,

    #booking by agent
    BookingCreateByAgentView, BookingDetailByAgentView, BookingListByAgentView, BookingUpdateByAgentView, BookingDeleteByAgentView,

    #booking by tenant
    BookingCreateByTenantView, BookingDetailByTenantView, BookingListByTenantView, BookingUpdateByTenantView, BookingDeleteByTenantView,

    #payment by employee
    PaymentCreateByEmployeeView, PaymentDetailByEmployeeView, PaymentListByEmployeeView, PaymentUpdateByEmployeeView, PaymentDeleteByEmployeeView,

    #building by landlord
    BuildingCreateByLandlordView, BuildingDetailByLandlordView, BuildingListByLandlordView, BuildingUpdateByLandlordView, BuildingDeleteByLandlordView,

    #building without authentication
    BuildingListView,

    #enquiry by employee
    EnquiryCreateByEmployeeView, EnquiryDetailByEmployeeView, EnquiryListByEmployeeView, EnquiryUpdateByEmployeeView, EnquiryDeleteByEmployeeView,

    #enquiry without authentication
    EnquiryCreateView,
    BookingCreateView,BookingListView,BuildingFilteredListView
)

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),

    # Building Filtered List
    path('building/filtered-list/', BuildingFilteredListView.as_view(), name='building-filtered-list'),

    #review create without authentication
    path('review/create/', ReviewCreateView.as_view(), name='review-create'),
    path('review/list/', ReviewListPublicView.as_view(), name='review-list-public'),
    # Employee URLs
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/create-token/', EmployeeCreateTokenView.as_view(), name='employee-create-token'),
    path('employee/list/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/<int:id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/update/<int:id>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:id>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    #Landlord crud by employee
    path('landlord/create-by-employee/', LandlordCreateByEmployeeView.as_view(), name='landlord-create-by-employee'),
    path('landlord_list-employee/<int:id>/', LandlordDetailByEmployeeView.as_view(), name='landlord-view-by-employee'),
    path('landlords/list-by-employee/', LandlordListByEmployeeView.as_view(), name='landlord-list-by-employee'),
    path('landlords/update-by-employee/<int:id>/', LandlordUpdateByEmployeeView.as_view(), name='landlord-update-by-employee'),
    path('landlords/delete-by-employee/<int:id>/', LandlordDeleteByEmployeeView.as_view(), name='landlord-delete-by-employee'),
    
    #Tenant crud by employee
    path('tenant/create-by-employee/', TenantCreateByEmployeeView.as_view(), name='tenant-create-by-employee'),
    path('tenant/list-by-employee/', TenantListByEmployeeView.as_view(), name='tenant-list-by-employee'),
    path('tenant/view-by-employee/<int:id>/', TenantDetailByEmployeeView.as_view(), name='tenant-view-by-employee'),
    path('tenant/update-by-employee/<int:id>/', TenantUpdateByEmployeeView.as_view(), name='tenant-update-by-employee'),
    path('tenant/delete-by-employee/<int:id>/', TenantDeleteByEmployeeView.as_view(), name='tenant-delete-by-employee'),
    
    #Agent crud by employee
    path('agent/create-by-employee/', AgentCreateByEmployeeView.as_view(), name='agent-create-by-employee'),
    path('agent/list-by-employee/', AgentListByEmployeeView.as_view(), name='agent-list-by-employee'),
    path('agent/view-by-employee/<int:id>/', AgentDetailByEmployeeView.as_view(), name='agent-view-by-employee'),
    path('agent/update-by-employee/<int:id>/', AgentUpdateByEmployeeView.as_view(), name='agent-update-by-employee'),
    path('agent/delete-by-employee/<int:id>/', AgentDeleteByEmployeeView.as_view(), name='agent-delete-by-employee'),

    # Building crud by employee
    path('building/create-by-employee/', BuildingCreateByEmployeeView.as_view(), name='building-create-by-employee'),
    path('building/list-by-employee/', BuildingListByEmployeeView.as_view(), name='building-list-by-employee'),
    path('building/view-by-employee/<int:id>/', BuildingDetailByEmployeeView.as_view(), name='building-view-by-employee'),
    path('building/update-by-employee/<int:id>/', BuildingUpdateByEmployeeView.as_view(), name='building-update-by-employee'),
    path('building/delete-by-employee/<int:id>/', BuildingDeleteByEmployeeView.as_view(), name='building-delete-by-employee'),

    # Booking crud by employee
    path('booking/create-by-employee/', BookingCreateByEmployeeView.as_view(), name='booking-create-by-employee'),
    path('booking/list-by-employee/', BookingListByEmployeeView.as_view(), name='booking-list-by-employee'),
    path('booking/view-by-employee/<int:id>/', BookingDetailByEmployeeView.as_view(), name='booking-view-by-employee'),
    path('booking/update-by-employee/<int:id>/', BookingUpdateByEmployeeView.as_view(), name='booking-update-by-employee'),
    path('booking/delete-by-employee/<int:id>/', BookingDeleteByEmployeeView.as_view(), name='booking-delete-by-employee'),

    # Payment crud by employee
    path('payment/create-by-employee/', PaymentCreateByEmployeeView.as_view(), name='payment-create-by-employee'),
    path('payment/list-by-employee/', PaymentListByEmployeeView.as_view(), name='payment-list-by-employee'),
    path('payment/view-by-employee/<int:id>/', PaymentDetailByEmployeeView.as_view(), name='payment-view-by-employee'),
    path('payment/update-by-employee/<int:id>/', PaymentUpdateByEmployeeView.as_view(), name='payment-update-by-employee'),
    path('payment/delete-by-employee/<int:id>/', PaymentDeleteByEmployeeView.as_view(), name='payment-delete-by-employee'),

    # Review crud by employee
    path('review/create-by-employee/', ReviewCreateByEmployeeView.as_view(), name='review-create-by-employee'),
    path('review/list-by-employee/', ReviewListByEmployeeView.as_view(), name='review-list-by-employee'),
    path('review/view-by-employee/<int:id>/', ReviewDetailByEmployeeView.as_view(), name='review-view-by-employee'),
    path('review/update-by-employee/<int:id>/', ReviewUpdateByEmployeeView.as_view(), name='review-update-by-employee'),
    path('review/delete-by-employee/<int:id>/', ReviewDeleteByEmployeeView.as_view(), name='review-delete-by-employee'),

    # Booking crud by landlord
    path('booking/create-by-landlord/', BookingCreateByLandlordView.as_view(), name='booking-create-by-landlord'),
    path('booking/list-by-landlord/', BookingListByLandlordView.as_view(), name='booking-list-by-landlord'),
    path('booking/view-by-landlord/<int:id>/', BookingDetailByLandlordView.as_view(), name='booking-view-by-landlord'),
    path('booking/update-by-landlord/<int:id>/', BookingUpdateByLandlordView.as_view(), name='booking-update-by-landlord'),
    path('booking/delete-by-landlord/<int:id>/', BookingDeleteByLandlordView.as_view(), name='booking-delete-by-landlord'),

    #building crud by landlord
    path('building/create-by-landlord/', BuildingCreateByLandlordView.as_view(), name='building-create-by-landlord'),
    path('building/list-by-landlord/', BuildingListByLandlordView.as_view(), name='building-list-by-landlord'),
    path('building/view-by-landlord/<int:id>/', BuildingDetailByLandlordView.as_view(), name='building-view-by-landlord'),
    path('building/update-by-landlord/<int:id>/', BuildingUpdateByLandlordView.as_view(), name='building-update-by-landlord'),
    path('building/delete-by-landlord/<int:id>/', BuildingDeleteByLandlordView.as_view(), name='building-delete-by-landlord'),

    #enquiry crud by employee
    path('enquiry/create-by-employee/', EnquiryCreateByEmployeeView.as_view(), name='enquiry-create-by-employee'),
    path('enquiry/list-by-employee/', EnquiryListByEmployeeView.as_view(), name='enquiry-list-by-employee'),
    path('enquiry/view-by-employee/<int:id>/', EnquiryDetailByEmployeeView.as_view(), name='enquiry-view-by-employee'),
    path('enquiry/update-by-employee/<int:id>/', EnquiryUpdateByEmployeeView.as_view(), name='enquiry-update-by-employee'),
    path('enquiry/delete-by-employee/<int:id>/', EnquiryDeleteByEmployeeView.as_view(), name='enquiry-delete-by-employee'),


    # Booking crud by agent
    path('booking/create-by-agent/', BookingCreateByAgentView.as_view(), name='booking-create-by-agent'),
    path('booking/list-by-agent/', BookingListByAgentView.as_view(), name='booking-list-by-agent'),
    path('booking/view-by-agent/<int:id>/', BookingDetailByAgentView.as_view(), name='booking-view-by-agent'),
    path('booking/update-by-agent/<int:id>/', BookingUpdateByAgentView.as_view(), name='booking-update-by-agent'),
    path('booking/delete-by-agent/<int:id>/', BookingDeleteByAgentView.as_view(), name='booking-delete-by-agent'),

    # Booking crud by tenant
    path('booking/create-by-tenant/', BookingCreateByTenantView.as_view(), name='booking-create-by-tenant'),
    path('booking/list-by-tenant/', BookingListByTenantView.as_view(), name='booking-list-by-tenant'),
    path('booking/view-by-tenant/<int:id>/', BookingDetailByTenantView.as_view(), name='booking-view-by-tenant'),
    path('booking/update-by-tenant/<int:id>/', BookingUpdateByTenantView.as_view(), name='booking-update-by-tenant'),
    path('booking/delete-by-tenant/<int:id>/', BookingDeleteByTenantView.as_view(), name='booking-delete-by-tenant'),

    # Tenant URLs
    path('tenant/create/', TenantCreateView.as_view(), name='tenant-create'),
    path('tenant/<int:id>/', TenantDetailView.as_view(), name='tenant-detail'),
    path('tenant/<int:id>/update/', TenantUpdateView.as_view(), name='tenant-update'),
    path('tenant/<int:id>/delete/', TenantDeleteView.as_view(), name='tenant-delete'),

    # Landlord URLs
    path('landlord/create/', LandlordCreateView.as_view(), name='landlord-create'),
    path('landlords/', LandlordListView.as_view(), name='landlord-list'),
    path('landlords/auth/', LandlordListAuthView.as_view(), name='landlord-list-auth'), #for authentication
    path('landlord/<int:id>/', LandlordDetailView.as_view(), name='landlord-detail'),
    path('landlord/<int:id>/update/', LandlordUpdateView.as_view(), name='landlord-update'),
    path('landlord/<int:id>/delete/', LandlordDeleteView.as_view(), name='landlord-delete'),

    # Agent URLs
    path('agent/create/', AgentCreateView.as_view(), name='agent-create'),
    path('agent/<int:id>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agent/<int:id>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('agent/<int:id>/delete/', AgentDeleteView.as_view(), name='agent-delete'),

    #get building list without authentication
    path('building/list/', BuildingListView.as_view(), name='building-list'),
    path('booking/list/', BookingListView.as_view(), name='booking-list'),
    path('booking/create/', BookingCreateView.as_view(), name='booking-create'),
    
    #enquiry without authentication
    path('enquiry/create/', EnquiryCreateView.as_view(), name='enquiry-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

