import predict
import sys


input_image_name = sys.argv[1]

insert_name = "./workspace/"+input_image_name+".jpg"

predict.predict(insert_name)
