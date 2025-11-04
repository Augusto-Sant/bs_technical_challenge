import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from sales.models import Product, Order, OrderItem


class Command(BaseCommand):
    help = "Populates the database with sample historical orders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--orders",
            type=int,
            default=20,
            help="Number of orders to create (default: 20)",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Number of days in the past to distribute orders (default: 90 days)",
        )

    def handle(self, *args, **options):
        num_orders = options["orders"]
        days_back = options["days"]

        # Check if there are products in the database
        products = list(Product.objects.all())

        if not products:
            self.stdout.write(self.style.ERROR("❌ No products found in the database!"))
            self.stdout.write(
                self.style.WARNING("💡 Run first: python manage.py import_products")
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f"📦 Creating {num_orders} historical orders with available products..."
            )
        )
        self.stdout.write(f"📊 {len(products)} products available in the database")
        self.stdout.write("=" * 80)

        created_orders = 0
        created_items = 0

        for i in range(num_orders):
            try:
                # Generate a random date in the past
                days_ago = random.randint(0, days_back)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)

                created_date = timezone.now() - timedelta(
                    days=days_ago, hours=hours_ago, minutes=minutes_ago
                )

                # Create the order (total will be calculated later)
                order = Order.objects.create(total=Decimal("0.00"))

                # Force the creation date
                Order.objects.filter(pk=order.pk).update(created_at=created_date)
                order.refresh_from_db()

                # Define how many items the order will have (1 to 5 different products)
                num_items = random.randint(1, 5)

                # Select random products without repetition
                selected_products = random.sample(
                    products, min(num_items, len(products))
                )

                order_total = Decimal("0.00")
                order_items_list = []

                for product in selected_products:
                    # Random quantity (1 to 3 units)
                    quantity = random.randint(1, 3)

                    # Use the current product price
                    price = product.price

                    # Create the order item
                    order_item = OrderItem.objects.create(
                        order=order, product=product, quantity=quantity, price=price
                    )

                    subtotal = price * quantity
                    order_total += subtotal

                    order_items_list.append(
                        f"   • {product.name[:40]}... x{quantity} = ${subtotal}"
                    )
                    created_items += 1

                # Update the order total
                order.total = order_total
                order.save()

                created_orders += 1

                # Show details of the created order
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✅ Order #{order.pk} - {order.created_at.strftime('%m/%d/%Y %H:%M')}"
                    )
                )
                self.stdout.write(f"   💰 Total: ${order_total}")
                self.stdout.write(f"   📦 Items ({len(order_items_list)}):")
                for item_desc in order_items_list:
                    self.stdout.write(item_desc)

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error creating order {i + 1}: {e}")
                )

        # Final summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS(f"✅ Orders created: {created_orders}"))
        self.stdout.write(self.style.SUCCESS(f"📦 Items created: {created_items}"))
        self.stdout.write(
            self.style.SUCCESS(
                f"💰 Total sales value: ${Order.objects.aggregate(total=models.Sum('total'))['total'] or 0}"
            )
        )
        self.stdout.write(self.style.SUCCESS("\n🎉 Order population completed!"))
