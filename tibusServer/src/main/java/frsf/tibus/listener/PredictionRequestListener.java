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

import frsf.tibus.domain.PredictionRequest;
import frsf.tibus.modeloPrediccion.ModeloPrediccion;

public class PredictionRequestListener implements MessageListener {

	private Session predictionSession;
	private boolean transacted=false;
	private int ackMode = Session.AUTO_ACKNOWLEDGE;
	private String requestQueueName = "predictions.requests";
	private MessageProducer responseProducer;
	private ModeloPrediccion modelo;
	
	public PredictionRequestListener(Connection c, ModeloPrediccion modeloPrediccion) {
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
	public void onMessage(Message request) {
		ObjectMessage response;
		try {
			response = this.predictionSession.createObjectMessage();
			response.setObject(this.modelo.obtenerPrediccion(new PredictionRequest(new Integer(1),"s")));
			
			response.setJMSCorrelationID(request.getJMSCorrelationID());

            this.responseProducer.send(request.getJMSReplyTo(), response);
		} catch (JMSException e) {			
			e.printStackTrace();
		}
		catch (Exception e) {
			e.printStackTrace();
		}		
	}

}
