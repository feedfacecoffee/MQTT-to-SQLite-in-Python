#written by William R. Herndon - feedfacecoffee@gmail.com
import paho.mqtt.client as mqtt
import sqlite3

#setup sqlite connection
sqlconn = sqlite3.connect('/MQTTToSQLite/mqttDB.sqlite');
c = sqlconn.cursor();

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc));

	client.subscribe("/security/#");

def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.payload)+" "+str(msg.retain));
	c.execute('insert into MqttData values (datetime(),?,?,?);',(msg.topic, msg.payload, msg.retain));
	sqlconn.commit();

client = mqtt.Client();
client.on_connect = on_connect;
client.on_message = on_message;

client.connect("10.0.1.250", 1883, 60);

client.loop_forever();
