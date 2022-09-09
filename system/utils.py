EntityChoice = (
    ("1", "Person"),
    ("2", "Company"),
)

ShippingTermsChoice = (
    ("1", "Prepaid/Prepay"),
    ("2", "Add/Collect"),
)

AddressTypeChoice=(
("1","Customer"),
("2","Billing"),
("3", "Shipping"),
)

LocationChoice=(
    ("1","Residential"),
    ("2","Commercial"),
    ("3","Construction Site")
)

ColumnTypeChoice=(
    ("1","string"),
    ("2","int"),
    ("3","boolean"),
    ("4","lookup"),
    ("5","date"),
    ("6", "datetime"),
    ("7", "multi-choice"),   
)

StatusChoice=(
    ("1","Closed"),
    ("2","Normal"),
    ("3","Warning"),
    ("3","Urgent"),
)

ChannelTypeChoice=(
    ("1","Home"),
    ("2","Work"),
    ("3", "Personal")
)

DateFormatChoices=(
    
    ("1", "MM/DD/YY"),
    ("2", "DD/MM/YY"),
    ("3", "YY/MM/DD"),
    ("4", "MM-DD-YYYY"),
    ("5", "DD-MM-YYYY"),
    ("6", "YYYY-MM-DD"),
)

TimeFormatChoice =(
    
    ("1","HH:MM:SS"),
    ("2","HH:MM:SS XM"),
    ("3","HH:MM"),
    ("4","HH:MM XM")
    
)
