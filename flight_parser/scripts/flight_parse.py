import argparse

from flight_parser.parser import get_data_flight


def main():
    parser = argparse.ArgumentParser(
        description='Generate diff between XML files'
    )
    parser.add_argument('-f, --flights',
                        help='Which flights are included in the itinerary?',
                        action='store_true',
                        dest='flights'
                        )
    parser.add_argument('-c, --changed',
                        help='What has changed about the conditions?',
                        action='store_true',
                        dest='has_changed'
                        )
    parser.add_argument('-a, --added',
                        help='Has a new itinerary been added?',
                        action='store_true',
                        dest='has_added'
                        )
    args = parser.parse_args()
    if args.flights:
        print('In RS_ViaOW.xml:')
        print(get_data_flight('RS_ViaOW.xml'))
        print()
        print('In RS_Via-3.xml:')
        print(get_data_flight('RS_Via-3.xml'))


if __name__ == '__main__':
    main()