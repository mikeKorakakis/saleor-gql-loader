from saleor_gql_loader import ETLDataLoader
import json
import time

data_loader = ETLDataLoader("bC3PE4EEm9kUawtOVE4oFbmZbEgoj0")

if False:
    warehouse_id = data_loader.create_warehouse(slug="test_warehouse", name="test", email="email@example.com",
                                                address={
                                                    "streetAddress1": "a fake street adress",
                                                    "city": "Fake City",
                                                    "postalCode": "1024",
                                                    "country": "CH"
                                                }
                                                )
if True:
    warehouse_id = data_loader.create_category(name="test_category", description=json.dumps({
        "time": time.time(), "blocks": [{"type": "paragraph", "data": {"text": "test description"}}], "version": "2.20.0"
    }),
        seo={"title": "", "description": ""})
