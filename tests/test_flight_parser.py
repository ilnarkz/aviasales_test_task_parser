import json
import sys
from bs4 import BeautifulSoup

from flight_parser.parser import parse_time, get_itinerary, get_flight_number, get_carrier, get_departure_time, \
    get_arrival_time, get_number_of_stops, get_ticket_type, get_class, parse_data_flight, get_new_flights, \
    get_data_flight, get_changes_between_xml_files

XML_FILE1 = 'tests/fixtures/RS_Via-3.xml'
XML_FILE2 = 'tests/fixtures/RS_ViaOW.xml'
XML_FILE_WITH_ONE_FLIGHT = 'tests/fixtures/xml_file_with_one_flight.xml'
XML_FILE_WITH_ONE_FLIGHT_WITH_ADDED_FLIGHT = 'tests/fixtures/xml_file_with_one_flight_with_added_flight.xml'


def test_parse_time():
    assert parse_time('2015-10-30T2040') == ('2015-10-30', '20:40')


def test_flight_data():
    with open(XML_FILE1, 'r', encoding='utf-8') as xml:
        soup_file_xml1 = BeautifulSoup(xml.read(), 'xml')
    with open(XML_FILE2, 'r', encoding='utf-8') as xml:
        soup_file_xml2 = BeautifulSoup(xml.read(), 'xml')
    onward_itinerary = soup_file_xml1.find('PricedItineraries').find_all('OnwardPricedItinerary')
    return_itinerary = soup_file_xml1.find('PricedItineraries').find_all('ReturnPricedItinerary')
    prices_xml1 = soup_file_xml1.find_all('ServiceCharges', ChargeType="TotalAmount", type="SingleAdult")
    prices_xml2 = soup_file_xml2.find_all('ServiceCharges', ChargeType="TotalAmount", type="SingleAdult")
    assert get_itinerary(onward_itinerary[0]) == 'DXB - DEL - BKK'
    assert get_itinerary(return_itinerary[0]) == 'BKK - DEL - DXB'
    assert get_flight_number(onward_itinerary[0]) == '996 - 332'
    assert get_flight_number(return_itinerary[0]) == '333 - 995'
    assert get_carrier(onward_itinerary[0]) == 'AirIndia - AirIndia'
    assert get_carrier(return_itinerary[0]) == 'AirIndia - AirIndia'
    assert get_departure_time(onward_itinerary[0]) == '2015-10-22T0005'
    assert get_departure_time(onward_itinerary[0]) == '2015-10-22T0005'
    assert get_arrival_time(onward_itinerary[0]) == '2015-10-22T1935'
    assert get_arrival_time(return_itinerary[0]) == '2015-10-30T2245'
    assert get_number_of_stops(onward_itinerary[0]) == '0 - 0'
    assert get_number_of_stops(return_itinerary[0]) == '0 - 0'
    assert get_class(onward_itinerary[0]) == 'G - G'
    assert get_class(return_itinerary[0]) == 'U - U'
    assert get_ticket_type(onward_itinerary[0]) == 'E - E'
    assert get_ticket_type(return_itinerary[0]) == 'E - E'
    assert parse_data_flight(XML_FILE1)[0] == ('AirIndia - AirIndia', 'DXB - DEL - BKK', '2015-10-22T0005',
                                               '2015-10-22T1935', 'AirIndia - AirIndia', 'BKK - DEL - DXB',
                                               '2015-10-30T0850', '2015-10-30T2245', prices_xml1[0])
    assert parse_data_flight(XML_FILE2)[0] == ('AirIndia - AirIndia', 'DXB - DEL - BKK',
                                               '2015-10-27T0005', '2015-10-27T1920', prices_xml2[0])
    data = {
        "Onward itinerary": {
            "Carrier": get_carrier(onward_itinerary[0]),
            "Itinerary": get_itinerary(onward_itinerary[0]),
            "Departure time": parse_time(get_departure_time(onward_itinerary[0])),
            "Arrival time": parse_time(get_arrival_time(onward_itinerary[0])),
        },
        "Return itinerary": {
            "Carrier": get_carrier(return_itinerary[0]),
            "Itinerary": get_itinerary(return_itinerary[0]),
            "Departure time": parse_time(get_departure_time(return_itinerary[0])),
            "Arrival time": parse_time(get_arrival_time(return_itinerary[0])),
        },
    }
    assert get_data_flight(XML_FILE_WITH_ONE_FLIGHT) == json.dumps([data], indent=4)


def test_get_new_flights(capsys):
    get_new_flights(XML_FILE_WITH_ONE_FLIGHT, XML_FILE_WITH_ONE_FLIGHT_WITH_ADDED_FLIGHT)
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    out = out.split('\n')
    assert out[1] == 'DXB - CAN - BKK'


def test_get_changes_between_xml_files(capsys):
    get_changes_between_xml_files(XML_FILE1, XML_FILE2)
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    out = out.split('\n')
    assert out[0] == '1 flight. Departure time for AirIndia - AirIndia (996 - 332) and  DXB - DEL - BKK was changed from 2015-10-22T0005 to 2015-10-27T0005'
    assert out[1] == '1 flight. Arrival time for AirIndia - AirIndia (996 - 332) and  DXB - DEL - BKK was changed from 2015-10-22T1935 to 2015-10-27T1920'
    assert out[-4] == '200 flight. Class for Emirates - Emirates (384 - 384) and DXB - BKK was changed from U - U to B - B'
