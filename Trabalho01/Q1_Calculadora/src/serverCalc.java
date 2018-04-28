import java.io.IOException;
import java.io.PrintStream;
import java.net.*;
import java.util.Scanner;

public class serverCalc {
	
	private static final int PORT = 5000; //Inline variable. It can't be changed.
	
	public static void main(String[] args) throws IOException {
				
		//Creating a port connection with server.
		ServerSocket calcServer = new ServerSocket(PORT);
		System.out.println("Port " + PORT + " opened...");
		
		//Server is always running
		while(true) {
			//Connecting with a client. Accept is a blocking method.
			Socket calcClient = calcServer.accept();
			System.out.println("New client connection...");
			
			//Creating a handle to client actions.
			clientHandle handle = new clientHandle(calcClient);
			
			//Putting it in a thread.
			Thread threadC = new Thread(handle);
			
			//Running thread.
			threadC.start();
		}		
	}
}
