import csv
import datetime

# function to check if a date is in the weekend
def is_weekend(date_str):
    # Convert the date string to a datetime object
    date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    
    # Check if the weekday is either Saturday (5) or Sunday (6)
    if date.weekday() == 5:
        return 'Saturday'
    elif date.weekday() == 6:
        return 'Sunday'
    else:
        return 'Nope'
    
# Read in CSV file exported from Clockify and calc total hours and pay including extra bonus on weekends
def calcPay(name):
    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        total_hours = 0
        billable_amount = 0
        billable_amount_extra = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            if row['User'].lower().strip() == name.lower().strip():
                print(f'Name: {row["User"]}, Email: {row["Email"]}, Date: {row["End Date"]} Duration (h): {row["Duration (h)"]}, Duration (decimal): {row["Duration (decimal)"]}, Billable Rate (USD): {row["Billable Rate (USD)"]}, Billable Amount (USD): {row["Billable Amount (USD)"]}')
                
                todays_billable = float(row["Billable Amount (USD)"])
                is_weekend_date = is_weekend(row["End Date"])
                # add 150% on saturdays
                if is_weekend_date == 'Saturday':
                    todays_billable = todays_billable + (todays_billable / 2)

                # add 200% on sundays
                if is_weekend_date == 'Sunday':
                    todays_billable = todays_billable * 2

                total_hours += float(row["Duration (decimal)"])
                billable_amount += float(row["Billable Amount (USD)"])
                billable_amount_extra += todays_billable

            line_count += 1

        total_hours = round(total_hours, 2)
        billable_amount = round(billable_amount, 2)
        billable_amount_extra = round(billable_amount_extra, 2)

        print(f'Processed {line_count} lines.')
        print("=====================================")
        print("total hours:", total_hours)
        print("billable amount (USD):", billable_amount)
        print("billable amount extra (USD):", billable_amount_extra)
        print("=====================================")

# call function
input_name = input("Please enter the name of the employee. (Make sure to use name in Clockify) \n")
calcPay(input_name)
print("If the amount is 0 then please verify if u have entered the name correctly")