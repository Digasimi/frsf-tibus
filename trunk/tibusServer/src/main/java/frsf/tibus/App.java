package frsf.tibus;


public class App 
{
    public static void main( String[] args ) throws InterruptedException
    {
        System.out.println("Servidor escuchando");

        new TibusServer();
        
    }
}
