package frsf.tibus.listener;



import javax.jms.Connection;
import javax.jms.DeliveryMode;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageConsumer;
import javax.jms.MessageListener;
import javax.jms.MessageProducer;
import javax.jms.ObjectMessage;
import javax.jms.Session;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import frsf.tibus.TibusServer;
import frsf.tibus.domain.BusPositionData;
import frsf.tibus.prediction.model.PredictionModel;

public class PositionDataListener implements MessageListener {
	
	private Session predictionSession;
	private boolean transacted=false;
	private int ackMode = Session.AUTO_ACKNOWLEDGE;
	private String requestQueueName = "busesPosition";
	private MessageProducer responseProducer;
	private PredictionModel modelo;
	private Logger logger;
	
	
	public PositionDataListener(Connection c, PredictionModel modeloPrediccion) {
		modelo = modeloPrediccion;
		logger = LoggerFactory.getLogger(TibusServer.class);
		
		try {						
			this.predictionSession = c.createSession(this.transacted, ackMode);
            Destination requestQueue = this.predictionSession.createQueue(requestQueueName);
            
            this.responseProducer = this.predictionSession.createProducer(null);
            this.responseProducer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
            
            MessageConsumer requestConsumer = this.predictionSession.createConsumer(requestQueue);
            requestConsumer.setMessageListener(this);
            
		} catch (JMSException e) {			
			e.printStackTrace();
		}
	}

	@Override
	public void onMessage(Message positionData) {
		
		if(positionData instanceof ObjectMessage)
		{
			try {
				Object position =  ((ObjectMessage)positionData).getObject();
				if(position instanceof BusPositionData)
				{
					logger.debug(((BusPositionData)position).toString());
					
					modelo.procesarNuevaPosicion((BusPositionData)position);
				}
			} catch (JMSException e) {
				e.printStackTrace();
			}
		}
		
	}

}
