#!/usr/bin/env bash
SERVICE="mysqld"
landlord_id="Landlord.98fcba4d-b554-4fdb-b5b6-5ea9d692726f"
house_id="House.3273e2f0-7d23-4037-b192-ff0ad52d096c"
aptmt1_id="Apartment.296fc502-0ed6-4cdc-95a6-1efffb097f4a"
aptmt2_id="Apartment.7dec7ce6-7906-4657-aaca-04597e19dfb5"

if pgrep -x "$SERVICE" >/dev/null
then
	echo "Mysql is running!"
else
	echo "Mysql isn't running. Starting...."
	sudo service mysql start
fi

echo "create Landlord first_name='Nyumba' last_name='Zangu' email='nyumba@zangu.com' password='Umelipa?' id=$landlord_id" | ./console.py
echo "create House house_name='Nyumba Kubwa' landlord_id=$landlord_id id=$house_id" | ./console.py
echo "create Apartment apartment_no='D001'  room_type='Two Bedroom' rent='32000' house_id=$house_id id=$aptmt1_id" | ./console.py
echo "update House id=$house_id number_of_apartments=1" | ./console.py
echo "create Apartment apartment_no='D002' room_type='Single Room' rent='8000' house_id=$house_id id=$aptmt2_id" | ./console.py
echo "update House id=$house_id number_of_apartments=2" | ./console.py
echo "create Tenant first_name='Mpiga' last_name='Kelele' apartment_id=$aptmt1_id landlord_id=$landlord_id tenant_id='MPKE0001' password='mpigakelele'"| ./console.py
echo "create Tenant first_name='Mkosa' last_name='Kulipa' apartment_id=$aptmt2_id landlord_id=$landlord_id tenant_id='MKKU0002' password='mkosakulipa'"| ./console.py

