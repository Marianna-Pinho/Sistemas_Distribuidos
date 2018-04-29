package AsynchronousChat;

import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

public class serverChat {
	
	private static final int PORT = 5000; //Inline variable. It can't be changed.
	
	public static void main(String[] args) throws IOException {
		
		String auxKb = "";
		
		//Creating a port connection with server.
		ServerSocket chatServer = new ServerSocket(PORT);
		System.out.println("Port " + PORT + " opened...");
		
		//Server is always running
	
		//Connecting with a client. Accept is a blocking method.
		Socket calcClient = chatServer.accept();
		System.out.println("New client connection...");
		
		//Creating a handle to client actions.
		handleInput handle = new handleInput(calcClient);
		
		//Putting it in a thread.
		Thread threadC = new Thread(handle);
		
		//Running thread.
		threadC.start();
		
		//It creates a Reader for the default entry (Keyboard).
		Scanner keyboard = new Scanner(System.in);
				
		//It creates a abstraction which relates the outputs to the socket channel.
		PrintStream output =  new PrintStream(calcClient.getOutputStream());

		while(true) {
			if(keyboard.hasNextLine()) {
				//It reads something from keyboard.
				auxKb = keyboard.nextLine();
		
				//Sending message to server
				output.println(auxKb);
			}
			
			if(auxKb.compareTo("stop") == 0) {
				break;	
			}	
		}
	
	
		//Closing server
		chatServer.close();
		//Closing input from keyboard
		keyboard.close();
		//Closing output to socket
		output.close();
	}
}
		
		