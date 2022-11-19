from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact, PhoneNumber
from django.views.generic import ListView


# Contact list

class ContactList(ListView):
    context_object_name = "contacts"
    paginate_by = 4  # add this

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Contact.objects.filter(created_by=self.request.user)
        return Contact.objects.filter(created_by=None)


# detail contact


@login_required(login_url="/login/")
def contact_details(request, id):
    contact = Contact.objects.get(id=id)
    phones = []
    for phone in contact.phones.all():
        phones.append(phone.number)
    context = {"contact": {"email": contact.email, "phones": phones, "created_date":contact.created_at, "id": contact.id}}
    return render(request, "contact/contact_details.html", context)

# Add new contact


@login_required(login_url="/login/")
def new_contact(request):
    if request.method == "POST":
        created_by = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # phone = request.POST.get("phone")
        email = request.POST.get("email")
        index = 0
        phones = []
        while True:
            try:
                phones.append(request.POST[f"phone{index}"])
                index +=1 
            except:
                break
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            created_by=created_by
        )
        contact.save()
        for phone in phones:
            obj_phone = PhoneNumber.objects.create(number=phone)
            obj_phone.save()
            contact.phones.add(obj_phone)
        contact.save()

        return redirect("/contacts/")

    return render(request, "contact/new_contact.html")


# Update a contact
@login_required(login_url="/login/")
def update_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # phone = request.POST.get("phone")
        email = request.POST.get("email")
        contact = Contact.objects.get(pk=contact.id)
        contact.first_name=first_name
        contact.last_name=last_name
        contact.email=email

        for phk in request.POST:
            if phk not in ['csrfmiddlewaretoken', 'last_name', 'first_name', 'email']:
                PhoneNumber.objects.filter(number=phk).delete()
                if request.POST[phk] != "":
                    obj_number = PhoneNumber(number=request.POST[phk])
                    obj_number.save()
                    contact.phones.add(obj_number)
        contact.save()

        return redirect("/contacts/")

    phones = []
    for phone in contact.phones.all():
        phones.append(phone)
    context = {"contact": {"email": contact.email, "first_name":contact.first_name,
                "created_date":contact.created_at, "id": contact.id, "last_name":contact.last_name},
                "phones": phones
            }
    return render(request, "contact/update_contact.html", context)

# Remove a contact
@login_required(login_url="/login/")
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        for phone in contact.phones.all():
            phone.delete()
        contact.delete()
        return redirect("/contacts/")
    context = {"contact": contact}
    return render(request, "contact/delete_contact.html", context)
