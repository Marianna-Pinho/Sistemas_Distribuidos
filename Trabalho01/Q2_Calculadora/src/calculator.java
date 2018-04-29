import java.text.DecimalFormat;
import java.util.*;

import javax.naming.InvalidNameException;

public class calculator {
	float operand1 = 0;
	float operand2 = 0;
	String operation = "";
	String result = "";
	
	//msg: OP1-OPERATION-OP2
	String computing(String msg) throws InvalidNameException {
		
		String[] auxString = msg.split("-");	
		
		operand1 = Float.parseFloat(auxString[0]);
		//System.out.println(operand1);
		
		operation = auxString[1];
		//System.out.println(operation);
	
		
		operand2 = Float.parseFloat(auxString[2]);
		//System.out.println(operand2);
		
			
		if(operation.compareTo("ADD") == 0) {
			
			result = "The sum is: " + operand1 + " + " + operand2 + " = " + new DecimalFormat("#0.00").format(operand1 + operand2);
			System.out.println(result);
		
		}else if(operation.compareTo("SUB") == 0) {
		
			result = "The sub is: " + operand1 + " - " + operand2 + " = " + new DecimalFormat("#0.00").format(operand1 - operand2);
			System.out.println(result);
		
		}else if(operation.compareTo("MULT") == 0) {
		
			result = "The mult is: " + operand1 + " * " + operand2 + " = " + new DecimalFormat("#0.00").format(operand1 * operand2);
			System.out.println(result);
		
		}else if(operation.compareTo("DIV") == 0) {
			if(operand2 != 0) {
		
				result = "The div is: " + operand1 + " / " + operand2 + " = " + new DecimalFormat("#0.00").format(operand1 / operand2);
				System.out.println(result);
			
			}else {
				result = "Denominator can't be 0";
			}
		}else {
			result = "Operation unknowed";
		}
		
		return result;
	}
	
	
//	public static void main(String[] args) {
//		calculator calc = new calculator();
//		
//		System.out.println(calc.computing("22-DIV-0"));
//	}
//	
}
