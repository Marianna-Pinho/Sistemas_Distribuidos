Calculadora que implementa as quatro operações básicas.
Ela consiste em um servidor multithread, ou seja, capaz de atender vários clientes.

1) Protocolo: as operações devem ser mandadas no formato "OPERANDO01-OPERAÇÃO-OPERANDO02", em que OPERAÇÃO deve ser {ADD, SUB, MULT, DIV}.
2) Tratamento: ela trata a) Divisão por zero.
			 b) Operação desconhecida.
			 c) Strings que não tem o símbolo "-".

3) Não trata: ela não trata a) Operandos escritos incorretamente.
			    b) Strings que tem "-", mas não estão na forma do protocolo.
