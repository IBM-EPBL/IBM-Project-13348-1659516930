from cloudant.client import Cloudant

client = Cloudant.iam("ca94e55a-7b99-4ad2-82fa-1b2dc7d7d811-bluemix", "3LtbSU2M5BUxRZDPklWM459UJn5bOAHp2dCMoRcoNX2S", connect = True)

my_database = client.create_database('diabetic-retinopathy')