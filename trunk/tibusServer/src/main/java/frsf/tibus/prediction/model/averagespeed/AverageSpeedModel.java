package frsf.tibus.prediction.model.averagespeed;

import java.util.HashMap;
import java.util.List;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;
import org.hibernate.service.ServiceRegistryBuilder;

import frsf.tibus.domain.BusPositionData;
import frsf.tibus.domain.PredictionRequest;
import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.prediction.model.PredictionModel;

public class AverageSpeedModel implements PredictionModel {
	
	private Session session;	
	private HashMap<String, Route> routes; 
	
	public AverageSpeedModel()
	{
		SessionFactory sessionFactory;
		Configuration configuration = new Configuration();
	    configuration.configure();
	    ServiceRegistry serviceRegistry = new ServiceRegistryBuilder().applySettings(configuration.getProperties()).buildServiceRegistry();        
	    sessionFactory = configuration.buildSessionFactory(serviceRegistry);
	    
	    session = sessionFactory.openSession();
	    
		loadRoutes();
	}

	private void loadRoutes() 
	{
	    session.beginTransaction();
				
	    List result = session.createQuery( "from Route" ).list();
		for ( Route route : (List<Route>) result ) {
			System.out.println( "Recorrido (" + route.getRouteId() + ") : ");
		}
        session.getTransaction().commit();
	}

	@Override
	public void procesarNuevaPosicion(BusPositionData busPosition) {
				
	}

	@Override
	public PredictionResponse obtenerPrediccion(PredictionRequest r) {
		return null;
	}

}
