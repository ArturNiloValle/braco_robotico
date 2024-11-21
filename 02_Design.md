# Design braço robótico  

Este projeto visa a criação de um sistema automatizado capaz de separar objetos com base na cor detectada por um sensor de cores, utilizando um braço robótico composto por 4 servomotores e controlado por um microcontrolador ESP32. O braço robótico será posicionado sobre uma esteira de transporte, realizando a coleta e a separação dos objetos de acordo com suas características cromáticas.

## Componentes do Sistema

### 1. Braço Robótico
O braço robótico é o elemento central do projeto e será responsável pelo movimento e pela manipulação dos objetos. O braço é projetado para realizar operações precisas de agarrar e posicionar objetos na esteira, utilizando um sistema de servomotores para movimentação.

-Estrutura do Braço: A estrutura do braço robótico pode ser construída com materiais leves, como acrílico ou alumínio, garantindo não só resistência, mas também leveza para movimentos rápidos e eficientes. O design pode seguir uma configuração de articulação humana, com um "ombro", "cotovelo" e "pulso" articulados para maior flexibilidade de movimento.
  
-Servomotores: O braço será composto por 4 servomotores, que são motores de precisão controlados eletronicamente. Os servomotores são ideais para este tipo de projeto devido à sua capacidade de mover-se com precisão a um ângulo específico. Eles serão distribuídos da seguinte forma:
  Base: Um servomotor responsável pelo movimento de rotação horizontal da base do braço, permitindo que ele gire ao redor de um ponto central.
Ombro: Um servomotor que permite o movimento do braço para cima e para baixo.
Cotovelo: Outro servomotor que ajuda a dobrar o braço em um movimento semelhante ao cotovelo humano, permitindo maior flexibilidade.
 Pinça: Um servomotor responsável pela abertura e fechamento de uma pinça, utilizada para agarrar e liberar os objetos. A pinça é projetada para ser leve, mas suficientemente robusta para manipular objetos com segurança.


