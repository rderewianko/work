from paho.mqtt import client as mqtt
import ssl

host = input("Product ID? ") + ".m2.exosite-staging.io"
cert = "./trusted.crt"

def on_connect(client, userdata, flags, rc):
    resource = "$resource/" + input("Resource ID? ")
    client.publish(resource, input("Value? "), qos=0)
    client.disconnect()

def on_message(client, userdata, msg):
 print("Value set, previous was: ", msg.payload.decode())

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("DisConnected with error", rc)
        exit()

client = mqtt.Client(client_id="")
client.tls_set(
    ca_certs=cert,
    server_hostname=host,
    cert_reqs=ssl.CERT_NONE
)
client.tls_insecure_set(True)
# client.username_pw_set(input("User? "), input("Password? "))
client.username_pw_set("", input("Device token? "))

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(host, 443)
client.loop_forever()