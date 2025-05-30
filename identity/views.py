from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from django.db.models import Q

@api_view(['POST'])
def identify(request):
    email = request.data.get('email')
    phone = request.data.get('phoneNumber')

    if not email and not phone:
        return Response({"error": "Either email or phoneNumber must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    matched_contacts = Contact.objects.filter(
        Q(email=email) | Q(phone_number=phone)
    ).order_by('created_at')

    if not matched_contacts.exists():
        new_contact = Contact(email=email, phone_number=phone)
        new_contact.save()
        return Response({
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phoneNumbers": [new_contact.phone_number] if new_contact.phone_number else [],
                "secondaryContactIds": []
            }
        })

    primary_contact = None
    for contact in matched_contacts:
        if contact.link_precedence == "primary":
            if primary_contact is None or contact.created_at < primary_contact.created_at:
                primary_contact = contact

    secondary_ids = []
    for contact in matched_contacts:
        if contact.id != primary_contact.id:
            contact.link_precedence = "secondary"
            contact.linked_id = primary_contact.id
            contact.save()
            secondary_ids.append(contact.id)

    existing_emails = set(c.email for c in matched_contacts if c.email)
    existing_phones = set(c.phone_number for c in matched_contacts if c.phone_number)

    if (email and email not in existing_emails) or (phone and phone not in existing_phones):
        new_contact = Contact(
            email=email,
            phone_number=phone,
            linked_id=primary_contact.id,
            link_precedence='secondary'
        )
        new_contact.save()
        secondary_ids.append(new_contact.id)

    final_contacts = Contact.objects.filter(Q(id=primary_contact.id) | Q(linked_id=primary_contact.id))
    all_emails = list({c.email for c in final_contacts if c.email})
    all_phones = list({c.phone_number for c in final_contacts if c.phone_number})
    all_secondary_ids = [c.id for c in final_contacts if c.link_precedence == 'secondary']

    response_data = {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": all_emails,
            "phoneNumbers": all_phones,
            "secondaryContactIds": all_secondary_ids
        }
    }

    return Response(response_data)
