package Chat;

import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

public class chatServer {
	
	private static final int PORT = 5000; //Inline variable. It can't be changed.
	
	public static void main(String[] args) throws IOException {
				
		//Creating a port connection with server.
		ServerSocket chatServer = new ServerSocket(PORT);
		System.out.println("Port " + PORT + " opened...");
					
		//It creates a Reader for the default entry (Keyboard).
		Scanner keyboard = new Scanner(System.in);
	
		//Auxiliary string to receive messages from socket reader.
		String auxM  ="", auxKb = "";
				
		//Connecting with a client. Accept is a blocking method.
		Socket chatClient = chatServer.accept();
		System.out.println("New client connection...");
		
		//It creates a Reader for socket buffered messages.
		Scanner msg = new Scanner(chatClient.getInputStream());
	
		//It creates a abstraction which relates the outputs to the socket channel.
		PrintStream output =  new PrintStream(chatClient.getOutputStream());
				
		
		//Server is always running
		while(true) {
			//If there is a message in socket channel, we read it.
			if(msg.hasNextLine()){
				System.out.println(msg.nextLine());
			}
				
			//If server wants to talk something with client.
			if(keyboard.hasNextLine()) {
				//It reads something from keyboard.
				auxKb = keyboard.nextLine();
		
				//Sending message to server
				output.println(auxKb);
			}
			
			//If message = stop, client wants close calculator.
			if((auxM.compareTo("stop") == 0) || (auxKb.compareTo("stop") == 0)) {
				break;	
			}				
		}
		
		//stop message sent.
		System.out.println("Closing connection...");
		
		//Closing server
		chatServer.close();
		//Closing input from keyboard
		keyboard.close();
		//Closing input from socket
		msg.close();
		//Closing output to socket
		output.close();
		//Closing socket
		chatClient.close();	
	}
}
