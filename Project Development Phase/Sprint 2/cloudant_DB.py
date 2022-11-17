from cloudant.client import Cloudant

client = Cloudant.iam("55cd1a75-db28-4490-b6d3-0e709667814a-bluemix", "l2E_BgNgSm4KW3DZ9Tzqcrgufouhz_1zec6RI1i2gAkK", connect = True)

my_database = client.create_database('diabetic-retinopathy')