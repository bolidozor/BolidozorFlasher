#include <Adafruit_NeoPixel.h>
#include <Adafruit_TinyUSB.h>
#include <WebSocketsClient.h>
#include <WiFi.h>
#include <Arduino_MultiWiFi.h>
#include "LittleFS.h"

#define PIN 0
#define NUMPIXELS 64


#define MAX_NETWORKS 10
#define SSID_MAX_LEN 32
#define PASS_MAX_LEN 64
#define CONFIG_FILE "/wifi_config.txt"

// Struktura pro uložení WiFi konfigurací
struct WiFiConfig {
  char ssid[SSID_MAX_LEN];
  char password[PASS_MAX_LEN];
  bool enabled;
};

WiFiConfig wifiConfigs[MAX_NETWORKS];
int savedNetworks = 0;


Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

WebSocketsClient webSocket;
MultiWiFi multi;


uint8_t counter = 0;
uint32_t last = 0;
float light = 1;

void setup() {

  Serial.begin(115200);

  pixels.begin();
  pixels.clear();
  pixels.show();


  for(int n=0; n<5; n++){
  for (int i = 0; i < NUMPIXELS; i++) {
    uint8_t red = 255;
    uint8_t green = 255;
    uint8_t blue = 0;
    pixels.setPixelColor(i, pixels.Color(red, green, blue));
    pixels.show();
    delay(1);
  }
  delay(200);
  for (int i = 0; i < NUMPIXELS; i++) {
    uint8_t red = 0;
    uint8_t green = 0;
    uint8_t blue = 0;
    pixels.setPixelColor(i, pixels.Color(red, green, blue));
    pixels.show();
    delay(1);
  }
  delay(200);
  }
  


  last = millis();

  LittleFS.begin();
  loadConfig();

  //animateStart();

  Serial.println("WiFi initialization..");

  multi.add("Bolidozor", "BolidozorLan");
  for (int i = 0; i < MAX_NETWORKS; i++) {
    if (wifiConfigs[i].enabled && strlen(wifiConfigs[i].ssid) > 0) {
      multi.add(wifiConfigs[i].ssid, wifiConfigs[i].password);
      Serial.printf("Added network: %s\n", wifiConfigs[i].ssid);
    }
  }
  
  Serial.print("Connecting to WiFi network...");

  if (multi.run() == WL_CONNECTED) {
    Serial.println("Connected to network");
    Serial.println(WiFi.SSID());
    Serial.println(WiFi.localIP());
  }

  while (!WiFi.isConnected()){
      serialLoop();
  }

    Serial.println("Connected to Wifi, Connecting to server.");

    webSocket.setExtraHeaders("FLASHER" );
    webSocket.begin("rtbolidozor.astro.cz", 80, "/ws/");
    //webSocket.beginSSL("rtbolidozor.astro.cz", 433, "/ws/");

    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(1000);
    webSocket.enableHeartbeat(5000, 500, 5);
      
    Serial.println("Connected to websocket!");
    //animateConnected();
  
    for(int n=0; n<5; n++){
    for (int i = 0; i < NUMPIXELS; i++) {
      uint8_t red = 255;
      uint8_t green = 100;
      uint8_t blue = 0;
      pixels.setPixelColor(i, pixels.Color(red, green, blue));
      pixels.show();
      delay(1);
    }
    delay(200);
    for (int i = 0; i < NUMPIXELS; i++) {
      uint8_t red = 100;
      uint8_t green = 0;
      uint8_t blue = 0;
      pixels.setPixelColor(i, pixels.Color(red, green, blue));
      pixels.show();
      delay(1);
    }
    delay(200);
  }
  
}


void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
	switch(type) {
		case WStype_DISCONNECTED:
			Serial.printf("[WSc] Disconnected!\n");
			break;
		case WStype_CONNECTED: {
			Serial.printf("[WSc] Connected to url: %s\n", payload);

			// send message to server when Connected
			webSocket.sendTXT("Connected");
		}
			break;
		case WStype_TEXT:
			Serial.printf("[WSc] get text: %s\n", payload);
      last = millis();
      light += 1;

			// send message to server
			// webSocket.sendTXT("message here");
			break;
		case WStype_BIN:
			Serial.printf("[WSc] get binary length: %u\n", length);
			hexdump(payload, length);

			break;
        case WStype_PING:
            // pong will be send automatically
            Serial.printf("[WSc] get ping\n");
            break;
        case WStype_PONG:
            // answer to a ping we send
            Serial.printf("[WSc] get pong\n");
            break;
    }

}



