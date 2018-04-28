import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

import javax.naming.InvalidNameException;

public class clientHandle implements Runnable {
	
	//Creating a socket variable to receive a socket.
	Socket calcClient = null;
	
	//Creating calculator object reference.
	calculator calculation = new calculator();
	
	//Constructor
	clientHandle(Socket client){	
		//Getting socket client.
		calcClient = client;
	}
	
	
	//Main method
	public void run() {
		try {		
			//It creates a Reader for socket buffered messages.
			Scanner msg = new Scanner(calcClient.getInputStream());
			
			//Auxiliary string to receive messages from socket reader.
			String auxM  ="";
			
			//It creates a abstraction which relates the outputs to the socket channel.
			PrintStream output =  new PrintStream(calcClient.getOutputStream());
		
			//While there is something to read from socket.
			while(msg.hasNextLine()) {
				
				//Read what there is in socket channel.
				auxM = msg.nextLine();
				
				//If message = stop, client wants close calculator.
				if(auxM.compareTo("stop") == 0) {
					break;	
				}
				//If message doesn't have separators, no computation can be done.
				else if(!auxM.contains("-")) {
					output.println("Wrong format message");
					continue;
				}
			
				//Sending calculation result to the client.
				output.println(calculation.computing(auxM));
			}
		
			//stop message sent.
			System.out.println("Closing connection...");
			
			//Closing input from socket
			msg.close();
			//Closing output to socket
			output.close();
			//Closing socket
			calcClient.close();
			
		}catch(IOException | InvalidNameException e) {
			e.printStackTrace();
		}
	}

}
