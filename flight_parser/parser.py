import json
from bs4 import BeautifulSoup


def read_file(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as xml:
        soup = BeautifulSoup(xml.read(), 'xml')
        return soup


def parse_data_flight(xml_file):
    soup = read_file(xml_file)
    onward_itinerary = get_onward_itinerary(soup)
    return_itinerary = get_return_itinerary(soup)
    prices = soup.find_all('ServiceCharges', ChargeType="TotalAmount", type="SingleAdult")
    onward_departure = []
    onward_arrival = []
    onward_carriers = []
    onw_itinerary = []
    for flight in onward_itinerary:
        carrier = get_carrier(flight)
        onward_carriers.append(carrier)
        itinerary = get_itinerary(flight)
        onw_itinerary.append(itinerary)
        departure = get_departure_time(flight)
        onward_departure.append(departure)
        arrival = get_arrival_time(flight)
        onward_arrival.append(arrival)
    if return_itinerary:
        return_departure = []
        return_arrival = []
        return_carriers = []
        ret_itinerary = []
        for flight in return_itinerary:
            carrier = get_carrier(flight)
            return_carriers.append(carrier)
            itinerary = get_itinerary(flight)
            ret_itinerary.append(itinerary)
            departure = get_departure_time(flight)
            return_departure.append(departure)
            arrival = get_arrival_time(flight)
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


def get_new_flights(xml_file1, xml_file2):
    soup1 = read_file(xml_file1)
    onward_itinerary1 = get_onward_itinerary(soup1)
    soup2 = read_file(xml_file2)
    onward_itinerary2 = get_onward_itinerary(soup2)
    onw_itinerary1 = []
    for flight in onward_itinerary1:
        itinerary = get_itinerary(flight)
        onw_itinerary1.append(itinerary)
    onw_itinerary2 = []
    for flight in onward_itinerary2:
        itinerary = get_itinerary(flight)
        onw_itinerary2.append(itinerary)
    added = list(set(onw_itinerary2) - set(onw_itinerary1))
    print(f'Added itineraries to {xml_file2}')
    for itinerary in added:
        print(itinerary)
    deleted = list(set(onw_itinerary1) - set(onw_itinerary2))
    print(f'Deleted itineraries in {xml_file1}')
    for itinerary in deleted:
        print(itinerary)


def get_changes(xml_file1, xml_file2):
    soup1 = read_file(xml_file1)
    onward_itinerary1 = soup1.find('PricedItineraries').find_all('OnwardPricedItinerary')
    soup2 = read_file(xml_file2)
    onward_itinerary2 = soup2.find('PricedItineraries').find_all('OnwardPricedItinerary')
    count = 0
    for index, data1 in enumerate(onward_itinerary1):
        carrier1 = get_carrier(data1)
        flight_number1 = get_flight_number(data1)
        itinerary1 = get_itinerary(data1)
        departure1 = get_departure_time(data1)
        arrival1 = get_arrival_time(data1)
        class1 = get_class(data1)
        stops1 = get_number_of_stops(data1)
        ticket_type1 = get_ticket_type(data1)
        for data2 in onward_itinerary2:
            carrier2 = get_carrier(data2)
            flight_number2 = get_flight_number(data2)
            itinerary2 = get_itinerary(data2)
            departure2 = get_departure_time(data2)
            arrival2 = get_arrival_time(data2)
            class2 = get_class(data2)
            stops2 = get_number_of_stops(data2)
            ticket_type2 = get_ticket_type(data2)
            if carrier1 == carrier2 and flight_number1 == flight_number2 and itinerary1 == itinerary2:
                if departure1 != departure2:
                    count += 1
                    print(f'{index + 1} flight. Departure time for {carrier1} ({flight_number1}) and  {itinerary1} was changed from {departure1} to {departure2}')
                if arrival1 != arrival2:
                    count += 1
                    print(f'{index + 1} flight. Arrival time for {carrier1} ({flight_number1}) and  {itinerary1} was changed from {arrival1} to {arrival2}')
                if class1 != class2:
                    count += 1
                    print(f'{index + 1} flight. Class for {carrier1} ({flight_number1}) and {itinerary1} was changed from {class1} to {class2}')
                if stops1 != stops2:
                    count += 1
                    print(f'{index + 1} flight. Number of stops for {carrier1} ({flight_number1}) and  {itinerary1} was changed from {stops1} to {stops2}')
                if ticket_type1 != ticket_type2:
                    count += 1
                    print(f'{index + 1} flight. Ticket type for {carrier1} ({flight_number1}) and {itinerary1} was changed from {ticket_type1} to {ticket_type2}')
    print(f'A total of {count} differences were found')
    print('All prices in RS_ViaOW.xml have fields for SingleChild '
          'and SingleInfant. Also RS_Via-3.xml prices are counted '
          'with return itinerary. So all prices will be different.')


def get_itinerary(data):
    source = data.find('Source').text
    between = data.find_all('Source')[-1].text
    destination = data.find_all('Destination')[-1].text
    if between != source:
        itinerary = source + ' - ' + between + ' - ' + destination
    else:
        itinerary = source + ' - ' + destination
    return itinerary


def get_flight_number(data):
    flight_number_first = data.find_all('FlightNumber')[0].text
    flight_number_second = data.find_all('FlightNumber')[-1].text
    flight_number = flight_number_first + ' - ' + flight_number_second
    return flight_number


def get_carrier(data):
    carrier_first = data.find_all('Carrier')[0].text
    carrier_second = data.find_all('Carrier')[-1].text
    carrier = carrier_first + ' - ' + carrier_second
    return carrier


def get_departure_time(data):
    return data.find('DepartureTimeStamp').text


def get_arrival_time(data):
    return data.find_all('ArrivalTimeStamp')[-1].text


def get_number_of_stops(data):
    stops_first = data.find_all('NumberOfStops')[0].text
    stops_second = data.find_all('NumberOfStops')[-1].text
    stops = stops_first + ' - ' + stops_second
    return stops


def get_class(data):
    class_first = data.find_all('Class')[0].text
    class_second = data.find_all('Class')[-1].text
    class_ = class_first + ' - ' + class_second
    return class_


def get_ticket_type(data):
    ticket_type_first = data.find_all('TicketType')[0].text
    ticket_type_second = data.find_all('TicketType')[-1].text
    ticket_type = ticket_type_first + ' - ' + ticket_type_second
    return ticket_type


def get_onward_itinerary(soup_file):
    return soup_file.find('PricedItineraries').find_all('OnwardPricedItinerary')


def get_return_itinerary(soup_file):
    return soup_file.find('PricedItineraries').find_all('ReturnPricedItinerary')
