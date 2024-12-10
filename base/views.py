from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# from .models import User, Employee, Department, Category, Supplier, Inventory, Customer
from .models import *
# from .forms import EmployeeForm, UserForm, MyUserCreationForm, InventoryForm,SupplierForm,CategoryForm, CustomerForm
from .forms import *


# Create your views here.

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect email or password.')

    context = {}
    return render(request, 'base/auth/login.html', context)

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def employees(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'base/employees.html', context)

@login_required(login_url='login')
def addEmployee(request):
    form = EmployeeForm()
    departments = Department.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(data=request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.email = employee.email.lower()
            # You can check if the data is saved successfully here
            try:
                employee.save()
                messages.success(request, 'User added successfully')
                return redirect('employees')
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form, 'departments': departments}
    return render(request, 'base/add-employee.html', context)

@login_required(login_url='login')
def registerUser(request):
    form = EmployeeForm
    if request.method == 'POST':
        form = EmployeeForm(data=request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.email = employee.email.lower()
            employee.save()
            return redirect('home')
        else:
            messages.error(request, 'An Error Occured During registration')
            
    context = {'form' : form}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def userProfile(request ):
    context = {}
    return render(request, 'base/profile.html', context)

# def users(request):
#     userForm = MyUserCreationForm()
#     users = User.objects.all()
    
#     if request.method == 'POST':
#         userForm = MyUserCreationForm(data=request.POST)
#         if userForm.is_valid():
#             user = userForm.save(commit=False)
#             user.username = user.username.lower()
#             # Modify other user fields here if needed
#             user.save()
#             messages.success(request, 'User registered successfully')
#             return redirect('users')
#         else:
#             # Include form errors in the context to display them in the template
#             context = {'users': users, 'userForm': userForm}
#             return render(request, 'base/users/index.html', context)
#          # Add a return statement here to return an HttpResponse object
#     context = {'users': users, 'userForm': userForm}
#     return render(request, 'base/users/index.html', context)
@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    userForm = MyUserCreationForm()
    if request.method == 'POST':
        userForm = MyUserCreationForm(request.POST, request.FILES)
        if userForm.is_valid():
            user = userForm.save()
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id})
        else:
            errors = userForm.errors
            return JsonResponse({'message': 'Form validation failed', 'errors': errors}, status=400)
    else:
        context = {'users': users, 'userForm': userForm}
        return render(request, 'base/users/index.html', context)

@login_required(login_url='login')
def editUser(request):
    if request.method == 'GET':
        user_id = request.GET.get('id')
        user = get_object_or_404(User, id=user_id)
        data = {'id': user.id, 'username': user.username, 'name': user.name, 'email': user.email }
        return JsonResponse(data)

@login_required(login_url='login')
def updateUser(request):
    user_id = request.POST.get('id')
    user = get_object_or_404(User, id=user_id)

    # Update employee data based on form submission
    user.name = request.POST.get('name')
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    # Update other fields similarly
    user.save()

    return JsonResponse({'message': 'User updated successfully'})

def logoutUser(request):
    logout(request)
    return redirect('login')

def deleteItem(request, pk):
    try:
        item = User.objects.get(id=pk)
    except User.DoesNotExist:
        return HttpResponse('Item not found', status=404)
    
    # Check if the current user is authorized to delete the employee
    if request.user != item.user:
        return HttpResponse('You are not allowed here!!', status=403)
    
    if request.method == 'POST':
        item.delete()
        return redirect('employees')  
    
    context = {
        'obj': item
    }
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def delete_user(request, pk):
    item = get_object_or_404(User, pk=pk)
    item.delete()
    return JsonResponse({'message': 'User deleted successfully.'})



#customers
@login_required(login_url='login')
def customers(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request,'base/customers/index.html',context)


@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            # You can check if the data is saved successfully here
            try:
                customer.save()
                messages.success(request, 'customer added successfully')
                return redirect('customers')
            except Exception as e:
                messages.error(request, f'An error occurred during creation: {str(e)}')
        else:
            messages.error(request, 'An error occurred during creation')
    context = {'form': form, 'message': 'Customer added successfully!'}
    return render(request,'base/customers/create-customer.html',context)

