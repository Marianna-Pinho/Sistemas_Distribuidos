package AsynchronousChat;

import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

public class clientChat {
	
	public static final int PORT = 5000; //Inline variable. It can't be changed.
	
	public static void main(String[] args) throws IOException {
		
		String auxM = "", auxKb = "";
		
		//It creates a client socket, which communicates with 127.0.0.1 server.
		Socket chatClient = new Socket("127.0.0.1", PORT);
		System.out.println("Server connection stablished...");
		
		//It creates a Reader for the default entry (Keyboard).
		Scanner keyboard = new Scanner(System.in);
		
		//It creates a abstraction which relates the outputs to the socket channel.
		PrintStream output =  new PrintStream(chatClient.getOutputStream());
	
		//Creating a handle to client actions.
		handleInput handle = new handleInput(chatClient);
		
		//Putting it in a thread.
		Thread threadC = new Thread(handle);
		
		//Running thread.
		threadC.start();
		
		
		//Server is always running
		while(true) {
			//If server wants to talk something with client.
			if(keyboard.hasNextLine()) {
				//It reads something from keyboard.
				auxKb = keyboard.nextLine();
		
				//Sending message to server
				output.println(auxKb);
			}	
			
			//If message = stop, client wants close calculator.
			if((auxKb.compareTo("stop") == 0)) {
				break;	
			}				
		}
			
		//Ctrl+D
		System.out.println("Closing connection...");
		
		//Closing output to socket
		output.close();
		//Closing input from keyboard
		keyboard.close();
		//Closing socket
		chatClient.close();
	}
}

