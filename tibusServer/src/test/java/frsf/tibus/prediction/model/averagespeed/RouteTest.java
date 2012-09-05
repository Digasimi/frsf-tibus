package frsf.tibus.prediction.model.averagespeed;

import java.util.ArrayList;

import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.domain.PredictionResponse.Prediction;

import junit.framework.TestCase;

public class RouteTest extends TestCase {

	private Route route;
	
	public RouteTest(String name) {
		super(name);
	}

	protected void setUp() throws Exception {
		super.setUp();
		Stop temporaryStop1 = new Stop();
		temporaryStop1.setStopId(new Integer(0));
		temporaryStop1.setOrder(new Integer(0));
		temporaryStop1.setAverageSpeed(new AverageSpeed(temporaryStop1,(float) 1.0));
		
		Stop temporaryStop2 = new Stop();
		temporaryStop2.setStopId(new Integer(1));
		temporaryStop2.setOrder(new Integer(1));
		temporaryStop2.setAverageSpeed(new AverageSpeed(temporaryStop2,(float) 1.0));
		
		route = new Route();
		ArrayList<Stop> stops = new ArrayList<Stop>();
		stops.add(temporaryStop1);
		stops.add(temporaryStop2);
		route.setStops(stops);
		
		Bus temporaryBus = new Bus();
		temporaryBus.setCurrentStop(temporaryStop1);
		temporaryBus.setId(15);
		ArrayList<Bus> buses = new ArrayList<Bus>();
		buses.add(temporaryBus);
		route.setBuses(buses);
	}

	public void testGetPredictions() {
		PredictionResponse p = route.getPredictions("1"); 
		assertEquals(1,p.getPrediction().get(0).getTimeSec().intValue());
		assertTrue(p.getError()==null);
	}
	
	public void testNoPredictionsAvailable() {
		String error = route.getPredictions("3").getError();
		assertTrue(error != null);
	}
	

}
