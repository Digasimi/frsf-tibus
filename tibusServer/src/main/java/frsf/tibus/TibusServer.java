package frsf.tibus;

import javax.jms.Connection;
import javax.jms.DeliveryMode;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.MessageProducer;
import javax.jms.Session;

import org.apache.activemq.ActiveMQConnectionFactory;

import frsf.tibus.listener.PositionDataListener;
import frsf.tibus.listener.PredictionRequestListener;
import frsf.tibus.prediction.model.PredictionModel;
import frsf.tibus.prediction.model.averagespeed.AverageSpeedModel;

public class TibusServer {
	
	private ActiveMQConnectionFactory jmsConnectionFactory;
	private PredictionRequestListener predictionListener;
	private PositionDataListener positionListener;
	private PredictionModel modeloPrediccion;
	
	public static void main( String[] args ) throws InterruptedException
    {
        System.out.println("Servidor escuchando");

        new TibusServer();
        
    }
	
	public TibusServer() {
		setupServer();
	}
	
	
	private void setupServer() {
	
		String messageBrokerUrl = "tcp://localhost:61616";
		jmsConnectionFactory = new ActiveMQConnectionFactory(messageBrokerUrl);
	    Connection connection;
		
	    modeloPrediccion = new AverageSpeedModel();
	    
	    try {
			connection = jmsConnectionFactory.createConnection();
			connection.start();
			
			setPredictionListener(new PredictionRequestListener(connection, modeloPrediccion));
			setPositionListener(new PositionDataListener(connection, modeloPrediccion));
			
			
            
		} catch (JMSException e) {			
			e.printStackTrace();
		}
	    
	    
        

		
	}


	public PredictionRequestListener getPredictionListener() {
		return predictionListener;
	}


	public void setPredictionListener(PredictionRequestListener predictionListener) {
		this.predictionListener = predictionListener;
	}


	public PositionDataListener getPositionListener() {
		return positionListener;
	}


	public void setPositionListener(PositionDataListener positionListener) {
		this.positionListener = positionListener;
	}
	
}
