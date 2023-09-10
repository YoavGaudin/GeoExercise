import json

from graphene_django.utils import GraphQLTestCase

from countries.models import Country, City


# Create your tests here.

class CountriesTestCase(GraphQLTestCase):

    def test_get_all_countries(self):
        france = Country.objects.create(name='France')
        israel = Country.objects.create(name='Israel')
        City.objects.create(name='Paris', country=france)
        City.objects.create(name='Aix-en-Provence', country=france)
        City.objects.create(name='Tel-Aviv', country=israel)
        City.objects.create(name='Haifa', country=israel)

        response = self.query('''
        query {
            listCountries {
                name
                cities {
                    name
                }
            }
        }''')

        expected_countries = {'data': {
            'listCountries': [{'cities': [{'name': 'Paris'}, {'name': 'Aix-en-Provence'}], 'name': 'France'},
                              {'cities': [{'name': 'Tel-Aviv'}, {'name': 'Haifa'}], 'name': 'Israel'}]}}
        actual_countries = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEquals(actual_countries, expected_countries)

    def test_create_country(self):
        query = '''
        mutation MyMutation {
            createCountry(name: "USA") {
                country {
                  name
                  cities {
                    name
                  }
                }
              }
            }
        '''
        response = self.query(query)
        self.assertResponseNoErrors(response)
        self.assertTrue(Country.objects.filter(name='USA').exists())
        # test country name uniqueness
        response = self.query(query)
        self.assertResponseHasErrors(response)


    def test_create_city(self):
        query = '''
        mutation MyMutation {{
          createCity(countryId: {}, name: "{}") {{
            city {{
              name
            }}
          }}
        }}
        '''

        response = self.query(query.format('1', 'New-York'))
        self.assertResponseHasErrors(response)
        Country.objects.create(name='USA')
        response = self.query(query.format(1, 'New-York'))
        self.assertResponseNoErrors(response)
        self.assertTrue(City.objects.filter(name='New-York').exists())

        response = self.query(query.format(1, 'New-York'))
        self.assertResponseHasErrors(response)
