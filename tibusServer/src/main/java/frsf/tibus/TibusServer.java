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
import frsf.tibus.modeloPrediccion.ModeloPrediccion;
import frsf.tibus.modeloPrediccion.test.ModeloTest;

public class TibusServer {
	
	private ActiveMQConnectionFactory jmsConnectionFactory;
	private PredictionRequestListener predictionListener;
	private PositionDataListener positionListener;
	private ModeloPrediccion modeloPrediccion;
	
	public TibusServer() {
		setupServer();
	}
	
	
	private void setupServer() {
	
		String messageBrokerUrl = "tcp://localhost:61616";
		jmsConnectionFactory = new ActiveMQConnectionFactory(messageBrokerUrl);
	    Connection connection;
		
	    modeloPrediccion = new ModeloTest();
	    
	    try {
			connection = jmsConnectionFactory.createConnection();
			connection.start();
			
			predictionListener = new PredictionRequestListener(connection, modeloPrediccion);
			positionListener = new PositionDataListener(connection, modeloPrediccion);
			
			
            
		} catch (JMSException e) {			
			e.printStackTrace();
		}
	    
	    
        

		
	}
	
}
