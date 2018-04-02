#define ANALOG_IN_1 A0
#define ANALOG_IN_2 A1
#define ANALOG_IN_3 A2
#define ANALOG_IN_4 A3
#define ANALOG_IN_5 A4

float value;

float min1=0, min2=0, min3=0, min4=0, min5=20;
float max1=670,max2=670,max3=670,max4=670,max5=670;

float normalize(float val, float min_, float max_) {
  float normalized = (val - min_) / (max_ - min_);
  if(normalized < 0.0) normalized = 0.0;
  if(normalized > 1.0) normalized = 1.0;
  return  normalized;
}

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
    Serial.println("a1");
    value = 1023.0 - (normalize(analogRead(ANALOG_IN_1), min1, max1) * 1023);
    Serial.println(value);
    
    Serial.println("a2");
    value = 1023.0 - (normalize(analogRead(ANALOG_IN_2), min2, max2) * 1023);
    Serial.println(value);
    
    Serial.println("a3");
    value = 1023.0 - (normalize(analogRead(ANALOG_IN_3), min3, max3) * 1023);
    Serial.println(value);
    
    Serial.println("a4");
    value = 1023.0 - (normalize(analogRead(ANALOG_IN_4), min4, max4) * 1023);
    Serial.println(value);
    
    Serial.println("a5");
    value = 1023.0 - (normalize(analogRead(ANALOG_IN_5), min5, max5) * 1023);
    Serial.println(value);
    
}




