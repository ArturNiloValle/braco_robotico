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
const int basePin = 3;
const int eixo1Pin = 5;
const int eixo2Pin = 9;
const int garraPin = 11;

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