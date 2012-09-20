package frsf.tibus;

import javax.jms.Connection;
import javax.jms.DeliveryMode;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.MessageProducer;
import javax.jms.Session;

import org.apache.activemq.ActiveMQConnectionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import frsf.tibus.listener.PositionDataListener;
import frsf.tibus.listener.PredictionRequestListener;
import frsf.tibus.prediction.model.PredictionModel;
import frsf.tibus.prediction.model.averagespeed.AverageSpeedModel;
import frsf.tibus.util.SplashScreen;

public class TibusServer {
	
	private ActiveMQConnectionFactory jmsConnectionFactory;
	private PredictionRequestListener predictionListener;
	private PositionDataListener positionListener;
	private PredictionModel modeloPrediccion;
	
	public static void main( String[] args ) throws InterruptedException
    {
		new TibusServer();
        
    }
	
	public TibusServer() {
		Logger logger = LoggerFactory.getLogger(TibusServer.class);
	    
		logger.info(SplashScreen.getStartingSplashScreen());
		
		setupServer();
		
		logger.info(SplashScreen.getStartedSplashScreen());
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
