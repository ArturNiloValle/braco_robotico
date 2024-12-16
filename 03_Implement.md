## Implementação

Após a etapa de concepção e design do sistema, foi iniciada a etapa de implementação do projeto. Para agilizar a implementação do projeto e testar as funcionalidades básicas, foi utilizado o Arduino UNO no lugar da ESP32, escolhida anteriormente no Design do projeto.

Inicialmente, foi instalada a IDE do Arduino necessários para o desenvolvimento do programa e foram realizados testes básicos utilizando apenas um Servo motor para validar seu funcionamento fora da estrutura do braço mecânico.
![image](https://github.com/user-attachments/assets/42e5e254-c90d-45c7-91f7-e305b79c4682)

Utilizando o código a seguir, foram realizados os primeros testes de funcionamento utilizando um único servo motor.
```c
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
```

#### Implementação com a estrutura do braço mecânico

Após a realização dos primeiros testes utilizando apenas um motor, foi iniciado o desenvolvimento do script para realizar o comamdo dos quatro servo motores da estrutura do braço mecânico escolhido. Durante o desenvolvimento, foram estudadas diferentes abordagem para o controle dos motores, chegando no script a seguir.

```c
#include <Servo.h>
#define DELAYT 300

/* #define baseInicial 90
#define baseEsquerda 180
#define baseDireita 0
#define eixo1Inicial 90
#define eixo2Inicial 90 */
#define garraAberta 180
#define garraFechada 0



// Definição dos pinos dos servos
const int basePin = 9;
const int eixo1Pin = 10;
const int eixo2Pin = 11;
const int garraPin = 12;

// Criando objetos para os servos
Servo base;
Servo eixo1;
Servo eixo2;
Servo garra;

// Posições dos servos
int baseInicial = 90;    // Posição inicial da base
int baseEsquerda = 180; // Posição da base para o lado esquerdo
int baseDireita = 0;    // Posição da base para o lado direito
int eixo1Inicial = 90;    // Posição inicial do eixo1
int eixo2Inicial = 90;    // Posição inicial do eixo2

// Variável para definir o lado que o braço se moverá (esquerda ou direita)
bool moverParaEsquerda = false;     // Se true, move para a esquerda. Se false, move para a direita.

bool movimentoConcluido = false; // Variável para garantir que o movimento será executado apenas uma vez

void setup() {
    Serial.begin(115200);
    roboInit();


    // Atraso para garantir que o braço esteja na posição inicial
    delay(2000);

    // Mensagem inicial
    if (moverParaEsquerda) {
    Serial.println("Movimento será para a esquerda.");
    } else {
    Serial.println("Movimento será para a direita.");
    }
}

void roboInit(){
   	 // Inicializando os servos
    base.attach(basePin);
    eixo1.attach(eixo1Pin);
    eixo2.attach(eixo2Pin);
    garra.attach(garraPin);

    // Movendo os servos para a posição inicial
    base.write(baseInicial);
    eixo1.write(eixo1Inicial);
    eixo2.write(eixo2Inicial);
    garra.write(garraFechada);
}

void loop() {
    if (!movimentoConcluido) {    // Verifica se o movimento já foi feito
    if (moverParaEsquerda) {
   	 // Movimento para o lado esquerdo
   	 moveParaEsquerda();
   	 delay(1000); // Espera 2 segundos na posição esquerda

   	 // Retorna para a posição inicial
   	 retornaPosicaoInicial();
   	 delay(1000); // Espera 2 segundos na posição inicial
    } else {
   	 // Movimento para o lado direito
   	 moveParaDireita();
   	 delay(1000); // Espera 2 segundos na posição direita

   	 // Retorna para a posição inicial
   	 retornaPosicaoInicial();
   	 delay(1000); // Espera 2 segundos na posição inicial
    }

    movimentoConcluido = true; // Marca que o movimento foi concluído
    Serial.println("Movimento concluído. Braço parado.");
    }

    // O loop fica vazio agora, o braço fica parado após a execução
    // Não há necessidade de continuar executando nada após o movimento
}

// Função que move o braço para o lado esquerdo
void moveParaEsquerda() {
    // Mover a base para o lado esquerdo lentamente
    moveLento(base, baseEsquerda);
    delay(DELAYT); // Pausa para garantir que o servo tenha tempo de se mover

    // Movimentar o braço (eixo1 e eixo2) para uma posição de trabalho lentamente
    moveLento(eixo1, 120);
    delay(DELAYT); // Pausa

    moveLento(eixo2, 60);
    delay(DELAYT); // Pausa

    // Fechar a garra lentamente
    moveLento(garra, garraFechada);
    delay(DELAYT); // Pausa
}

// Função que move o braço para o lado direito
void moveParaDireita() {
    // Mover a base para o lado direito lentamente
    moveLento(base, baseDireita);
    delay(DELAYT); // Pausa para garantir que o servo tenha tempo de se mover

    // Movimentar o braço (eixo1 e eixo2) para uma posição de trabalho lentamente
    moveLento(eixo1, 120);
    delay(DELAYT); // Pausa

    moveLento(eixo2, 120);
    delay(DELAYT); // Pausa

    // Abrir a garra lentamente
    moveLento(garra, garraAberta);
    delay(DELAYT); // Pausa
}

// Função que retorna os servos para a posição inicial
void retornaPosicaoInicial() {
    // Retorna os servos para a posição inicial
    moveLento(base, baseInicial);
    delay(DELAYT); // Pausa

    moveLento(eixo1, eixo1Inicial);
    delay(DELAYT); // Pausa

    moveLento(eixo2, eixo2Inicial);
    delay(DELAYT); // Pausa

    moveLento(garra, garraFechada); // Fecha a garra novamente
    delay(DELAYT); // Pausa
}

// Função para mover os servos de forma lenta
void moveLento(Servo& servo, int posicao) {
    int posAtual = servo.read();
    int passo = (posicao > posAtual) ? 1 : -1; // Determina o sentido do movimento

    for (int i = posAtual; i != posicao; i += passo) {
    servo.write(i);
    delay(20); // Atraso para fazer o movimento de forma mais suave
    }

    // Garantir que o servo chegue exatamente à posição final
    servo.write(posicao);
}
```
O programa realizado define as posições iniciais dos servos e os movimentos que ele precisa realizar para se mover para a direita ou para a esquerda utilizando funções com as posições específicas de cada motor. A decisão da direção ainda não é feita automaticamente e está sendo configurada manualmente para a realização dos testes.
A proxima etapa consiste em definir critérios para a decisão da direção do movimento e definir um procedimento de calibração para configurar as posições iniciais e finais de cada movimento.

### Prototipação de shield para arduino

Foi idealizada a prototipação de um shield para Arduino para facilitar e organizar as conexões entre os motores e a placa do Arduino. O shield foi desenvolvido no Altium e foram desenvolvidos o esquemático e layout da placa considerando a conexão com até quatro sevo motores.
Segue uma immagem do esquemático da placa

![image](https://github.com/user-attachments/assets/1fe51d05-125e-43ab-803c-7d04ff9e8aeb)

O Layout da placa foi baseado nos pinos de conexão do arduino e foram seguidos os espaçamentos dos conectores e suas posições para permitir o encaixe entre as duas placas como um shield. Os pinos de conexão com a placa do Arduino foram posicionados virados para a face inferior e os pinos de conexão com os motores para a face superior, facilitando a conexão e evitando mal contato.
Abaixo seguem as figuras ilustrando a placa desenvolvida e a conexão com o módulo do Arduino.

![image](https://github.com/user-attachments/assets/f2cdf7f5-9daf-4c10-a092-15f8c6b9f4d7)
![image](https://github.com/user-attachments/assets/3d41291f-37d8-4331-89d3-92f3082d6c30)

