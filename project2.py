import csv


fedtaxus = 0.05  # 5% federal tax rate in the US
czetax = 0.21    # 21% VAT (standard rate in Czech Republic)
statetax = {
    "indiana": 0.07,
    "california": 0.0725,
    "texas": 0.0625,
    "new york": 0.04,
    "florida": 0.06,
    # Could add all of the states but let's just say this business operates only here so I can save some time instead of searching for those tax rates:)
}




def load_price_list(financial):
    price_list = {}
    try:
        with open(financial, "r") as file:
            for line in file:
                service, price = line.strip().split(",")
                price_list[service] = float(price)
    except FileNotFoundError:
        print(f"Error: File '{financial}' not found. Please check if the price_list.txt exists in your Python directory or call 7655598100 for assistance.")
    except ValueError:
        print("If you see this error, check your price_list.txt and ensure it follows the correct format: 'service,price'.")
    return price_list






def display_prices(price_list):
    print("\nAvailable services for purchase:")
    for idx, (service, price) in enumerate(price_list.items(), start=1):
        print(f"{idx}. {service}: ${price}")






def generate_text_report(cart, subtotal, total, taxes, price_list, country, state):
    with open("report.txt", "w") as file:
        file.write("Shopping Cart Report\n")
        file.write("--------------------\n") # for better visibility
        for item in cart:
            file.write(f"{item}: ${price_list[item]}\n")
        file.write("--------------------\n")
        file.write(f"Subtotal: ${subtotal:.2f}\n")
        if country.lower() == "us" and state:
            state_tax, federal_tax, total_tax = taxes
            file.write(f"State Tax ({state.title()}): ${state_tax:.2f}\n")
            file.write(f"Federal Tax: ${federal_tax:.2f}\n")
            file.write(f"Total Tax: ${total_tax:.2f}\n")
        elif country.lower() == "czech":
            vat = taxes
            file.write(f"Czech VAT (21%): ${vat:.2f}\n")
        file.write(f"Grand Total: ${total:.2f}\n")
    print("Report saved as 'report.txt'.")







def generate_csv_report(cart, subtotal, total, taxes, price_list, country, state):
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Service", "Price"])
       
        for item in cart:
            writer.writerow([item, price_list[item]])
            writer.writerow([])
            writer.writerow(["Subtotal", subtotal])
        
        if country.lower() == "us" and state:
            state_tax, federal_tax, total_tax = taxes
            writer.writerow(["State Tax", state_tax])
            writer.writerow(["Federal Tax", federal_tax])
            writer.writerow(["Total Tax", total_tax])
        
        elif country.lower() == "czech":
            vat = taxes
            writer.writerow(["Czech VAT (21%)", vat])
        writer.writerow(["Grand Total", total])
    print("Report saved as 'report.csv'.")






def display_web_report(cart, subtotal, total, taxes, price_list, country, state): # had to look up little bit about syntax but in the end it wasn't as complicated
    with open("report.html", "w") as file:
        file.write("<html><body><h1>Shopping Cart Report</h1>")
        file.write("<ul>")
        for item in cart:
            file.write(f"<li>{item}: ${price_list[item]}</li>")
        file.write("</ul>")
        file.write(f"<p>Subtotal: ${subtotal:.2f}</p>")
        
        
        if country.lower() == "us" and state: # two conditions for us as country and state since different taxes apply
            state_tax, federal_tax, total_tax = taxes
            file.write(f"<p>State Tax ({state.title()}): ${state_tax:.2f}</p>")
            file.write(f"<p>Federal Tax: ${federal_tax:.2f}</p>")
            file.write(f"<p>Total Tax: ${total_tax:.2f}</p>")
            file.write(f"<p><b>Grand Total: ${total:.2f}</b></p>")

       
       
        elif country.lower() == "czech":
            vat = taxes
            file.write(f"<p>Czech VAT (21%): ${vat:.2f}</p>")
            file.write(f"<p><b>Grand Total: ${total:.2f}</b></p>")
            file.write("</body></html>")
    
    print("Report saved as 'report.html'. You can open it in a browser.")
    




def calculate_us_taxes(subtotal, state): # formulas for us taxes
    state_tax_rate = statetax.get(state.lower(), 0)
    state_tax = subtotal * state_tax_rate
    federal_tax = subtotal * fedtaxus
    total_tax = state_tax + federal_tax
    
    return state_tax, federal_tax, total_tax




def calculate_czech_taxes(subtotal): # formula for czech tax aka VAT
    vat = subtotal * czetax
    return vat



def main():
    file_path = "price_list.txt"
    price_list = load_price_list(file_path)

    if not price_list:
        print("Exiting program due to missing or invalid price list.")
        return



    cart = []
    subtotal = 0
    services = list(price_list.keys())

    while True:
        display_prices(price_list)
        choice = input("Add to shopping cart by selecting the number (or type 'done' to finish): ").strip() #Some items are named with 2 names (prevention of error)
        if choice.lower() == "done":
            break
        
        
        if choice.isdigit() and 1 <= int(choice) <= len(services): 
            item = services[int(choice) - 1]
            cart.append(item)
            subtotal += price_list[item]
            print(f"Added {item} to your cart. Subtotal so far: ${subtotal:.2f}")
        
        
        else:
            print("Invalid selection. Please select a valid number.")

    print("\nYour shopping cart:", cart)
    print(f"Subtotal: ${subtotal:f}")

    country = input("Are you from the US or Czech Republic? ").strip().lower()
    
    
    if country == "us":
        state = input("Please enter your state (e.g., Indiana, Texas, California): ").strip().lower()
        state_tax, federal_tax, total_tax = calculate_us_taxes(subtotal, state)
        total = subtotal + total_tax
        taxes = (state_tax, federal_tax, total_tax)
    
    
    
    elif country == "czech":
        vat = calculate_czech_taxes(subtotal)
        total = subtotal + vat
        taxes = vat
    
    
    else:
        print("Unsupported country. Sorry we couldn't help you!")
        return

    print(f"Finalized price: ${total:.2f}")

    while True:
        output_choice = input("Choose output format (text/csv/web): ").lower()
        if output_choice == "text":
            generate_text_report(cart, subtotal, total, taxes, price_list, country, state if country == "us" else None)
            break
        
        
        elif output_choice == "csv":
            generate_csv_report(cart, subtotal, total, taxes, price_list, country, state if country == "us" else None)
            break
        
        elif output_choice == "web":
            display_web_report(cart, subtotal, total, taxes, price_list, country, state if country == "us" else None)
            break
        
        else:
            print("Invalid choice. Please type 'text', 'csv', or 'web'.")

if __name__ == "__main__":
    main()
