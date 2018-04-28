package Chat;

import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

public class chatClient {
	
	public static final int PORT = 5000; //Inline variable. It can't be changed.
	
	public static void main(String[] args) throws IOException {
		
		String auxM = "", auxKb = "";
		
		//It creates a client socket, which communicates with 127.0.0.1 server.
		Socket calcClient = new Socket("127.0.0.1", PORT);
		System.out.println("Server connection stablished...");
		
		//It creates a Reader for the default entry (Keyboard).
		Scanner keyboard = new Scanner(System.in);
		
		//It creates a abstraction which relates the outputs to the socket channel.
		PrintStream output =  new PrintStream(calcClient.getOutputStream());
		
		//It creates a Reader for socket buffered messages.
		Scanner msg = new Scanner(calcClient.getInputStream());

		
		//Server is always running
		while(true) {
			//If server wants to talk something with client.
			if(keyboard.hasNextLine()) {
				//It reads something from keyboard.
				auxKb = keyboard.nextLine();
		
				//Sending message to server
				output.println(auxKb);
			}
			
			//If there is a message in socket channel, we read it.
			if(msg.hasNextLine()){
				System.out.println(msg.nextLine());
			}			
			
			//If message = stop, client wants close calculator.
			if((auxM.compareTo("stop") == 0) || (auxKb.compareTo("stop") == 0)) {
				break;	
			}				
		}
		
		
		//Ctrl+D
		System.out.println("Closing connection...");
		
		//Closing input from socket
		msg.close();
		//Closing output to socket
		output.close();
		//Closing input from keyboard
		keyboard.close();
		//Closing socket
		calcClient.close();
	}
}
