## Testes realizados e implementações finais

Após a primeira implementação, o prototipo foi testado utilizando o shield e foi ajustado o portmap para o funcionamento correto.

![image](https://github.com/user-attachments/assets/95035ea5-10dc-44a4-be5a-47c907b548d3)


A partir do código original, foi criado um protocolo para movimentação dos servo motores via outro dispositivo. O código tem a seguinte estrutura:

AXXX

Sendo:


- A - Código do motor a ser movido: B = Base; M = Primeiro eixo (Médio); S = Segundo eixo (Superior); G = Garra;
- XXX - Ângulo a ser configurado (0 a 180)

Sendo que há também a possibilidade de recebimento de multiplos comandos simultâneamente, para a movimentação de mais de um motor, como por exemplo:

B90 \\movimenta apenas a base para 90 graus

B90 M120 S90 \\ Movimenta a base, o primeiro e o segundo eixo para os respectivos angulos.

A partir desta ideia, foi criada uma função de processamento para reconhecer os códigos recebidos e executar os comandos:
```c
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

```
Além disso, também foi implementada a leitura de dados da interface serial, para permitir o envio de comandos e verificar o funcionamento correto dos motores, tanto individuais, como em conjunto.
Para a execução dos comandos, foi implementada uma função para mover os motores em passos peguenos para que o movimento seja realizado de forma igualitária entre todos os motores, até que o movimento seja concluido.
```c
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
```
Foram realizadas estas implementações e testados alguns comandos pelo monitor serial da interface do Arduino e funcionaram normalmente.

## Script para envio de comandos
Para melhorar a interação com o braço mecânico e realizar a verificação da resposta aos comandos, foi desenvolvido uma janela em python para realizar a conexão com o braço via serial
e enviar os comandos. A janela conta com uma aba de controle manual, onde cada modor pode ser movimentado individualmente, sendo possível salvar as posições em um arquivo.
Também há uma aba que faz a leitura de um arquivo e realiza o envio de todos os comandos pela serial.

