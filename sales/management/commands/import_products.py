import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from sales.models import Product


class Command(BaseCommand):
    help = "Import products from a JSON file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="products.json",
            help="path to products JSON file (default: products.json)",
        )

    def handle(self, *args, **options):
        json_file = options["file"]

        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f"❌ File {json_file} not found!"))
            return

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                products_data = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading file: {e}"))
            return

        self.stdout.write(
            self.style.WARNING(
                f"📦 Init products import. Length: {len(products_data)}."
            )
        )
        self.stdout.write("=" * 80)

        created_count = 0
        updated_count = 0
        error_count = 0

        for product_data in products_data:
            try:
                sku = product_data.get("sku")

                if not sku:
                    self.stdout.write(self.style.ERROR("❌ No SKU found, skipping..."))
                    error_count += 1
                    continue

                product_info = {
                    "name": product_data.get("name", ""),
                    "price": product_data.get("price", 0),
                    "stock_qty": product_data.get("stock_qty", 0),
                    "description": product_data.get("description", ""),
                    "brand": product_data.get("brand", ""),
                }

                product, created = Product.objects.update_or_create(
                    sku=sku, defaults=product_info
                )

                if product_data.get("image_path"):
                    image_path = os.path.join("uploads", product_data["image_path"])

                    if os.path.exists(image_path):
                        with open(image_path, "rb") as img_file:
                            filename = os.path.basename(image_path)
                            product.image.save(filename, File(img_file), save=True)

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"✅ Created: {sku} - {product.name[:50]} (with image)"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"🔄 Updated: {sku} - {product.name[:50]} (with image)"
                                )
                            )
                    else:
                        if created:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"✅ Created: {sku} - {product.name[:50]} (no image)"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"🔄 Updated: {sku} - {product.name[:50]} (no image)"
                                )
                            )
                else:
                    if created:
                        self.stdout.write(
                            self.style.WARNING(
                                f"✅ Created: {sku} - {product.name[:50]} (no image)"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"🔄 Updated: {sku} - {product.name[:50]} (no image)"
                            )
                        )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Error when processing product {product_data.get('sku', 'no SKU')}: {e}"
                    )
                )
                error_count += 1

        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS(f"✅ Created products: {created_count}"))
        self.stdout.write(self.style.SUCCESS(f"🔄 Updated products: {updated_count}"))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"❌ Errors: {error_count}"))
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Finished import!"))
