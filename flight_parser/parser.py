import json
from typing import Tuple
import bs4
from bs4 import BeautifulSoup


LENGTH_DATA_FLIGHT_WITH_RETURN_ITINERARY = 9


def read_file(xml_file: str) -> bs4.BeautifulSoup:
    with open(xml_file, 'r', encoding='utf-8') as xml:
        soup = BeautifulSoup(xml.read(), 'xml')
        return soup


def get_itinerary(data: bs4.element.Tag) -> str:
    source = data.find('Source').text
    between = data.find_all('Source')[-1].text
    destination = data.find_all('Destination')[-1].text
    if between != source:
        itinerary = f'{source} - {between} - {destination}'
    else:
        itinerary = f'{source} - {destination}'
    return itinerary


def get_flight_number(data: bs4.element.Tag) -> str:
    flight_number_first = data.find_all('FlightNumber')[0].text
    flight_number_second = data.find_all('FlightNumber')[-1].text
    flight_number = f'{flight_number_first} - {flight_number_second}'
    return flight_number


def get_carrier(data: bs4.element.Tag) -> str:
    carrier_first = data.find_all('Carrier')[0].text
    carrier_second = data.find_all('Carrier')[-1].text
    carrier = f'{carrier_first} - {carrier_second}'
    return carrier


def get_departure_time(data: bs4.element.Tag) -> str:
    return data.find('DepartureTimeStamp').text


def get_arrival_time(data: bs4.element.Tag) -> str:
    return data.find_all('ArrivalTimeStamp')[-1].text


def get_number_of_stops(data: bs4.element.Tag) -> str:
    stops_first = data.find_all('NumberOfStops')[0].text
    stops_second = data.find_all('NumberOfStops')[-1].text
    stops = f'{stops_first} - {stops_second}'
    return stops


def get_class(data: bs4.element.Tag) -> str:
    class_first = data.find_all('Class')[0].text
    class_second = data.find_all('Class')[-1].text
    class_ = f'{class_first} - {class_second}'
    return class_


def get_ticket_type(data: bs4.element.Tag) -> str:
    ticket_type_first = data.find_all('TicketType')[0].text
    ticket_type_second = data.find_all('TicketType')[-1].text
    ticket_type = f'{ticket_type_first} - {ticket_type_second}'
    return ticket_type


def get_onward_itinerary(soup_file: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return soup_file.find('PricedItineraries').find_all('OnwardPricedItinerary')


def get_return_itinerary(soup_file: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return soup_file.find('PricedItineraries').find_all('ReturnPricedItinerary')


def is_same_flight(carrier_xml1: str, carrier_xml2: str,
                   flight_number_xml1: str, flight_number_xml2: str,
                   itinerary_xml1: str, itinerary_xml2: str) -> bool:
    return carrier_xml1 == carrier_xml2 and flight_number_xml1 == flight_number_xml2 and itinerary_xml1 == itinerary_xml2


def parse_time(time_tag: str) -> Tuple[str, str]:
    date = time_tag[:-5]
    time = f'{time_tag[-4:-2]}:{time_tag[-2:]}'
    return date, time


def parse_data_flight(xml_file: str) -> list:
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


def get_data_flight(xml_file: str) -> str:
    result = parse_data_flight(xml_file)
    flights = []
    for flight in result:
        if len(flight) == LENGTH_DATA_FLIGHT_WITH_RETURN_ITINERARY:
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


def get_new_flights(xml_file1: str, xml_file2: str) -> None:
    soup_xml1 = read_file(xml_file1)
    onward_itinerary_xml1 = get_onward_itinerary(soup_xml1)
    soup_xml2 = read_file(xml_file2)
    onward_itinerary_xml2 = get_onward_itinerary(soup_xml2)
    all_onward_itinerary_xml1 = []
    for flight in onward_itinerary_xml1:
        itinerary = get_itinerary(flight)
        all_onward_itinerary_xml1.append(itinerary)
    all_onward_itinerary_xml2 = []
    for flight in onward_itinerary_xml2:
        itinerary = get_itinerary(flight)
        all_onward_itinerary_xml2.append(itinerary)
    added = list(set(all_onward_itinerary_xml2) - set(all_onward_itinerary_xml1))
    print(f'Added itineraries to {xml_file2}')
    for itinerary in added:
        print(itinerary)
    deleted = list(set(all_onward_itinerary_xml1) - set(all_onward_itinerary_xml2))
    print(f'Deleted itineraries in {xml_file1}')
    for itinerary in deleted:
        print(itinerary)


def get_changes_between_xml_files(xml_file1: str, xml_file2: str) -> None:
    soup_xml1 = read_file(xml_file1)
    onward_itinerary_xml1 = get_onward_itinerary(soup_xml1)
    soup_xml2 = read_file(xml_file2)
    onward_itinerary_xml2 = get_onward_itinerary(soup_xml2)
    count = 0
    for index, data_xml1 in enumerate(onward_itinerary_xml1):
        carrier_xml1 = get_carrier(data_xml1)
        flight_number_xml1 = get_flight_number(data_xml1)
        itinerary_xml1 = get_itinerary(data_xml1)
        departure_xml1 = get_departure_time(data_xml1)
        arrival_xml1 = get_arrival_time(data_xml1)
        class_xml1 = get_class(data_xml1)
        stops_xml1 = get_number_of_stops(data_xml1)
        ticket_type_xml1 = get_ticket_type(data_xml1)
        for data_xml2 in onward_itinerary_xml2:
            carrier_xml2 = get_carrier(data_xml2)
            flight_number_xml2 = get_flight_number(data_xml2)
            itinerary_xml2 = get_itinerary(data_xml2)
            departure_xml2 = get_departure_time(data_xml2)
            arrival_xml2 = get_arrival_time(data_xml2)
            class_xml2 = get_class(data_xml2)
            stops_xml2 = get_number_of_stops(data_xml2)
            ticket_type_xml2 = get_ticket_type(data_xml2)
            if is_same_flight(carrier_xml1, carrier_xml2, flight_number_xml1, flight_number_xml2, itinerary_xml1, itinerary_xml2):
                if departure_xml1 != departure_xml2:
                    count += 1
                    print(f'{index + 1} flight. Departure time for {carrier_xml1} ({flight_number_xml1}) and  {itinerary_xml1} was changed from {departure_xml1} to {departure_xml2}')
                if arrival_xml1 != arrival_xml2:
                    count += 1
                    print(f'{index + 1} flight. Arrival time for {carrier_xml1} ({flight_number_xml1}) and  {itinerary_xml1} was changed from {arrival_xml1} to {arrival_xml2}')
                if class_xml1 != class_xml2:
                    count += 1
                    print(f'{index + 1} flight. Class for {carrier_xml1} ({flight_number_xml1}) and {itinerary_xml1} was changed from {class_xml1} to {class_xml2}')
                if stops_xml1 != stops_xml2:
                    count += 1
                    print(f'{index + 1} flight. Number of stops for {carrier_xml1} ({flight_number_xml1}) and  {itinerary_xml1} was changed from {stops_xml1} to {stops_xml2}')
                if ticket_type_xml1 != ticket_type_xml2:
                    count += 1
                    print(f'{index + 1} flight. Ticket type for {carrier_xml1} ({flight_number_xml1}) and {itinerary_xml1} was changed from {ticket_type_xml1} to {ticket_type_xml2}')
    print(f'A total of {count} differences were found')
    print('All prices in RS_ViaOW.xml have fields for SingleChild '
          'and SingleInfant. Also RS_Via-3.xml prices are counted '
          'with return itinerary. So all prices will be different.')
