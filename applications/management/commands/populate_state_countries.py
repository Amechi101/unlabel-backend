# -*- coding: utf-8 -*-
import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from oscar.core.loading import get_model

Country = get_model('address', 'Country')
States = get_model('address', 'States')
statesList = [
      'Alaska',
      'Alabama',
      'Arkansas',
      'American Samoa',
      'Arizona',
      'California',
      'Colorado',
      'Connecticut',
      'District of Columbia',
      'Delaware',
      'Florida',
      'Georgia',
      'Guam',
      'Hawaii',
      'Iowa',
      'Idaho',
      'Illinois',
      'Indiana',
      'Kansas',
      'Kentucky',
      'Louisiana',
      'Massachusetts',
      'Maryland',
      'Maine',
      'Michigan',
      'Minnesota',
      'Missouri',
      'Northern Mariana Islands',
      'Mississippi',
      'Montana',
      'National',
      'North Carolina',
      'North Dakota',
      'Nebraska',
      'New Hampshire',
      'New Jersey',
      'New Mexico',
      'Nevada',
      'New York',
      'Ohio',
      'Oklahoma',
      'Oregon',
      'Pennsylvania',
      'Puerto Rico',
      'Rhode Island',
      'South Carolina',
      'South Dakota',
      'Tennessee',
      'Texas',
      'Utah',
      'Virginia',
      'Virgin Islands',
      'Vermont',
      'Washington',
      'Wisconsin',
      'West Virginia',
      'Wyoming'
]

class Command(BaseCommand):
    help = "Populates the list of countries with data from pycountry."

    option_list = BaseCommand.option_list + (
        make_option(
            '--no-shipping',
            action='store_false',
            dest='is_shipping',
            default=True,
            help="Don't mark countries for shipping"),
        make_option(
            '--initial-only',
            action='store_true',
            dest='is_initial_only',
            default=False,
            help="Exit quietly without doing anything if countries were already populated."),
    )

    def handle(self, *args, **options):
        try:
            states = [
                States(
                    name=state
                )
                for state in statesList]
            States.objects.bulk_create(states)

        except:
            print ("Your db is already populated with states in USA")
        try:
            import pycountry
        except ImportError:
            raise CommandError(
                "You are missing the pycountry library. Install it with "
                "'pip install pycountry'")

        if Country.objects.exists():
            if options.get('is_initial_only', False):
                # exit quietly, as the initial load already seems to have happened.
                self.stdout.write("Countries already populated; nothing to be done.")
                sys.exit(0)
            else:
                raise CommandError(
                    "You already have countries in your database. This command "
                    "currently does not support updating existing countries.")

        countries = [
            Country(
                iso_3166_1_a2=country.alpha_2,
                iso_3166_1_a3=country.alpha_3,
                iso_3166_1_numeric=country.numeric,
                printable_name=country.name,
                name=getattr(country, 'official_name', ''),
                is_shipping_country=options['is_shipping'])
            for country in pycountry.countries]

        Country.objects.bulk_create(countries)
        self.stdout.write("Successfully added %s countries." % len(countries))
