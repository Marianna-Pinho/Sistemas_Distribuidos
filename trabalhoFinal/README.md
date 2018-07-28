This is the final project of Distributed Systems course. 
We implemented a calendar of events, using Python programming language, RabbitMQ broker and Remote Procedure Call (RPC) method of interaction.
We are storing the data into two files, one of them just to user information, and the other to event information. 
It's allowed create several server and clients at the same time, because RABBITMQ provides decoupling of time and space. All the servers need read and write data using the same files, because they must be syncronized.
All data exchanged among clients and servers must be in JSON format. So, they are serialized before sending and desserialized when received.

#OBS: we are assuming that the user follows all the rules. So, we are not treating when the user writes something that isn't in the asked format.
