#include <Servo.h>

#define DELAYT 300

// Definição dos pinos dos servos
const int basePin = 3;
const int eixo1Pin = 5;
const int eixo2Pin = 9;
const int garraPin = 11;

// Criando objetos para os servos
Servo base;
Servo eixo1;
Servo eixo2;
Servo garra;

// Posições iniciais dos servos
int basePos = 90;
int eixo1Pos = 90;
int eixo2Pos = 90;
int garraPos = 0;

void setup() {
    Serial.begin(115200);
    roboInit();
    Serial.println("Digite comandos (ex: B90 para mover base para 90 graus)");

    delay(500);
}

void roboInit(){
    // Inicializando os servos
    base.attach(basePin);
    eixo1.attach(eixo1Pin);
    eixo2.attach(eixo2Pin);
    garra.attach(garraPin);

    // Movendo os servos para a posição inicial
    moveLento(base, basePos);
    moveLento(eixo1, eixo1Pos);
    moveLento(eixo2, eixo2Pos);
    moveLento(garra, garraPos);

    delay(500);
}

void loop() {
    if (Serial.available() > 0) {
        String comando = Serial.readStringUntil('\n'); // Lê a linha inteira do Serial
        comando.trim(); // Remove espaços e quebras de linha

        if (comando.length() >= 2) {
            char motor = comando.charAt(0); // Primeiro caractere define qual motor mover
            int angulo = comando.substring(1).toInt(); // O restante é o ângulo desejado

            if (angulo >= 0 && angulo <= 180) { // Validação do ângulo
                switch (motor) {
                    case 'B': 
                        moveLento(base, angulo);
                        basePos = angulo;
                        Serial.print("Base movida para "); Serial.println(angulo);
                        break;
                    case 'M': 
                        moveLento(eixo1, angulo);
                        eixo1Pos = angulo;
                        Serial.print("Eixo medio movido para "); Serial.println(angulo);
                        break;
                    case 'S': 
                        moveLento(eixo2, angulo);
                        eixo2Pos = angulo;
                        Serial.print("Eixo superior movido para "); Serial.println(angulo);
                        break;
                    case 'G': 
                        moveLento(garra, angulo);
                        garraPos = angulo;
                        Serial.print("Garra movida para "); Serial.println(angulo);
                        break;
                    default:
                        Serial.println("Comando inválido! Use B, M, S ou G seguido do ângulo.");
                        break;
                }
            } else {
                Serial.println("Ângulo inválido! Insira um valor entre 0 e 180.");
            }
        }
    }
}

// Função para mover os servos de forma lenta
void moveLento(Servo& servo, int posicao) {
    int posAtual = servo.read();
    int passo = (posicao > posAtual) ? 1 : -1;

    for (int i = posAtual; i != posicao; i += passo) {
        servo.write(i);
        delay(10); // Movimento mais suave
    }

    servo.write(posicao);
}
