package Chat;

import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

public class clientHandle implements Runnable {
	
	//Creating a socket variable to receive a socket.
	Socket calcClient = null;
	
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
			
			//It creates a Reader for the default entry (Keyboard).
			Scanner keyboard = new Scanner(System.in);
			
			//Auxiliary string to receive messages from socket reader.
			String auxM  ="";
			
			//It creates a abstraction which relates the outputs to the socket channel.
			PrintStream output =  new PrintStream(calcClient.getOutputStream());
		
			//While there is something to read from socket.
			
			do {
				//If there is a message in socket channel, we read it.
				if(msg.hasNextLine()){
					System.out.println(msg.nextLine());
				}
						
				//It reads something from keyboard.
				auxM = keyboard.nextLine();
				
				//Sending message to server
				output.println(auxM);
				
				//If message = stop, client wants close calculator.
				if(auxM.compareTo("stop") == 0) {
					break;	
				}
				
			} while(keyboard.hasNextLine());
		
			//stop message sent.
			System.out.println("Closing connection...");
			
			//Closing input from keyboard
			keyboard.close();
			//Closing input from socket
			msg.close();
			//Closing output to socket
			output.close();
			//Closing socket
			calcClient.close();
			
		}catch(IOException e) {
			e.printStackTrace();
		}
	}

}
