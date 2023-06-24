import requests
from collections import defaultdict

API_KEY = 'API_KEY_HERE'

def get_search_results(url, city, state_code, limit):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "realty-in-us.p.rapidapi.com"
    }
    params = {
        "city": city,
        "state_code": state_code,
        "limit": limit,
        "offset": "0",
        "sort": "relevance"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def main():
    city = input("Enter the area's city: ")
    state_code = input("Enter the area's state code (e.g., 'CA' for California): ")
    limit = input("Enter the number of houses you want to see: ")
    rent = int(input("Enter the target rent ratio: "))

    # Fetch average rental price per square foot for each bedroom count
    rent_url = "https://realty-in-us.p.rapidapi.com/properties/v2/list-for-rent"
    rent_search_results = get_search_results(rent_url, city, state_code, "500")
    properties_for_rent = rent_search_results["properties"]

    bed_counts = defaultdict(lambda: {"total_rent_price": 0, "total_sqft": 0, "count": 0})
    for prop in properties_for_rent:
        price = prop.get("price", None)
        building_size = prop.get("building_size", {}).get("size", None)
        beds = prop.get("beds", None)

        if price is not None and building_size is not None and beds is not None:
            bed_counts[beds]["total_rent_price"] += price
            bed_counts[beds]["total_sqft"] += building_size
            bed_counts[beds]["count"] += 1

    average_rent_price_per_sqft = {
        beds: info["total_rent_price"] / info["total_sqft"] for beds, info in bed_counts.items()
    }

    # Fetch properties for sale
    sale_url = "https://realty-in-us.p.rapidapi.com/properties/v2/list-for-sale"
    sale_search_results = get_search_results(sale_url, city, state_code, limit)
    properties_for_sale = sale_search_results["properties"]

    for prop in properties_for_sale:
        price = prop.get('price', None)
        if price != None and price < 250000 and price > 60000:
            beds = prop.get("beds", None)
            building_size = prop.get("building_size", {}).get("size", None)

            if building_size is not None and beds is not None and beds in average_rent_price_per_sqft:
                estimated_rental_price = average_rent_price_per_sqft[beds] * building_size
                if estimated_rental_price != None and (estimated_rental_price / price) > (rent / 100):
                    print(f"Property ID: {prop.get('property_id', 'N/A')}")
                    print(f"Listing ID: {prop.get('listing_id', 'N/A')}")
                    print(f"Address: {prop.get('address', {}).get('line', 'N/A')}")
                    print(f"City: {prop.get('address', {}).get('city', 'N/A')}")
                    print(f"State: {prop.get('address', {}).get('state_code', 'N/A')}")
                    print(f"Postal Code: {prop.get('address', {}).get('postal_code', 'N/A')}")
                    print(f"Price: ${prop.get('price', 'N/A')}")
                    print(f"Beds: {prop.get('beds', 'N/A')}")
                    print(f"Baths: {prop.get('baths_full', 'N/A')}")
                    print(f"Building Size: {prop.get('building_size', {}).get('size', 'N/A')} sqft")
                    print(f"Lot Size: {prop.get('lot_size', {}).get('size', 'N/A')} sqft")
                    print(f"Estimated Rental Price: ${estimated_rental_price:.2f}")
                    print("---------------------------------------------------")

if __name__ == "__main__":
    main()
