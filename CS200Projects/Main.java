package CS200Projects;    
//import CS200Projects.FibonacciCalculator; 


public class Main {
    public static void main(String[] args) {
        FibonacciCalculator calculator = new FibonacciCalculator();
        int result = calculator.calculateFibonacci(10);
        System.out.println("The 10th Fibonacci number is: " + result);
    }
}
