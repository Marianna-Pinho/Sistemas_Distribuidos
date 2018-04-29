Este programa implementa um chat não bloqueante, em que ambos os membros podem enviar e receber mensagens a qualquer instante.
Como as funções de leitura, tanto do teclado como do socket são bloqueantes, foi criada uma thread para tratar a leitura do socket, enquanto a leitura do teclado ficou dentro de um While, no processo principal.
