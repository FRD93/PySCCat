#define ANALOG_IN_1 A0
#define ANALOG_IN_2 A1
#define ANALOG_IN_3 A2
#define ANALOG_IN_4 A3
#define ANALOG_IN_5 A4

float v1, v2, v3, v4, v5, min1=512, min2=512, min3=512, min4=512, min5=512, max1=512, max2=512, max3=512, max4=512, max5=512;

void setup() {
  // put your setup code here, to run once:
  
  pinMode(ANALOG_IN_1, INPUT);
  pinMode(ANALOG_IN_2, INPUT);
  pinMode(ANALOG_IN_3, INPUT);
  pinMode(ANALOG_IN_4, INPUT);
  pinMode(ANALOG_IN_5, INPUT);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
    
    v1 = analogRead(ANALOG_IN_1);
    if(v1 < min1) min1 = v1;
    if(v1 > max1) max1 = v1;

    v2 = analogRead(ANALOG_IN_2);
    if(v2 < min2) min2 = v2;
    if(v2 > max2) max2 = v2;

    v3 = analogRead(ANALOG_IN_3);
    if(v3 < min3) min3 = v3;
    if(v3 > max3) max3 = v3;

    v4 = analogRead(ANALOG_IN_4);
    if(v4 < min4) min4 = v4;
    if(v4 > max4) max4 = v4;

    v5 = analogRead(ANALOG_IN_5);
    if(v5 < min5) min5 = v5;
    if(v5 > max5) max5 = v5;

    Serial.println("POT 1:");
    Serial.println("min:");
    Serial.println(min1);
    Serial.println("max:");
    Serial.println(max1);

    Serial.println("POT 2:");
    Serial.println("min:");
    Serial.println(min2);
    Serial.println("max:");
    Serial.println(max2);

    Serial.println("POT 3:");
    Serial.println("min:");
    Serial.println(min3);
    Serial.println("max:");
    Serial.println(max3);

    Serial.println("POT 4:");
    Serial.println("min:");
    Serial.println(min4);
    Serial.println("max:");
    Serial.println(max4);

    Serial.println("POT 5:");
    Serial.println("min:");
    Serial.println(min5);
    Serial.println("max:");
    Serial.println(max5);
    
    
    
}
