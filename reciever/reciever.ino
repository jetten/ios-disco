#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Conceptinetics.h>

char buffer[3];
int8_t i = 0;
uint16_t dmxchannel;
uint8_t dmxvalue;
bool dataready = false;

unsigned long pingtime = 0;
unsigned long smoketime = 0;
unsigned long powerontime = 0;
unsigned long reconnecttime = 0;
bool smokeon = false;

byte mac[] = {0x7E, 0xE4, 0xAD, 0x78, 0xA3, 0xC7};
char server[] = "jiihon.com";
EthernetClient client;
EthernetUDP Udp;

unsigned char dmxvalues[7];

//
// The master will control 100 Channels (1-100)
//
// depending on the ammount of memory you have free you can choose
// to enlarge or schrink the ammount of channels (minimum is 1)
//
#define DMX_MASTER_CHANNELS   7

//
// Pin number to change read or write mode on the shield
//
#define RXEN_PIN                2

// Pin number for controlling relay
#define POWERCTRL_PIN 3

// Configure a DMX master controller, the master controller
// will use the RXEN_PIN to control its write operation
// on the bus
DMX_Master        dmx_master ( DMX_MASTER_CHANNELS, RXEN_PIN );


// the setup routine runs once when you press reset:
void setup() {

  pinMode(POWERCTRL_PIN, OUTPUT);
  digitalWrite(POWERCTRL_PIN, LOW);

  Ethernet.begin(mac);
  Udp.begin(9996);

  //Serial.begin(9600);
  /*while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }*/

  //Serial.println(Ethernet.localIP());

  while (!client.connect(server, 9999)) {}
  log("Connected to "); log(server);
  client.print("cbsZ\n"); //Transmit password

  // Enable DMX master interface and start transmitting
  dmx_master.enable();
  
  set_timer(&pingtime, 60000);
  set_timer(&reconnecttime, 3600000);
}

// the loop routine runs over and over again forever:
void loop()
{

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
      if(digitalRead(POWERCTRL_PIN)==HIGH) {
        client.print("UP\n");
      }
      else{
        client.print("DOWN\n");
      }
      i=2;
    }
    // Print DMX log
    else if(i==0 && (readchar&127) == 'L') {
      logdmx();
      i=2;
    }
    // Command to turn on power
    else if(i==0 && (readchar&127) == '1') {
      digitalWrite(POWERCTRL_PIN, HIGH);
      log("Power on\n");
      set_timer(&powerontime, 18000000);
      i=2;
    }
    // Command to turn off power
    else if(i==0 && (readchar&127) == '0') {
      digitalWrite(POWERCTRL_PIN, LOW);
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
    }

    if(i<2) {
      i++;
    }
    else {
      i = 0;
    }

    if (dataready) {
      dmx_master.setChannelValue (dmxchannel, dmxvalue );
      dmxvalues[dmxchannel-1] = dmxvalue;
      dataready = false;

      // Smoke output active, start timer
      if(dmxchannel==1 && dmxvalue>0) {
        set_timer(&smoketime, 10000);
        smokeon = true;
        //log("Smoke\n");
      }
      if(dmxchannel==1 && dmxvalue==0) {
        smokeon = false;
      }
    }
  }
  

  // Timer handlers
  if(timer(&pingtime)) {
    size_t retval;
    if(digitalRead(POWERCTRL_PIN)==HIGH) {
      retval = client.print("UP\n");
      log("UP\n");
    }
    else{
      retval = client.print("DOWN\n");
      log("DOWN\n");
    }
    if(!retval) {
      reconnect();
    }
    set_timer(&pingtime, 60000);
  }
  
  if(smokeon && timer(&smoketime)) {
    // Turn off smoke output
    dmx_master.setChannelValue(1, 0);
    dmxvalues[0] = 0;
    smokeon = false;
    log("Timer turned off smoke\n");
  }
  
  if(digitalRead(POWERCTRL_PIN)==HIGH && timer(&powerontime)) {
    digitalWrite(POWERCTRL_PIN, LOW);
    log("Timer turned off power\n");
  }
  
  if(timer(&reconnecttime)) {
    reconnect();
    set_timer(&reconnecttime, 3600000);
  }
  
  if (!client.connected()) {
    reconnect();
  }
  Ethernet.maintain();

}




void log(char msg[]) {
    //Serial.write(msg);
    Udp.beginPacket(server, 9996);
    Udp.write(msg);
    Udp.endPacket();
}

void logdmx() {
    char msg[25];
    for(int i=1; i<8; i++) {
      sprintf(msg, "Channel %d value %d\n", i, dmxvalues[i-1]);
      log(msg);
    }
}

// Reconnect on error
void reconnect() {
    log("Reconnecting...");
    client.stop();
    while (!client.connect(server, 9999)) {}
    client.print("cbsZ\n"); //Transmit password
    log("done\n");
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
