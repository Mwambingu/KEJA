#!/bin/env bash
SERVICE="mysqld"

if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is running..."
else
    echo "$SERVICE is stopped."
fi

landlord_id="Landlord1111-1111-1111-1111"
tenant_id="Tenant1111-1111-1111-1111"
apt_id="Apartment1111-1111-1111-1111"
house_id="House1111-1111-1111-1111"

echo "create Landlord id=$landlord_id first_name=ligma last_name=balls email=ligma@balls.com password=ligmaligma" | python3 console.py
echo "create House id=$house_id 'house_name=Ligma Housing' landlord_id=$landlord_id" | python3 console.py
echo "create Apartment id=$apt_id apt_no=D1 room_type=single rent=6000 house_id=$house_id" | python3 console.py
echo "create Tenant id=$tenant_id first_name=Karnt last_name=Pei tenant_id=KAPE001 password=wontpei apt_id=$apt_id landlord_id=$landlord_id" | python3 console.py