package AsynchronousChat;

import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

import javax.naming.InvalidNameException;

public class handleInput implements Runnable {
	
	//Creating a socket variable to receive a socket.
	Socket chatClient = null;
		
	//Constructor
	handleInput(Socket client){	
		//Getting socket client.
		chatClient = client;
	}
	
	
	//Main method
	public void run() {
		try {		
			//It creates a Reader for socket buffered messages.
			Scanner msg = new Scanner(chatClient.getInputStream());
			
			//Auxiliary string to receive messages from socket reader.
			String auxM  ="";
					
			//While there is something to read from socket.
			while(true) {	
				if(msg.hasNextLine()) {
					//Read what there is in socket channel.
					auxM = msg.nextLine();
					
					//If message = stop, client wants close calculator.
					if(auxM.compareTo("stop") == 0) {
						break;	
					}
				
					//Sending calculation result to the client.
					System.out.println(auxM);
				}
			}
		
			//stop message sent.
			System.out.println("Closing connection...");
			
			//Closing input from socket
			msg.close();
			//Closing socket
			chatClient.close();
			
		}catch(IOException e) {
			e.printStackTrace();
		}
	}

}

