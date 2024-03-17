#include "WiFi.h"
#include "aREST.h"
 
aREST rest = aREST();
 
WiFiServer server(80);
 
const char* ssid = "the internet";
const char* password =  "unit0502";

void setup()
{
 
  Serial.begin(115200);
 
  pinMode(15, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
 
  server.begin();
 
}
 
void loop() {
 
  WiFiClient client = server.available();
  if (client) {
 
    while(!client.available()){
      delay(5);
    }
    rest.handle(client);
  }
}