#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

char buffer[3];
int8_t i = 0;
uint16_t dmxchannel;
uint8_t dmxvalue;
bool dataready = false;

unsigned long pingtime = 0;
unsigned long reconnecttime = 0;
unsigned long ontimer = 0;
unsigned long offtimer = 0;

unsigned short ontime = 255;
unsigned short offtime = 0;
unsigned short brightness = 255;

const char* ssid = "tupsu";

char server[] = "jiihon.com";
WiFiClient client;
//WiFiUDP Udp;

#define STROBO_PIN 10


void setup() {
  Serial.begin(115200);
  pinMode(STROBO_PIN, OUTPUT);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(""); Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());

  while (!client.connect(server, 9999)) {}
  Serial.println("Connected to "); Serial.println(server);
  client.print("cbsZ\n"); //Transmit password

  set_timer(&pingtime, 60000);
  set_timer(&reconnecttime, 3600000);
  set_timer(&ontimer, ontime);
}


void loop() {

  char readchar;

  while (client.available() && i<3) {

    readchar = client.read();
    //Serial.println((unsigned int)readchar);

    // DMX command
    if(i==0 && (readchar&127) =='D') {
      dmxchannel = readchar&128;
    }
    // Ping command
    else if(i==0 && (readchar&127) == 'P') {
      client.print("STROBO HELLO\n");
      i=2;
    }
    // Print DMX log
    else if(i==0 && (readchar&127) == 'L') {
      //logdmx();
      i=2;
    }
    else if(i==0) {
      // First char did not contain valid header!
      i--;
    }
    else if(i==1){
      dmxchannel = dmxchannel<<1 | readchar;
    }
    else if(i==2){
      dmxvalue = readchar;
      dataready = true;
      Serial.println("Data ready");
    }

    if(i<2) {
      i++;
    }
    else {
      i = 0;
    }

    if (dataready) {
      // DO SOMETHING!

      // DMX Channel 8 = Ontime
      // DMX Channel 9 = Offtime

      Serial.print("DMX Data: "); Serial.print(dmxchannel); Serial.print(" "); Serial.println(dmxvalue);

      if(dmxchannel==8) {
        ontime = dmxvalue;
      }
      else if(dmxchannel==9) {
        offtime = dmxvalue;
        // reset timers
        ontimer=0;
        offtimer=0;
        set_timer(&ontimer, 0);
      }

      dataready = false;

    }
  }


  // Timer handlers
  if(timer(&ontimer)) {
    if(ontime>0) {
      digitalWrite(STROBO_PIN, HIGH);
    }
    set_timer(&offtimer, ontime*10);

  }

  if(timer(&offtimer)) {
    if(offtime>0) {
      digitalWrite(STROBO_PIN, LOW);
    }
    set_timer(&ontimer, offtime*10);
  }

  if(timer(&pingtime)) {
    size_t retval;
    retval = client.print("STROBO HELLO\n");
    Serial.println("STROBO HELLO\n");

    if(!retval) {
      reconnect();
    }
    set_timer(&pingtime, 60000);
  }

  if(timer(&reconnecttime)) {
    reconnect();
    set_timer(&reconnecttime, 3600000);
  }
}


// Reconnect on error
void reconnect() {
    Serial.println("Reconnecting...");
    client.stop();
    while (!client.connect(server, 9999)) {}
    client.print("cbsZ\n"); //Transmit password
    Serial.println("done\n");
}

boolean timer(unsigned long *trigger)
{
  if (*trigger && (long)(millis() - *trigger) >= 0)
  {
    *trigger = 0;
    return true;
  }
  else
    return false;
}

void set_timer(unsigned long *timer, unsigned long value)
{
  *timer = millis() + value;
  if (*timer == 0)
    (*timer)++;
}
