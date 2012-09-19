package frsf.tibus.nextbusProvider;


import java.io.IOException;
import java.io.InputStream;
import java.util.ResourceBundle;

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
import frsf.tibus.nextbusProvider.xml.NextBusData;
import frsf.tibus.nextbusProvider.xml.VehiclePositionData;


public class NextBusProvider 
{	
	private ResourceBundle properties;
	private ActiveMQConnectionFactory jmsConnectionFactory;
	private HttpClient httpclient;
	private Connection connection;
	private Session jmsSession;
	private String url;
	private MessageProducer p;
	private Unmarshaller um;
	
	JAXBContext jc;
	
    public static void main( String[] args ) throws Exception, JMSException
    {
    	NextBusProvider provider = new NextBusProvider();
    	provider.retrievePositions();
    }
    
    public NextBusProvider() throws JMSException, JAXBException
    {
    	setUpProvider();
    }
    
    public void setUpProvider() throws JMSException, JAXBException
    {
    	properties = ResourceBundle.getBundle("providerProperties");
    	
    	httpclient = new DefaultHttpClient();
    	
    	String messageBrokerUrl = "tcp://"+properties.getString("jms.broker.ip")+":"
    								+properties.getString("jms.broker.port");
		
    	jmsConnectionFactory = new ActiveMQConnectionFactory(messageBrokerUrl);
	    
	    url = "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=N&t="
	    		+properties.getString("route");
	    
		connection = jmsConnectionFactory.createConnection();
		connection.start();
		jmsSession = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
		Destination busQueue = jmsSession.createQueue(properties.getString("jms.broker.queue"));
		p = jmsSession.createProducer(busQueue);
		
		jc = JAXBContext.newInstance("frsf.tibus.nextbusProvider.xml");
		um = jc.createUnmarshaller();
    }
    
    public void retrievePositions()
    {
	    Integer lastTime = 0;
	    
		HttpResponse response;
    	HttpEntity entity;
    	
    	while(true)
    	{
    		try 
    		{
	    		response = httpclient.execute(new HttpGet(url + lastTime));
	        	entity = response.getEntity();
	        	
		    	if (entity != null) 
		    	{
		    		InputStream is = entity.getContent();
		    		NextBusData b = (NextBusData) um.unmarshal(is);
		    	    
		    		for(VehiclePositionData data : b.getVehicle())
		    		{
		    			if(data.isPredictable())
		    			{
			    			ObjectMessage r = jmsSession.createObjectMessage();
			    			DateTime timestamp = new DateTime();
			    			
			    			timestamp.minusSeconds(data.getSecsSinceReport());
			    			
			    			r.setObject(new BusPositionData(new Integer(data.getId()), data.getLat(), 
			    					data.getLon(), data.getHeading(), timestamp,data.getRouteTag()));
			    			p.send(r);
		    			}
		    		}
		    		lastTime = b.getLastTime().getTime();
		    	}
		    	
	    	Thread.sleep(60000);
	    	
        	}
        	catch (JMSException e) {			
    			e.printStackTrace();
    		} catch (JAXBException e) {
    			e.printStackTrace();
    		} catch (InterruptedException e) {
    			e.printStackTrace();
    		} catch (IllegalStateException e) {
    			e.printStackTrace();
    		} catch (IOException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    		}
    	}
    }
}
