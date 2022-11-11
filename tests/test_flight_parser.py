import pytest
from bs4 import BeautifulSoup

from flight_parser.parser import parse_time, get_itinerary, get_flight_number, get_carrier, get_departure_time, \
    get_arrival_time, get_number_of_stops, get_ticket_type, get_class

XML_FILE1 = 'RS_Via-3.xml'
XML_FILE2 = 'RS_ViaOW.xml'


def read_files(xml_file):
    file1 = open(xml_file).read()
    return file1


@pytest.mark.parametrize('received, expected', [('2015-10-30T2040', ('2015-10-30', '20:40')),
                                                ('2000-12-31T0000', ('2000-12-31', '00:00')),
                                                ('2022-01-01T2359', ('2022-01-01', '23:59'))])
def test_parse_time(received, expected):
    assert parse_time(received) == expected


def test_flight_data():
    with open(XML_FILE1, 'r', encoding='utf-8') as xml:
        soup_file = BeautifulSoup(xml.read(), 'xml')
    onward_itinerary = soup_file.find('PricedItineraries').find_all('OnwardPricedItinerary')
    return_itinerary = soup_file.find('PricedItineraries').find_all('ReturnPricedItinerary')
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
