import json
from bs4 import BeautifulSoup


def read_file(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as xml:
        soup = BeautifulSoup(xml.read(), 'xml')
        return soup


def parse_data_flight(xml_file):
    soup = read_file(xml_file)
    onward_itinerary = soup.find('PricedItineraries').find_all('OnwardPricedItinerary')
    return_itinerary = soup.find('PricedItineraries').find_all('ReturnPricedItinerary')
    prices = soup.find_all('ServiceCharges', ChargeType="TotalAmount", type="SingleAdult")
    onward_departure = []
    onward_arrival = []
    onward_carriers = []
    onw_itinerary = []
    for flight in onward_itinerary:
        carrier_first = flight.find_all('Carrier')[0].text
        carrier_second = flight.find_all('Carrier')[-1].text
        carrier = carrier_first + ' - ' + carrier_second
        onward_carriers.append(carrier)
        source = flight.find('Source').text
        between = flight.find_all('Source')[-1].text
        destination = flight.find_all('Destination')[-1].text
        if between:
            itinerary = source + ' - ' + between + ' - ' + destination
        else:
            itinerary = source + ' - ' + destination
        onw_itinerary.append(itinerary)
        departure = flight.find('DepartureTimeStamp').text
        onward_departure.append(departure)
        arrival = flight.find_all('ArrivalTimeStamp')[-1].text
        onward_arrival.append(arrival)
    if return_itinerary:
        return_departure = []
        return_arrival = []
        return_carriers = []
        ret_itinerary = []
        for flight in return_itinerary:
            carrier_first = flight.find_all('Carrier')[0].text
            carrier_second = flight.find_all('Carrier')[-1].text
            carrier = carrier_first + ' - ' + carrier_second
            return_carriers.append(carrier)
            source = flight.find('Source').text
            between = flight.find_all('Source')[-1].text
            destination = flight.find_all('Destination')[-1].text
            if between:
                itinerary = source + ' - ' + between + ' - ' + destination
            else:
                itinerary = source + ' - ' + destination
            ret_itinerary.append(itinerary)
            departure = flight.find('DepartureTimeStamp').text
            return_departure.append(departure)
            arrival = flight.find_all('ArrivalTimeStamp')[-1].text
            return_arrival.append(arrival)
        result = list(
            zip(
                onward_carriers, onw_itinerary, onward_departure, onward_arrival,
                return_carriers, ret_itinerary, return_departure, return_arrival, prices
            )
        )
        return result
    result = list(zip(onward_carriers, onw_itinerary, onward_departure, onward_arrival, prices))
    return result


def get_data_flight(xml_file):
    result = parse_data_flight(xml_file)
    flights = []
    for flight in result:
        if len(flight) == 9:
            data = {
                "Onward itinerary": {
                    "Carrier": flight[0],
                    "Itinerary": flight[1],
                    "Departure time": parse_time(flight[2]),
                    "Arrival time": parse_time(flight[3]),
                },
                "Return itinerary": {
                    "Carrier": flight[4],
                    "Itinerary": flight[5],
                    "Departure time": parse_time(flight[6]),
                    "Arrival time": parse_time(flight[7]),
                },
            }
        else:
            data = {
                "Onward itinerary": {
                    "Carrier": flight[0],
                    "Itinerary": flight[1],
                    "Departure time": parse_time(flight[2]),
                    "Arrival time": parse_time(flight[3]),
                },
            }
        if data in flights:
            continue
        flights.append(data)
    return json.dumps(flights, indent=4)


def parse_time(time_tag):
    date = time_tag[:-5]
    time = time_tag[-4:-2] + ':' + time_tag[-2:]
    return date, time