![image](https://github.com/user-attachments/assets/2d4d90b2-7c57-4522-9653-122a91926fc7)


### 2. ESP32 (Microcontrolador)
O ESP32 é um microcontrolador poderoso e versátil que será o cérebro do sistema. Ele gerenciará as entradas e saídas do sistema, incluindo os dados recebidos do sensor de cores e os sinais enviados aos servomotores para controlar os movimentos do braço robótico.

O ESP32 é um microcontrolador de baixo custo, desenvolvido pela Espressif Systems, com Wi-Fi e Bluetooth integrados. Ele é amplamente utilizado em projetos de Internet das Coisas (IoT) e robótica devido ao seu baixo consumo de energia, alta performance de processamento e capacidade de comunicação sem fio. O ESP32 possui múltiplos núcleos de processamento, o que permite executar várias tarefas simultaneamente, tornando-o ideal para controlar dispositivos como sensores e atuadores.

![image](https://github.com/user-attachments/assets/6ff70b03-2086-4669-a352-1230bbce8ddb)


Funções no Projeto: O ESP32 será programado para receber os dados do sensor de cores, processá-los e, em seguida, gerar os comandos apropriados para os servomotores. Além disso, ele pode ser configurado para comunicação remota, caso seja necessário monitoramento ou controle externo via rede sem fio.


### 3. Sensor de Cores
O sensor de cores é um dispositivo eletrônico capaz de detectar e identificar a cor de um objeto. No nosso caso, o sensor será posicionado sobre a esteira de forma a capturar as cores dos objetos que passam por ele, enviando os dados de cor para o ESP32.

Sensores de cores como o TCS34725 operam utilizando LEDs e fotodiodos para capturar a luz refletida pelos objetos. Cada objeto refletirá a luz em diferentes intensidades, dependendo de sua cor. O sensor converte essas intensidades em sinais digitais ou analógicos, que são interpretados pelo ESP32.

![image](https://github.com/user-attachments/assets/73e496a2-8c0a-4a00-863f-54ad0b716d4d)

Utilização no Projeto: O sensor de cores identificará as cores dos objetos que estão sendo transportados pela esteira e enviará essa informação ao ESP32, que, por sua vez, determinará qual ação tomar com o braço robótico (por exemplo, mover para uma área de separação específica).


### 4. Esteira de Transporte
A esteira é um componente que transporta os objetos até o braço robótico, permitindo que o sistema funcione de maneira automatizada. A esteira pode ser motorizada e programada para operar a uma velocidade constante, garantindo que os objetos passam sob o sensor de cores de forma regular e ordenada.

![image](https://github.com/user-attachments/assets/7e14f051-c27d-4053-894a-347df4289f8e)

Integração com o Sistema: O ESP32 pode ser integrado à esteira para sincronizar os movimentos do braço com a chegada dos objetos, garantindo que o braço se posicione corretamente e faça a separação de maneira eficiente.


### 5. Fonte de Alimentação
Todos os componentes do sistema, incluindo o ESP32, os servomotores e o sensor de cores, exigem uma fonte de alimentação adequada. Como os servomotores consomem uma quantidade significativa de energia, é fundamental dimensionar corretamente a fonte de alimentação, garantindo que todos os dispositivos funcionem sem falhas ou quedas de energia.

## Funcionamento do Sistema

#### 1. Detecção de Cores:
   Quando um objeto passa sobre a esteira, o sensor de cores o "analisa" e identifica sua cor. Ele converte a intensidade da luz refletida pelas diferentes superfícies do objeto em sinais digitais que são enviados ao ESP32. Por exemplo, se o objeto for vermelho, o sensor detectará a predominância da cor vermelha. Esta informação já é publicada pelo sistema do sensor via MQTT e pode ser acessada pelo nosso sistema.

#### 2. Processamento e Decisão:   
O ESP32 processa as informações enviadas pelo sensor de cores e, com base em um conjunto de regras programadas, determina a ação que o braço robótico deve realizar. Por exemplo:
   - Se o objeto for vermelho, o braço deve pegá-lo e colocá-lo em uma caixa de cor vermelha.
   - Se o objeto for azul, o braço o moverá para uma área diferente.
   
#### 3. Movimentação do Braço Robótico:
   Após a decisão, o ESP32 envia os comandos aos servomotores, controlando os movimentos do braço robótico. Ele move a base, o ombro e o cotovelo para a posição correta, e se necessário, a pinça para agarrar os objetos em questão. A movimentação do braço é precisa, graças à utilização dos servomotores.

#### 4. Separação do Objeto:
   Com o objeto preso pela pinça, o braço se move até a área de separação correspondente e solta o item. Após isso, o braço retorna à posição inicial para aguardar o próximo objeto. Inicialmente será feito o teste apenas arrastando o objeto para a área determinada

#### 5. Ciclo Contínuo:
   O sistema continua o ciclo de captura e separação de objetos conforme eles passam pela esteira, com o ESP32 controlando toda a lógica e os movimentos do braço robótico.

### Desafios Potenciais

Precisão nos Movimentos: A precisão dos movimentos dos servomotores pode ser afetada por vários fatores, como calibração incorreta, limitações mecânicas ou resistência no movimento.
  
Velocidade do Sistema: A velocidade de resposta do sistema é um desafio. O tempo de detecção, processamento e movimentação pode limitar a eficiência do processo, especialmente se os objetos na esteira se moverem muito rapidamente.

Iluminação Variável: O sensor de cores pode ter dificuldades em condições de iluminação variáveis ou se os objetos tiverem cores muito semelhantes. Isso pode ser mitigado ajustando os parâmetros do sensor ou utilizando algoritmos de processamento de imagem mais sofisticados.


Este projeto oferece uma solução inovadora e eficiente para a separação automatizada de objetos com base na cor. A utilização de um ESP32 como controlador central, juntamente com servomotores e sensores de cores, cria um sistema robusto e altamente adaptável, que pode ser implementado em diversas áreas da indústria ou educação, promovendo a automação e o aprimoramento de processos.

### Fluxograma

![image](https://github.com/user-attachments/assets/5461c614-897e-4f66-bfb9-4a774792becc)

### Esquema de montagem

![image](https://github.com/user-attachments/assets/f2cd5547-3afe-4404-8b6c-ee840bc2f8e3)
