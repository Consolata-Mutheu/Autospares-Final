from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logoutUser"),    
    
    path('home/', views.home, name="home"),
    path('employees/', views.employees, name="employees"),
    path('users/', views.users, name="users"),
    path('add-employee/', views.addEmployee, name="add-employee"),
    
    path('edit-user/', views.editUser, name="edit-user"),
    path('update-user/', views.updateUser, name="update-user"),
    
    path('user-profile/', views.userProfile, name="user-profile"),
    path('delete-item/<str:pk>/', views.deleteItem, name="delete-item"),
    path('delete-user/<str:pk>/', views.delete_user, name="delete-user"),

    #customers
    path('customers/', views.customers, name="customers"),
    path('create-customer/', views.createCustomer, name="create-customer"),
    path('edit-customer/<str:pk>/', views.editCustomer, name="edit_customer"),
    path('update-customer/<str:pk>/', views.updateCustomer, name="update_customer"),
   # path('delete-item/<str:pk>/', views.deleteItem, name="delete-item"),
    path('delete-customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),

    #inventory
    path('inventory/', views.inventory, name="inventory"),
    path('add-inventory/', views.addInventory, name="add-inventory"),
    path('edit-inventory/<str:pk>/', views.editInventory, name="edit_inventory"),

    path('delete-item/<str:pk>/', views.deleteItem, name="delete_item"),

    #Supplier
    path('suppliers/', views.suppliers, name="suppliers"),
    path('add-suppliers/', views.addSupplier, name="add-suppliers"),
    path('edit-supplier/<str:pk>/', views.editSupplier, name="edit_supplier"),
    path('delete-supplier/<str:pk>/', views.deleteSupplier, name="delete_supplier"),

    #category
    path('categories/', views.categories, name="categories"),
    path('add-categories/', views.addCategory, name="add-category"),
    path('edit-category/<str:pk>/', views.editCategory, name="edit_category"),
    path('delete-category/<str:pk>/', views.deleteCategory, name="delete_category"),

    path('orders/', views.orders, name="orders"),
    path('create-order/', views.create_order, name="create-order"),
    path('get-product-price/<int:product_id>/', views.get_product_price, name='get_product_price'),
    path('edit-order/<str:pk>/', views.editOrder, name="edit_order"),
    path('delete-order/<str:pk>/', views.delete_order, name="delete_order"),

    path('sales-report/', views.salesReport, name="sales_report"),






]
