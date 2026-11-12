#include <WiFiS3.h>
#include "secrets.h"

const int sensorPin = A0;            

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS; //wifi connection state 

WiFiClient client;

void sendDataToServer(int rawValue){
  //Opens a connection to flask server, sends HTTP request, closes 
  if(client.connect(SERVER_IP, SERVER_PORT)){ //if connected to server
    Serial.println("Connected to Server");
    
    //GET request 
    String url = "/log_sensor?raw=" + String(rawValue);
    client.println("GET " + url + " HTTP/1.1");
    client.println("Host: " + String(SERVER_IP));
    client.println("Connection: close");
    client.println(); //empty line marks the end of HTTP request 

    client.stop(); //closes socket conection 
    Serial.println("Sent.");
  } else{ //if uh oh print failure 
    Serial.println("Connection to server failed");
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);

//verifies wifi is communication properly 
  if(WiFi.status() == WL_NO_MODULE){
    Serial.println("Can't connect to WiFi module");
    while(true); //If wifi module isn't found or won't respond don't move on 
  }

  while(status != WL_CONNECTED){
    //try and connect to wifi 
    Serial.print("Connecting to: "); 
    Serial.println(ssid); //print target ssid name 
    status = WiFi.begin(ssid, pass); //check for wifi with saved ssid and try and connect using pass
    delay(5000); //wait 5 seconds to prevent crashing and burning   
  }
  Serial.print("Connected to ");
  Serial.println(ssid);

}

void loop() {
  int sensorValue = analogRead(sensorPin);  
  Serial.print("Sensor value:");
  Serial.println(sensorValue); //print raw value to serial for debugging purposes 

  sendDataToServer(sensorValue); //send sensor data to the server 

  delay(5000); //wait 5 seconds to prevent crashing and burning                        
}

