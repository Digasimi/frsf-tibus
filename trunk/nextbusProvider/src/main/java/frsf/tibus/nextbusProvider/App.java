package frsf.tibus.nextbusProvider;


import java.io.IOException;
import java.io.InputStream;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;


import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.*;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

public class App 
{	
    public static void main( String[] args ) throws ClientProtocolException, IOException, JAXBException
    {
    	HttpClient httpclient = new DefaultHttpClient();
    	HttpGet httpget = new HttpGet("http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=N&t=0");
    	HttpResponse response = httpclient.execute(httpget);
    	HttpEntity entity = response.getEntity();
    	
    	JAXBContext jc;
    	Unmarshaller um;
    	
    	jc = JAXBContext.newInstance("frsf.tibus.nextbusProvider");
    	um = jc.createUnmarshaller();	
    	
    	if (entity != null) {
    		InputStream is = entity.getContent();
    		Body b = (Body) um.unmarshal(is);
    		System.out.println(b.getCopyright());
    	    try {

    	        } 
    	    
    	    finally 
    	    {
    	    is.close();
    	    }
    	}
    }
}
