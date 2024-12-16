#include <Servo.h>

//Variáveis
int Angulo;
bool direcao;

Servo servo;

void setup() {
  Serial.begin(115200);
  Serial.println("Controle de servo");
  servo.attach(9);
  Angulo = 1;
  direcao=1;
  delay(2000);
}


void loop() {
  if (direcao){
    Angulo=Angulo+20;
  }
  else
  {
    Angulo=Angulo-20;
  }
    if (Angulo>179){
    direcao=0;
    Angulo=179;
  }
  else if (Angulo<1){
    direcao=1;
    Angulo=1;
  }
  Serial.println(Angulo);
  servo.write(Angulo);

  int i = 0;
  for (i=0; i<=9; i++)
  {
    Angulo=i*20;
    Serial.println(Angulo);
    servo.write(Angulo);
    // servo.writeMicroseconds(1500);
    delay(1000);
  }
}
