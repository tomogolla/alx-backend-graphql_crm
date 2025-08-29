# crm/schema.py
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError
from django.utils import timezone

from crm.models import Product, Order, Customer
from crm.filters import CustomerFilter, ProductFilter, OrderFilter

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)
        fields = "__all__"

class ProductType(graphene.ObjectType):
    class Meta:
        id = graphene.ID()
        name = graphene.String()
        price = graphene.Float()
        stock = graphene.Int()
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)
        fields = "__all__"

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully.")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput)

    created_customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created = []
        errors = []
        for c in customers:
            if Customer.objects.filter(email=c.email).exists():
                errors.append(f"Email {c.email} already exists.")
                continue
            customer = Customer(name=c.name, email=c.email, phone=c.phone)
            customer.save()
            created.append(customer)
        return BulkCreateCustomers(created_customers=created, errors=errors)

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise ValidationError("Price must be positive.")
        if stock < 0:
            raise ValidationError("Stock cannot be negative.")
        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Invalid customer ID.")

        if not product_ids:
            raise ValidationError("At least one product must be selected.")

        products = Product.objects.filter(pk__in=product_ids)
        if not products.exists():
            raise ValidationError("Invalid product IDs.")

        order = Order(customer=customer)
        order.save()
        order.products.set(products)
        order.total_amount = sum(p.price for p in products)
        order.save()

        return CreateOrder(order=order)
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

class Query(graphene.ObjectType):
    customer = graphene.relay.Node.Field(CustomerType)
    all_customers = DjangoFilterConnectionField(CustomerType, order_by=graphene.List(of_type=graphene.String))

    product = graphene.relay.Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType, order_by=graphene.List(of_type=graphene.String))

    order = graphene.relay.Node.Field(OrderType)
    all_orders = DjangoFilterConnectionField(OrderType, order_by=graphene.List(of_type=graphene.String))

    def resolve_all_customers(self, info, order_by=None, **kwargs):
        qs = Customer.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def resolve_all_products(self, info, order_by=None, **kwargs):
        qs = Product.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def resolve_all_orders(self, info, order_by=None, **kwargs):
        qs = Order.objects.all()
        if order_by:
            qs = qs.order_by(*order_by)
        return qs




# Product type for GraphQL
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # simulate restock
            product.save()
            updated_products.append(product)

        if updated_products:
            return UpdateLowStockProducts(
                success=True,
                message=f"{len(updated_products)} products updated at {timezone.now()}",
                updated_products=updated_products,
            )
        else:
            return UpdateLowStockProducts(
                success=False,
                message="No low-stock products found",
                updated_products=[],
            )

# Add to main mutation
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
