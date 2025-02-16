#include <Servo.h>
#include <math.h>
#include "QueueArray.h"  // Biblioteca da fila

#define DELAYT 10        // Tempo entre cada passo de movimento
#define MAX_FILA 10      // Capacidade da fila

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

// Posições atuais dos servos
int basePos = 0;
int eixo1Pos = 20;
int eixo2Pos = 90;
int garraPos = 0;

// Criando buffer de comandos com ponteiros char*
QueueArray<char*> comandoQueue(MAX_FILA);

void setup() {
    Serial.begin(115200);
    roboInit();
    delay(500);
    Serial.println("Digite comandos (ex: B90 M45 S120 G90) ou coordenadas X, Y, Z (terminando com ENTER).");
}

void roboInit() {
    base.attach(basePin);
    eixo1.attach(eixo1Pin);
    eixo2.attach(eixo2Pin);
    garra.attach(garraPin);

    moveLentoSimultaneo(basePos, eixo1Pos, eixo2Pos, garraPos);
    delay(500);
}

void loop() {
    // 1) Verifica se há dados na Serial
    if (Serial.available() > 0) {
        // 2) Lê uma linha inteira até '\n'
        String line = Serial.readStringUntil('\n');
        line.trim(); // Remove espaços e \r extras

        // 3) Se a linha não estiver vazia, armazena na fila
        if (line.length() > 0) {
            if (!comandoQueue.isFull()) {
                // Aloca memória e copia a linha
                char *novoComando = (char*)malloc(line.length() + 1);
                strcpy(novoComando, line.c_str());
                
                comandoQueue.push(novoComando);  
                Serial.print("Comando armazenado: ");
                Serial.println(novoComando);
            } else {
                Serial.println("Fila de comandos cheia! Aguarde o processamento.");
            }
        }
    }

    // 4) Se a fila não estiver vazia, processa o próximo comando
    if (!comandoQueue.isEmpty()) {
        char* comandoAtual = comandoQueue.pop();  // Retira um comando da fila
        processarComando(comandoAtual);
        free(comandoAtual);  // Libera memória alocada após uso
    }
}

// Processa e interpreta o comando (ex: "B90 M0 S180 G180")
void processarComando(const char* comando) {
    int novaBase = basePos, novoM = eixo1Pos, novoS = eixo2Pos, novaGarra = garraPos;
    int pos = 0;

    while (comando[pos] != '\0') {
        char motor = comando[pos++];
        int angulo = 0;

        // Lê o ângulo correspondente
        while (comando[pos] >= '0' && comando[pos] <= '9') {
            angulo = angulo * 10 + (comando[pos] - '0');
            pos++;
        }

        // Valida e atualiza os ângulos
        if (angulo >= 0 && angulo <= 180) {
            switch (motor) {
                case 'B': novaBase = angulo;   break;
                case 'M': novoM   = angulo;   break;
                case 'S': novoS   = angulo;   break;
                case 'G': novaGarra = angulo; break;
                default:
                    Serial.print("Comando inválido: ");
                    Serial.println(motor);
                    return;
            }
        } else {
            Serial.print("Ângulo inválido: ");
            Serial.println(angulo);
            return;
        }

        // Pula espaços e continua até fim da string
        while (comando[pos] == ' ') pos++;
    }

    // Movimenta todos os motores simultaneamente
    moveLentoSimultaneo(novaBase, novoM, novoS, novaGarra);
}

// Move os motores de forma simultânea e suave
void moveLentoSimultaneo(int novaBase, int novoM, int novoS, int novaGarra) {
    int passoBase = (novaBase > basePos) ? 1 : -1;
    int passoM    = (novoM    > eixo1Pos) ? 1 : -1;
    int passoS    = (novoS    > eixo2Pos) ? 1 : -1;
    int passoG    = (novaGarra> garraPos) ? 1 : -1;

    int maiorDiferenca = max(abs(novaBase - basePos),
                          max(abs(novoM - eixo1Pos),
                          max(abs(novoS - eixo2Pos),
                              abs(novaGarra - garraPos))));

    for (int i = 0; i <= maiorDiferenca; i++) {
        if (basePos != novaBase)    base.write(basePos += passoBase);
        if (eixo1Pos != novoM)      eixo1.write(eixo1Pos += passoM);
        if (eixo2Pos != novoS)      eixo2.write(eixo2Pos += passoS);
        if (garraPos != novaGarra)  garra.write(garraPos += passoG);
        delay(DELAYT);
    }

    basePos   = novaBase;
    eixo1Pos  = novoM;
    eixo2Pos  = novoS;
    garraPos  = novaGarra;

    Serial.print("Movimento concluído -> Base: "); Serial.print(basePos);
    Serial.print(" | M: "); Serial.print(eixo1Pos);
    Serial.print(" | S: "); Serial.print(eixo2Pos);
    Serial.print(" | G: "); Serial.println(garraPos);
}
