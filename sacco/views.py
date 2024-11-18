from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from sacco.app_forms import CustomerForm
from sacco.models import Customer, Deposit


# Create your views here.
def test(request):
    #save a customer
    # c1 = Customer(first_name='Saida', last_name='Ali', email='saida@x.com', dob='2000-11-28', gender='Female', weight=62)
    # c1.save()
    #
    # c2 = Customer(first_name='Jake', last_name='Juma', email='juma@x.com', dob='1999-11-28', gender='Male', weight=62)
    # c2.save()


    customer_count = Customer.objects.count()

    #fetching one customer
    c1 = Customer.objects.get(id=1) # select * from customers where id=1
    print(c1)
    d1 = Deposit(amount=1000, status=True, customer=c1)
    d1.save()
    d2 = Deposit(amount=2000, status=False, customer=c1)
    d2.save()

    deposit_count = Deposit.objects.count()

    return HttpResponse(f"Ok, Done, we have {customer_count} customers and {deposit_count} deposits")


def customers(request):
    data = Customer.objects.all().order_by('id').values() # ORM select * from customers / when you want to fetch data
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, "customers.html", {"data": paginated_data})


def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id) #select * from customers where id=7
    customer.delete() #delete from customers where id=7
    return redirect('customers')


def deposits(request):
    data = Deposit.objects.all()
    return render(request, "deposits.html", {"deposits": data})


def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {"form": form})

# packages for making the forms appear nicely
# pip install django-crispy-forms
# pip install crispy-bootstrap5


def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = Deposit.objects.filter(customer_id=customer_id)
    return render(request, "details.html", {"deposits": deposits, "customer": customer})