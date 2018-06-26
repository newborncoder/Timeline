#This is an Interview Assignment.

Timeline is a backend application used to provide a timeline of additions and changes that are done by a user/retailer while adding,editing or removing the items from his list.

The application.py file contains all the code needed for implementing the design. Config.cfg file is a configuration file which contains dummy code. Change this file for connecting to a mysql database. 

The application  has been tested using an online free mysql hosting.

Problem Statement
================================
Input : Two dates with/without user id.
Output : List of statements like: 

"UserX edited Product's Selling Price"
"UserX deleted ProductZ"

==================================


Solution :

User
ID	UserName
1	ChocoShop
2	JoyShop


Item

ID	Item Name	Brand	Category	Date Created	Date Modified
1	Yamaha R1	Yamaha	Automobiles	10-10-2016	10-10-2016
2	Pulsar 220	Pulsar	Automobiles	10-11-2018	10-11-2018

Variant

ID	Name
1	TopSpeed
2	Color
3	Cost Price
4	Selling Price

User_Item
user_id	item_id
1	1
1	2
1	3
2	11331
2	11332

Item_Variants
Item_id	variant_id	Value
1	1	300 kmph
1	2	Red, Blue, Black
11331	3	100
1131	4	250

AutoLog
user_id	action	item_id	variant_id	date_created
1	edited	11331	3	11-11-2016
1	edited	11331	4	11-11-2016
2	created	1221	4	12-02-2018
2	deleted	1221	4	12-02-2018


Possible solutions :

Item {
Item::Created:1
Item::NameEdited: 2
Item::BrandEdited: 3
Item::CategoryEdited: 4
Item::Deleted: 5
VariantAdded:6
VariantEdited:7
VariantDeleted:8
}