@login_required(login_url='login')
def editCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')  # Redirect to customer list
    else:
        form = CustomerForm(instance=customer)
        context = {'form': form}
    return render(request,'base/customers/edit_customer.html', context)

@login_required(login_url='login')
def updateCustomer(request):
    return render(request,'base/customers/edit_customer.html')


@login_required(login_url='login')
def deleteCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customers')

@login_required(login_url='login')
def inventory(request):
    items = Inventory.objects.all()
    context = {'items': items}
    return render(request,'base/inventory/index.html', context)

@login_required(login_url='login')
def addInventory(request):
    form = InventoryForm()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        form = InventoryForm(data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)

            # You can check if the data is saved successfully here
            try:
                item.save()
                messages.success(request, 'Item added successfully')
                return redirect('inventory')
            except Exception as e:
                messages.error(request, f'An error occurred during creation: {str(e)}')
        else:
            messages.error(request, 'An error occurred during creation')
    context = {'categories': categories ,'suppliers': suppliers}
    return render(request,'base/inventory/add-inventory.html', context)

#edit inventory
def editInventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Redirect to customer list
    else:
        form = InventoryForm(instance=item)
        context = {'form': form}
    return render(request, 'base/inventory/edit_inventory.html', context)

@login_required(login_url='login')
def deleteItem(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    item.delete()
    return redirect('inventory')
@login_required()

@login_required(login_url='login')
def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {'suppliers': suppliers}
    return render(request,'base/suppliers/index.html', context)

@login_required(login_url='login')
def addSupplier(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(data=request.POST)
        if form.is_valid():
            suppliers= form.save(commit=False)
            # You can check if the data is saved successfully here
            try:
                suppliers.save()
                messages.success(request, 'supplier added successfully')
                return redirect('suppliers')
            except Exception as e:
                messages.error(request, f'An error occurred during creation: {str(e)}')
        else:
            messages.error(request, 'An error occurred during creation')
    return render(request,'base/suppliers/add-supplier.html')


#Edit supplier


def editSupplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers')  # Redirect to customer list
    else:
        form = SupplierForm(instance=supplier)
        context = {'form': form}
    return render(request, 'base/suppliers/edit_supplier.html', context)

@login_required(login_url='login')
def deleteSupplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('suppliers')

@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request,'base/inventory/category.html',context)

@login_required(login_url='login')
def addCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            categories = form.save(commit=False)
            # You can check if the data is saved successfully here
            try:
                categories.save()
                messages.success(request, 'category added successfully')
                return redirect('categories')
            except Exception as e:
                messages.error(request, f'An error occurred during creation: {str(e)}')
        else:
            messages.error(request, 'An error occurred during creation')

    return render(request,'base/inventory/add-category.html')



def editCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')  # Redirect to customer list
    else:
        form = CategoryForm(instance=category)
        context = {'form': form}
    return render(request, 'base/inventory/edit_category.html', context)

@login_required(login_url='login')
def deleteCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')



@login_required(login_url='login')
def orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'base/orders/index.html',context)

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            # Check if sufficient stock is available
            if product.quantity >= quantity:
                # Deduct stock and save the order
                product.quantity -= quantity
                product.save()
                form.save()
                messages.success(request, 'Order created successfully.')
                return redirect('orders')
            else:
                messages.error(request, 'Insufficient stock for the selected product.')
    else:
        form = OrderForm()

    return render(request, 'base/orders/create_order.html', {'form': form})

def get_product_price(request, product_id):
    try:
        product = Inventory.objects.get(id=product_id)
        return JsonResponse({'price': str(product.price)})
    except Inventory.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def editOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders')  # Redirect to customer list
    else:
        form = OrderForm(instance=order)
        context = {'form': form}
    return render(request, 'base/orders/edit_order.html', context)


@login_required(login_url='login')
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        # Restore stock before deleting the order
        product = order.product
        product.quantity += order.quantity
        product.save()
        order.delete()
        messages.success(request, 'Order deleted and stock restored.')
        return redirect('orders')

    # return render(request, 'base/orders/delete_order.html', {'order': order})

    #sales report

def salesReport(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'base/reports/sales_report.html', context)






