package frsf.tibus.prediction.model.averagespeed;

import java.util.ArrayList;
import java.util.HashMap;

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
		Stop stop1 = new Stop();
		stop1.setStopId(new Integer(1));
		stop1.setOrder(new Integer(0));
		stop1.setLat(new Float(-31.635696));
		stop1.setLon(new Float(-60.702808));
		stop1.setAverageSpeed(new AverageSpeed(stop1,(float) 1.0));
		
		Stop stop2 = new Stop();
		stop2.setStopId(new Integer(2));
		stop2.setOrder(new Integer(1));
		stop2.setLat(new Float(-31.637820));
		stop2.setLon(new Float(-60.692556));
		stop2.setAverageSpeed(new AverageSpeed(stop2,(float) 1.0));
		
		route = new Route();
		ArrayList<Stop> stops = new ArrayList<Stop>();
		stops.add(stop1);
		stops.add(stop2);
		route.setStops(stops);
		
		Bus temporaryBus = new Bus(1, route);
		temporaryBus.setCurrentStop(stop1);
		temporaryBus.setId(15);
		HashMap<Integer,Bus> buses = new HashMap<Integer,Bus>();
		buses.put(temporaryBus.getId(),temporaryBus);
		route.setBuses(buses);
	}

	public void testGetPredictions() {
		PredictionResponse p = route.getPredictions("2"); 
		assertEquals(1000,p.getPrediction().get(0).getTimeSec().intValue(),1);
		assertTrue(p.getError()==null);
	}
	
	public void testGetDistanciaParadasConsecutivas()
	{
		assertEquals(new Double(1000),route.getDistance(route.getStopByOrder(0), route.getStopByOrder(1)),1);		
	}
	
	public void testNoPredictionsAvailable() {
		String error = route.getPredictions("3").getError();
		assertTrue(error != null);
	}
	
	public void testCalculateHeadingWithoutStops()
	{
		route = new Route();
		Stop s = new Stop();
		s.setLat((float) 1.0);
		s.setLon((float) 1.0);
		Double result = route.calculateHeading(s);
		
		assertNull(result);
	}
	
	
	public void testCalculateHeadingWithOneStop()
	{
		route = new Route();
		Stop s = new Stop();
		s.setLat((float) 1.0);
		s.setLon((float) 1.0);
		s.setOrder(1);
		ArrayList<Stop> stops = new ArrayList<Stop>();
		stops.add(s);
		route.setStops(stops);
		
		Double result = route.calculateHeading(s);
		Double expected = (double) 0;
		
		assertEquals(expected, result);
	}
	
	public void testCalculateHeadingWithTwoStops()
	{
		route = new Route();
		
		Stop s1 = new Stop();
		s1.setLat((float) 0.0);
		s1.setLon((float) 0.0);
		s1.setOrder(0);
		
		Stop s2 = new Stop();
		s2.setLat((float) 1.0);
		s2.setLon((float) 0.0);
		s2.setOrder(1);
		
		ArrayList<Stop> stops = new ArrayList<Stop>();
		stops.add(s1);
		stops.add(s2);
		route.setStops(stops);
		
		Double result = route.calculateHeading(s1);
		Double expected = (double) 0;
		
		assertEquals((double)0, route.calculateHeading(s1));
		assertEquals((double)180, route.calculateHeading(s2));
		
	}
	
	
	

}
