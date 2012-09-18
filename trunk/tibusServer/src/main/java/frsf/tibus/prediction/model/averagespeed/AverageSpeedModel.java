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
		//Hibernate
		SessionFactory sessionFactory;
		Configuration configuration = new Configuration();
	    configuration.configure();
	    ServiceRegistry serviceRegistry = new ServiceRegistryBuilder().applySettings(configuration.getProperties()).buildServiceRegistry();        
	    sessionFactory = configuration.buildSessionFactory(serviceRegistry);
	    
	    session = sessionFactory.openSession();
	    
		loadRoutes();
	}

	@SuppressWarnings("unchecked")
	private void loadRoutes() 
	{
	    session.beginTransaction();
		routes = new HashMap<String, Route>();	
	    List<Route> result = session.createQuery( "from Route" ).list();
		for ( Route route : (List<Route>) result ) {
			System.out.println( "Recorrido (" + route.getRouteId() + ") : ");
			routes.put(route.getRouteName(), route);
		}
        session.getTransaction().commit();
	}

	@Override
	public void procesarNuevaPosicion(BusPositionData busPosition) 
	{
		Route r = routes.get(busPosition.getRouteName());
		r.processBusPosition(busPosition);
	}

	@Override
	public PredictionResponse obtenerPrediccion(PredictionRequest r) 
	{
		Route route = routes.get(r.getLinea());
		return route.getPredictions(r.getParada());
	}

}
