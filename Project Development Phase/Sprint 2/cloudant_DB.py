from cloudant.client import Cloudant

client = Cloudant.iam("6748bc63-c73d-431e-9737-c70dfbbcfc67-bluemix", "zejuFJi6IoYqpgfPHRnQ8S12LkJudVndHK9aJpTCr7ka", connect = True)

my_database = client.create_database('diabetic-retinopathy')