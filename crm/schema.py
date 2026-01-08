import graphene
from graphene_django import DjangoObjectType
from shop.models import Customer, Order, Product


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'date_ordered', 'total_amount')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock', 'price')


class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  

    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)

        updated_products_list = []
        for product in low_stock_products:
            # Increment stock by 10
            product.stock += 10
            product.save()
            updated_products_list.append(product)

        return UpdateLowStockProducts(
            success=True,
            message=f"Updated {len(updated_products_list)} low-stock products",
            updated_products=updated_products_list
        )


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    customer = graphene.Field(CustomerType, id=graphene.Int(required=True))
    all_orders = graphene.List(OrderType)
    all_products = graphene.List(ProductType)
    low_stock_products = graphene.List(ProductType)

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_customer(self, info, id):
        return Customer.objects.get(pk=id)

    def resolve_all_orders(self, info):
        return Order.objects.all()

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_low_stock_products(self, info):
        return Product.objects.filter(stock__lt=10)


schema = graphene.Schema(query=Query, mutation=Mutation)
