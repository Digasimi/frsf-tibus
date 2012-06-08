package frsf.tibus.listener;

import java.util.ArrayList;

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

import frsf.tibus.domain.Posicion;
import frsf.tibus.modeloPrediccion.ModeloPrediccion;

public class PositionDataListener implements MessageListener {
	
	private Session predictionSession;
	private boolean transacted=false;
	private int ackMode = Session.AUTO_ACKNOWLEDGE;
	private String requestQueueName = "busesPosition";
	private MessageProducer responseProducer;
	private ModeloPrediccion modelo;
	
	public PositionDataListener(Connection c, ModeloPrediccion modeloPrediccion) {
		modelo = modeloPrediccion;
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
				ArrayList<Posicion> positions = (ArrayList<Posicion>) ((ObjectMessage)positionData).getObject();
				if(positions != null)
				{
					modelo.procesarNuevasPosiciones(positions);
				}
			} catch (JMSException e) {
				e.printStackTrace();
			}
		}
		
	}

}
