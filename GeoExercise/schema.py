import graphene
from graphene_django import DjangoObjectType, DjangoListField

from countries.models import Country, City


####### Queries ######
class CityType(DjangoObjectType):
    class Meta:
        model = City
        field = ("id", "name")


class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        field = ("id", "name", "cities")

    cities = DjangoListField(CityType)


class Query(graphene.ObjectType):
    list_countries = graphene.List(CountryType)
    read_country = graphene.Field(CountryType, name=graphene.String())

    def resolve_list_countries(self, info):
        return Country.objects.all()

    def resolve_read_country(self, info, name):
        return Country.objects.get(name=name)


##### Mutations #######

class CityMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        country_id = graphene.BigInt()

    city = graphene.Field(CityType)
    @classmethod
    def mutate(cls, root, info, name, country_id):
        City.objects.create(name=name, country=Country.objects.get(country_id=country_id))


class CountryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    country = graphene.Field(CountryType)

    @classmethod
    def mutate(cls, root, info, name):
        Country.objects.create(name=name)


class Mutation(graphene.ObjectType):
    create_country = CountryMutation.Field()
    create_city = CityMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
