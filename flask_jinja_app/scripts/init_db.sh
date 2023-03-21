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

landlord_id2="Landlord2222-2222-2222-2222"
tenant_id2="Tenant2222-2222-2222-2222"
apt_id2="Apartment2222-2222-2222-2222"
house_id2="House2222-2222-2222-2222"

echo "create Landlord id=$landlord_id2 first_name=Mapropati last_name=Mapropati email=propati@mapropati.com password=mapropati22" | python3 console.py
echo "create House id=$house_id2 'house_name=Mapropatis' landlord_id=$landlord_id2" | python3 console.py
echo "create Apartment id=$apt_id2 apt_no=D1 room_type=single rent=6000 house_id=$house_id2" | python3 console.py
echo "create Tenant id=$tenant_id2 first_name=Richie last_name=Manny tenant_id=RIMA001 password=richman apt_id=$apt_id2 landlord_id=$landlord_id2" | python3 console.py

landlord_id3="Landlord3333-3333-3333-3333"
tenant_id3="Tenant3333-3333-3333-3333"
apt_id3="Apartment3333-3333-3333-3333"
house_id3="House3333-3333-3333-3333"

echo "create Landlord id=$landlord_id3 first_name=Houwser last_name=Clouser email=clouser@howser.com password=howsclous22" | python3 console.py
echo "create House id=$house_id3 'house_name=Mapropatis' landlord_id=$landlord_id3" | python3 console.py
echo "create Apartment id=$apt_id3 apt_no=D1 room_type=single rent=6000 house_id=$house_id3" | python3 console.py
echo "create Tenant id=$tenant_id3 first_name=Lett last_name=Peya tenant_id=LEPA001 password=letpeying apt_id=$apt_id3 landlord_id=$landlord_id3" | python3 console.py