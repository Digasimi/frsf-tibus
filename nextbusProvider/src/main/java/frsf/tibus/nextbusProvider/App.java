package frsf.tibus.nextbusProvider;


import java.io.IOException;
import java.io.InputStream;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageProducer;
import javax.jms.ObjectMessage;
import javax.jms.Session;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;


import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.*;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.joda.time.DateTime;

import frsf.tibus.domain.BusPositionData;


public class App 
{	
    public static void main( String[] args ) throws ClientProtocolException, IOException, JAXBException, InterruptedException
    {
    	ActiveMQConnectionFactory jmsConnectionFactory;
    	HttpClient httpclient = new DefaultHttpClient();    	
    	
    	JAXBContext jc;
    	Unmarshaller um;
    	
    	String messageBrokerUrl = "tcp://localhost:61616";
		jmsConnectionFactory = new ActiveMQConnectionFactory(messageBrokerUrl);
	    Connection connection;	 
	    
	    String url = "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=N&t=";
	    Integer lastTime = 0;
	    
		try {
			connection = jmsConnectionFactory.createConnection();			
			connection.start();
			Session jmsSession = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			Destination busQueue = jmsSession.createQueue("busesPosition");
			MessageProducer p = jmsSession.createProducer(busQueue);
		    	
	    	
	    	jc = JAXBContext.newInstance("frsf.tibus.nextbusProvider");
	    	um = jc.createUnmarshaller();	

	    	HttpResponse response;
	    	HttpEntity entity;
	    	
	    	while(true)
	    	{
	    		response = httpclient.execute(new HttpGet(url + lastTime));
	        	entity = response.getEntity();
	        	
		    	if (entity != null) 
		    	{
		    		InputStream is = entity.getContent();
		    		Body b = (Body) um.unmarshal(is);
		    	    
		    		for(NextBusPositionData data : b.getVehicle())
		    		{
		    			if(data.isPredictable())
		    			{
			    			ObjectMessage r = jmsSession.createObjectMessage();
			    			DateTime timestamp = new DateTime();
			    			
			    			timestamp.minusSeconds(data.getSecsSinceReport());
			    			
			    			r.setObject(new BusPositionData(new Integer(data.getId()), data.getLat(), 
			    					data.getLon(), data.getHeading(), timestamp,"3" /*data.getRouteTag()*/));
			    			p.send(r);
		    			}
		    		}
		    		lastTime = b.getLastTime().getTime();
		    	}
		    	
		    	Thread.sleep(60000);
	    	}
	    		
    	} catch (JMSException e) {			
			e.printStackTrace();
		}	    	        	
    }
}
