from saleor_gql_loader import ETLDataLoader
import json
import time

data_loader = ETLDataLoader("bC3PE4EEm9kUawtOVE4oFbmZbEgoj0")

if True:
    channel_id = data_loader.create_channel(name="Default3", isActive=True,
                                            defaultCountry="GR",
                                            currencyCode="EUR",
                                            slug="default3")

if True:
    warehouse_id = data_loader.create_warehouse(name="main warehouse", email="email@example.com",
                                                address={
                                                    "streetAddress1": "a fake street adress",
                                                    "city": "Fake City",
                                                    "postalCode": "1024",
                                                    "country": "CH"
                                                }
                                                )


products = [
    {
        "name": "tea a",
        "description": "description for tea a",
        "category": "green tea",
        "price": 5.5,
        "strength": "medium"
    },
    {
        "name": "tea b",
        "description": "description for tea b",
        "category": "black tea",
        "price": 10.5,
        "strength": "strong"
    },
    {
        "name": "tea c",
        "description": "description for tea c",
        "category": "green tea",
        "price": 9.5,
        "strength": "light"
    }
]

for i, product in enumerate(products):
    product["sku"] = "{:05}-00".format(i)

if True:
    strength_attribute_id = data_loader.create_attribute(
        name="strength", inputType="DROPDOWN", type="PRODUCT_TYPE")
    unique_strength = set([product['strength'] for product in products])
    for strength in unique_strength:
        data_loader.create_attribute_value(
            strength_attribute_id, name=strength)

if True:
    qty_attribute_id = data_loader.create_attribute(
        name="qty", inputType="DROPDOWN", type="PRODUCT_TYPE")
    unique_qty = {"100g", "200g", "300g"}
    for qty in unique_qty:
        data_loader.create_attribute_value(qty_attribute_id, name=qty)

if True:
    product_type_id = data_loader.create_product_type(name="tea",
                                                      hasVariants=True,
                                                      productAttributes=[
                                                          strength_attribute_id],
                                                      variantAttributes=[
                                                          qty_attribute_id],
                                                      kind="NORMAL")

if True:
    unique_categories = set([product['category'] for product in products])

    cat_to_id = {}
    for category in unique_categories:
        cat_to_id[category] = data_loader.create_category(name=category, description=json.dumps({
            "time": time.time(),
            "blocks": [{"type": "paragraph", "data": {"text": category}}],
            "version": "2.20.0"
        }),
            seo={"title": "", "description": ""})

if True:
    for i, product in enumerate(products):
        # print(product_type_id)
        # print(product["name"])
        # print(product["description"])
        # print(product["price"])
        # print(product["sku"])
        # print(product["category"])
        # print([{"id": strength_attribute_id, "values": [product["strength"]]}])
        product_id = data_loader.create_product(product_type_id,
                                                name=product["name"],
                                                description=json.dumps({
                                                    "time": time.time(),
                                                    "blocks": [{"type": "paragraph", "data": {"text": product["description"]}}],
                                                    "version": "2.20.0"
                                                }),
                                                # basePrice=product["price"],
                                                # sku=product["sku"],
                                                category=cat_to_id[product["category"]],
                                                attributes=[
                                                    {"id": strength_attribute_id, "values": [product["strength"]]}],
                                                # isPublished=True
                                                )
        print(product_id)
        products[i]["id"] = product_id

# create some variant for each product:
product_variants = []
if True:
    for product in products:
        for i, qty in enumerate(unique_qty):
            print(product_id)
            print({"id": qty_attribute_id, "values": [qty]})
            # print(product["sku"].replace("-00", "-1{}".format(i+1)))
            # print([{"id": qty_attribute_id, "values": [qty]}])
            # print(product["price"])
            # print(0.75)
            # print([{"warehouse": warehouse_id, "quantity": 15}])
            variant_id = data_loader.create_product_variant(product["id"],
                                                            sku=product["sku"].replace(
                                                                "-00", "-1{}".format(i+1)),
                                                            attributes=[
                                                                {"id": qty_attribute_id, "values": [qty]}],
                                                            # costPrice=product["price"],
                                                            weight=0.75,
                                                            stocks=[{"warehouse": warehouse_id, "quantity": 15}])
            product_variants.append(variant_id)

print(product_variants)
if True:
    for product in products:
        product_channel_listing_update = data_loader.product_channel_listing_update(product["id"],channelId=channel_id, isAvailableForPurchase=True, isPublished=True
        # , addVariants=product_variants
        )

if True:
    # for product in products:
    # print(channel_id)
    for product_variant in product_variants:
        # print(product_variant)
        product_variant_channel_id = data_loader.product_variant_channel_listing_update(product_variant,
                                                                                        channelId=channel_id, price=10, costPrice=8)
