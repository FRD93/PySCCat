/********************************************************************************
* HARDWARE CONTROLLER SOFTWARE
* 
* Copyright (C) 2017  Francesco Roberto Dani
* Mail of the author: f.r.d@hotmail.it
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
********************************************************************************/

/********************************
* * SERIAL PORT OUTPUT VALUES * *
* "a1" -> value of sensor 1     *
* "a2" -> value of sensor 2     *
* "a3" -> value of sensor 3     *
* "a4" -> value of sensor 4     *
* "a5" -> value of sensor 5     *
* "mn" -> mean of all sensors   *
* "br" -> radius of barycentrum *
* "ba" -> angle of barycentrum  *
********************************/


// CONSTANTS
#define NUM_SENSORS 5
#define BAUD_RATE 9600

// VARIABLES
const int analog_ins[] = {A0, A1, A2, A3, A4};
const float min_[] = {0, 0, 0, 0, 20};
const float max_[] =  {670, 670, 670, 670, 670};
float pots[] = {0, 0, 0, 0, 0};
float mean, barycentrum;

// FUNCTION TO NORMALIZE A NUMBER GIVEN MIN AND MAX
float normalize(float val, float min_, float max_) {
  float normalized = (val - min_) / (max_ - min_);
  if (normalized < 0.0) normalized = 0.0;
  if (normalized > 1.0) normalized = 1.0;
  return  normalized;
}

// FUNCTION TO CONVERT FROM CARTESIAN TO POLAR COORDINATES
float* carToPol(float x, float y) {
  static float res[2];
  res[0] = sqrt(pow(x, 2) + pow(y, 2));
  res[1] = atan2(y, x);
  return res;
}

// FUNCTION TO CONVERT FROM POLAR TO CARTESIAN COORDINATES
float* polToCar(float r, float a) {
  float res[2];
  res[0] = r * cos(a);
  res[1] = r * sin(a);
  return res;
}

// FUNCTION TO READ SENSOR VALUES
void readSensors(void) {
  for (int i = 0; i < NUM_SENSORS; i++) {
    Serial.println(String("a") + (i+1));
    //Serial.println("a0");
    pots[i] = 1023.0 - (normalize(analogRead(analog_ins[i]), min_[i], max_[i]) * 1023);
    Serial.println(pots[i]);
  }
}

// FUNCTION TO COMPUTE THE MEAN OF ALL SENSORS
void sensorsMean(void) {
  float mean = 0;
  for (int i = 0; i < NUM_SENSORS; i++) mean = mean + pots[i];
  mean = mean / NUM_SENSORS;
  Serial.println("mn");
  Serial.println(mean);
}

// FUNCTION TO COMPUTE THE BARYCENTRUM OF THE SENSORS IN POLAR COORDINATES
void sensorsBarycentrum() {
  float pol_vec[NUM_SENSORS][2];
  float car_vec[NUM_SENSORS][2];
  float int_tri[3][2];
  float barycentrum[2];
  float* result;
  // Get sensor coordinates in polar form and convert them to cartesian coordinates
  for (int i = 0; i < NUM_SENSORS; i++) {
    pol_vec[i][0] = pots[i] / 1023.0; // normalize between 0.0 and 1.0
    pol_vec[i][1] = ( float(i) / NUM_SENSORS ) * ( 2 * PI ); // angles in radians
    car_vec[i][0] = pol_vec[i][0] * cos(pol_vec[i][1]);
    car_vec[i][1] = pol_vec[i][0] * sin(pol_vec[i][1]);
  }
  // Compute the barycentrums of the triangles composed by the sensors [0,1,2], [1,2,3], [2,3,4]
  for (int a = 0; a < 2; a++) {
    int_tri[0][a] = (car_vec[0][a] + car_vec[1][a] + car_vec[2][a]) / 3.0;
    int_tri[1][a] = (car_vec[1][a] + car_vec[2][a] + car_vec[3][a]) / 3.0; // [0,2,4]????
    int_tri[2][a] = (car_vec[2][a] + car_vec[3][a] + car_vec[4][a]) / 3.0;
  }
  // Compute the barycentrum of the triangle made from the previous three barycentrums
  barycentrum[0] = ( int_tri[0][0] + int_tri[1][0] + int_tri[2][0] ) / 3.0;
  barycentrum[1] = ( int_tri[0][1] + int_tri[1][1] + int_tri[2][1] ) / 3.0;
  // Convert barycentrum from cartesian to polar coordinates
  result = carToPol(barycentrum[0], barycentrum[1]);
  // Print barycentrum radius and angle to serial port
  Serial.println("br");
  Serial.println( result[0] * 1023.0 ); // rescale between 0.0 and 1023.0
  Serial.println("ba");
  Serial.println( abs( result[1] * 1023.0 / ( 2 * PI ) ) ); // rescale between 0.0 and 1023.0
}

// SETUP FUNCTION
void setup() {
  for (int i = 0; i < NUM_SENSORS; i++) pinMode(analog_ins[i], INPUT);
  Serial.begin(BAUD_RATE);
}

// LOOP FUNCTION
void loop() {
  readSensors();
  sensorsMean();
  sensorsBarycentrum();
}




