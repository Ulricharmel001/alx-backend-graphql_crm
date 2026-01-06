import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Order


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'date_ordered', 'total_amount')


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    customer = graphene.Field(CustomerType, id=graphene.Int(required=True))
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_customer(self, info, id):
        return Customer.objects.get(pk=id)

    def resolve_all_orders(self, info):
        return Order.objects.all()


schema = graphene.Schema(query=Query)