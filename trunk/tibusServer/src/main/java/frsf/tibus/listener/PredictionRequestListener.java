package frsf.tibus.listener;

import java.io.ByteArrayInputStream;
import java.io.StringWriter;

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
import javax.jms.TextMessage;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;

import frsf.tibus.domain.PredictionRequest;
import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.prediction.model.PredictionModel;

public class PredictionRequestListener implements MessageListener {

	private Session predictionSession;
	private boolean transacted=false;
	private int ackMode = Session.AUTO_ACKNOWLEDGE;
	private String requestQueueName = "predictions.requests";
	private MessageProducer responseProducer;
	private PredictionModel modelo;
	
	private JAXBContext jc;
	private Marshaller m;
	private Unmarshaller um;;
	
	public PredictionRequestListener(Connection c, PredictionModel modeloPrediccion) {
		modelo = modeloPrediccion;
		try {						
			this.predictionSession = c.createSession(this.transacted, ackMode);
            Destination requestQueue = this.predictionSession.createQueue(requestQueueName);
            
            this.responseProducer = this.predictionSession.createProducer(null);
            this.responseProducer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
            
            MessageConsumer requestConsumer = this.predictionSession.createConsumer(requestQueue);
            requestConsumer.setMessageListener(this);
            
            try {
				jc = JAXBContext.newInstance("frsf.tibus.domain");
				m = jc.createMarshaller();
	        	um = jc.createUnmarshaller();	           
			} catch (JAXBException e) {
				e.printStackTrace();
			}
        	
		} catch (JMSException e) {			
			e.printStackTrace();
		}
	}
	
	@Override
	public void onMessage(Message request) {
		try {
			if(request instanceof ObjectMessage)
			{
				
				
				ObjectMessage response = this.predictionSession.createObjectMessage();
				
				Object predictionRequest = ((ObjectMessage)request).getObject();
				
				if(predictionRequest instanceof PredictionRequest)
					response.setObject(this.modelo.obtenerPrediccion((PredictionRequest)predictionRequest));
				
				response.setJMSCorrelationID(request.getJMSCorrelationID());
	
	            this.responseProducer.send(request.getJMSReplyTo(), response);
			}
			if(request instanceof TextMessage)
			{
				TextMessage response = this.predictionSession.createTextMessage();
				
				//FIX: validar request con el esquema
				ByteArrayInputStream requestBAIS = new ByteArrayInputStream(((TextMessage) request).getText().getBytes());
				PredictionRequest pr = (PredictionRequest) this.um.unmarshal(requestBAIS);
				
				PredictionResponse res = this.modelo.obtenerPrediccion(pr);
				
				StringWriter resString = new StringWriter();
				
				this.m.marshal(res, resString);
				
				response.setText(resString.toString());
				
				response.setJMSCorrelationID(request.getJMSCorrelationID());
	
	            this.responseProducer.send(request.getJMSReplyTo(), response);
			}
		} catch (JMSException e) {			
			e.printStackTrace();
		}
		catch (Exception e) {
			e.printStackTrace();
		}		
	}
}