void loop() {

  if(!WiFi.isConnected()){
    Serial.println("Disconnected...");
    if (multi.run() == WL_CONNECTED) {
      Serial.println("Connected to network");
      Serial.println(WiFi.SSID());
      Serial.println(WiFi.localIP());
    }
  } else {
    webSocket.loop();
  }

  serialLoop();

  if(light > 3){
      light = 3;
  } else if (light > 1){
      light -= 0.004;
  } else if (light > 0){
      light -= 0.0008;
  }
  
  float real_light = light;
  if(real_light<0){
  real_light=0;
  } 
  if(real_light>1){
    real_light=1;
    }

  for (int i = 0; i < NUMPIXELS; i++) {
    uint8_t red = int(real_light*253+2);
    uint8_t green = int((light > 1) ? ((light-1)/2*128) : 0);
    uint8_t blue = green;
    pixels.setPixelColor(i, pixels.Color(red, green, blue));
  }
  pixels.show();
}

void serialLoop(){
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.equalsIgnoreCase("conf")) {
      showMenu();
    } else {
      Serial.println("Unknown cmd. Try 'conf' for configuration.");
      last = millis();
      light += 1;
    }
  }

}


void showMenu() {
  showHelp();

  while (true) {
    if (Serial.available()) {
      String command = Serial.readStringUntil('\n');
      command.trim();

      if (command.equalsIgnoreCase("save")) {
        saveConfig();
        Serial.println("Configuration saved.");
      } else if (command.equalsIgnoreCase("show")) {
        for (int i = 0; i < MAX_NETWORKS; i++) {
          if (strlen(wifiConfigs[i].ssid) > 0) {
            Serial.printf("W%d: SSID: %s, Password: %s, Active: %s\n", i, wifiConfigs[i].ssid, wifiConfigs[i].password, wifiConfigs[i].enabled ? "YES" : "NE");
          }
        }
      } else if (command.equalsIgnoreCase("reboot")) {
        rebootDevice();
      } else if (command.equalsIgnoreCase("help")) {
        showHelp();
      } else if (command.equalsIgnoreCase("exit")) {
        Serial.println("Leaving configuration file.");
        break;
      } else {
        handleConfigCommand(command);
      }
    }
  }
}

void handleConfigCommand(const String& command) {
  if (command.startsWith("W") && command.length() > 3) {
    int index = command.substring(1, 2).toInt();
    if (index < 0 || index >= MAX_NETWORKS) {
      Serial.println("Invalid network number (0-9). Try it again.");
      return;
    }

    if (command.substring(2, 3) == "S") {
      String ssid = command.substring(4);
      strncpy(wifiConfigs[index].ssid, ssid.c_str(), SSID_MAX_LEN);
      wifiConfigs[index].ssid[SSID_MAX_LEN - 1] = '\0';
      Serial.printf("SSID for network %d set to: %s\n", index, wifiConfigs[index].ssid);
    } else if (command.substring(2, 3) == "P") {
      String password = command.substring(4);
      strncpy(wifiConfigs[index].password, password.c_str(), PASS_MAX_LEN);
      wifiConfigs[index].password[PASS_MAX_LEN - 1] = '\0';
      Serial.printf("Password for network %d set.\n", index);
    } else if (command.substring(2, 3) == "E") {
      int enabled = command.substring(4).toInt();
      wifiConfigs[index].enabled = (enabled == 1);
      Serial.printf("Network %d %s.\n", index, wifiConfigs[index].enabled ? "enabled" : "disabled");
    } else {
      Serial.println("Unknown command. Use W<X>S=, W<X>P= or W<X>E=.");
    }
    } else {
    Serial.println("Unknown command. Use W<X>S=, W<X>P= or W<X>E=.");
  }
}

void saveConfig() {
  File file = LittleFS.open(CONFIG_FILE, "w");
  if (!file) {
    Serial.println("Error: Saving config!");
    return;
  }

  for (int i = 0; i < MAX_NETWORKS; i++) {
    if (strlen(wifiConfigs[i].ssid) > 0) {
      file.printf("W%dS=%s\n", i, wifiConfigs[i].ssid);
      file.printf("W%dP=%s\n", i, wifiConfigs[i].password);
      file.printf("W%dE=%d\n", i, wifiConfigs[i].enabled);
    }
  }
  file.close();
}

void loadConfig() {
  File file = LittleFS.open(CONFIG_FILE, "r");
  if (!file) {
    Serial.println("Configuration file not found. Using default values.");
    return;
  }

  while (file.available()) {
    String line = file.readStringUntil('\n');
    line.trim();
    handleConfigCommand(line);
  }
  file.close();
}

void rebootDevice() {
  Serial.println("Restarting device...");
  //delay(1000);
  //ESP.restart();
}

void showHelp() {
  Serial.println("\n============================");
  Serial.println(" WiFi Configuration Menu ");
  Serial.println("============================");
  Serial.println("W<X>S=<ssid> - Set SSID for network X (0-9)");
  Serial.println("W<X>P=<password> - Set password for network X (0-9)");
  Serial.println("W<X>E=<0/1> - Enable/disable network X (0-9)");
  Serial.println("save - Save configuration to file");
  Serial.println("show - Show current network settings");
  Serial.println("reboot - Restart the device");
  Serial.println("help - Show help");
  Serial.println("exit - Exit configuration");
  Serial.println("============================\n");
}
