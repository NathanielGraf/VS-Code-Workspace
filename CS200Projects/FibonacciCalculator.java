package CS200Projects;

public class FibonacciCalculator {
    public int calculateFibonacci(int n) {
        if (n == 0 || n == 1) {
            return n;
        }
        return calculateFibonacci(n - 1) + calculateFibonacci(n - 2);
    }
}
