package frsf.tibus.prediction.model.averagespeed;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;

import org.junit.Before;
import org.junit.Test;

import frsf.tibus.domain.PredictionResponse;

import junit.framework.TestCase;

public class RouteTest extends TestCase {

	private Route route;
	
	public RouteTest(String name) {
		super(name);
	}

	@Before
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

	@Test
	public void testGetPredictions() {
		PredictionResponse p = route.getPredictions("2"); 
		assertEquals(1000,p.getPrediction().get(0).getTimeSec().intValue(),1);
		assertTrue(p.getError()==null);
	}
	
	@Test
	public void testNoPredictionsAvailable() {
		String error = route.getPredictions("3").getError();
		assertTrue(error != null);
	}
	
	@Test
	public void testCalculateHeadingWithoutStops()
	{
		route = new Route();
		Stop s = new Stop();
		s.setLat((float) 1.0);
		s.setLon((float) 1.0);

		try{
			route.calculateHeading(null);
			fail();
		}
		catch (IllegalArgumentException e){		}
		
		try{
			route.calculateHeading(s);
			fail();
		}
		catch (IllegalArgumentException e){		}
	}
	
	@Test
	public void testCalculateHeadingWithOneStop()
	{
		route = new Route();
		Stop s = new Stop();
		s.setLat((float) 1.0);
		s.setLon((float) 1.0);
		s.setOrder(1);
		s.setStopId(1);
		ArrayList<Stop> stops = new ArrayList<Stop>();
		stops.add(s);
		route.setStops(stops);
		
		try{
			route.calculateHeading(null);
			fail();
		}
		catch (IllegalArgumentException e){		}
		
		Double result = route.calculateHeading(s);
		Double expected = (double) 0;
		
		assertEquals(expected, result);
	}
	
	@Test
	public void testCalculateHeadingWithTwoStops()
	{
		route = new Route();
		
		Stop s1 = new Stop();
		s1.setLat((float) 0.0);
		s1.setLon((float) 0.0);
		s1.setOrder(0);
		s1.setStopId(0);
		
		Stop s2 = new Stop();
		s2.setLat((float) 1.0);
		s2.setLon((float) 0.0);
		s2.setOrder(1);
		s2.setStopId(1);
		
		Stop s3 = new Stop();
		s3.setLat((float) 1.0);
		s3.setLon((float) 1.0);
		s3.setOrder(2);
		s3.setStopId(2);
		
		Stop s4 = new Stop();
		s4.setLat((float) 0.0);
		s4.setLon((float) 1.0);
		s4.setOrder(3);
		s4.setStopId(3);
		
		ArrayList<Stop> stops = new ArrayList<Stop>();
		stops.add(s1);
		stops.add(s2);
		stops.add(s3);
		stops.add(s4);
		route.setStops(stops);		
		
		assertEquals((double)0, route.calculateHeading(s1), 0.1);
		assertEquals((double)90, route.calculateHeading(s2), 0.1);
		assertEquals((double)180, route.calculateHeading(s3), 0.1);
		assertEquals((double)270, route.calculateHeading(s4), 0.1);
		
	}
	
	@Test
	public void testNextStop()
	{
		route = new Route();
		
		Stop s1 = new Stop();
		s1.setLat((float) 0.0);
		s1.setLon((float) 0.0);
		s1.setOrder(0);
		s1.setStopId(0);
		
		Stop s2 = new Stop();
		s2.setLat((float) 0.001);
		s2.setLon((float) 0.000);
		s2.setOrder(1);
		s2.setStopId(1);
		
		Stop s3 = new Stop();
		s3.setLat((float) 0.001);
		s3.setLon((float) 0.001);
		s3.setOrder(2);
		s3.setStopId(2);
		
		Stop s4 = new Stop();
		s4.setLat((float) 0.0);
		s4.setLon((float) 0.001);
		s4.setOrder(3);
		s4.setStopId(3);
		
		ArrayList<Stop> stops = new ArrayList<Stop>();
		
		//Recorrido sin paradas
		try {
			route.getNextStop(s1);
			fail();
		}
		catch (IllegalArgumentException e){		}
		
		try {
			route.getNextStop(null);
			fail();
		}
		catch (IllegalArgumentException e){		}
		
		
		//Recorrido con una parada
		stops.add(s1);
		route.setStops(stops);
		assertEquals(s1, route.getNextStop(s1));
		
		stops.add(s2);
		stops.add(s3);
		stops.add(s4);
		route.setStops(stops);		
		
		//Recorrido con mas de una parada
		assertEquals(s2, route.getNextStop(s1));
		assertEquals(s3, route.getNextStop(s2));
		assertEquals(s4, route.getNextStop(s3));
		assertEquals(s1, route.getNextStop(s4));
	}
	
	@Test
	public void testDistance()
	{
		route = new Route();
		
		Stop s1 = new Stop();
		s1.setLat((float) 0.0);
		s1.setLon((float) 0.0);
		s1.setStopId(0);
		
		Stop s2 = new Stop();
		s2.setLat((float) 0.001);
		s2.setLon((float) 0.000);
		s2.setStopId(1);
		
		Stop s3 = new Stop();
		s3.setLat((float) 0.001);
		s3.setLon((float) 0.001);
		s3.setStopId(2);
		
		Stop s4 = new Stop();
		s4.setLat((float) 0.0);
		s4.setLon((float) 0.001);
		s4.setStopId(3);
		
		ArrayList<Stop> stops = new ArrayList<Stop>();
		
		stops.add(s1);
		stops.add(s2);
		stops.add(s3);
		stops.add(s4);
		route.setStops(stops);
		
		//Distancia entre paradas consecutivas
		assertEquals(111.1, route.getDistance(s1, s2), 1);
		
		//Distancia a la misma parada
		assertEquals(0.0, route.getDistance(s1, s1));
		
		assertEquals(111.1, route.getDistance(s2, s3), 1);
		assertEquals(111.1*2, route.getDistance(s1, s3), 1);
		assertEquals(111.1*3, route.getDistance(s2, s1), 1);
	}
	
	@Test
	public void testConsecutive()
	{
		route = new Route();
		
		Stop s1 = new Stop();
		s1.setLat((float) 0.0);
		s1.setLon((float) 0.0);
		s1.setStopId(0);
		
		Stop s2 = new Stop();
		s2.setLat((float) 0.001);
		s2.setLon((float) 0.000);
		s2.setStopId(1);
		
		Stop s3 = new Stop();
		s3.setLat((float) 0.001);
		s3.setLon((float) 0.001);
		s3.setStopId(2);
		
		Stop s4 = new Stop();
		s4.setLat((float) 0.0);
		s4.setLon((float) 0.001);
		s4.setStopId(3);
		
		ArrayList<Stop> stops = new ArrayList<Stop>();
		
		stops.add(s1);
		stops.add(s2);
		stops.add(s3);
		stops.add(s4);
		route.setStops(stops);
		
		assertTrue(route.consecutive(s1, s2));
		assertTrue(route.consecutive(s2, s3));
		assertTrue(route.consecutive(s3, s4));
		assertTrue(route.consecutive(s4, s1));
		
		assertFalse(route.consecutive(s1, s1));
		assertFalse(route.consecutive(s2, s1));
		assertFalse(route.consecutive(s1, s3));
		assertFalse(route.consecutive(s1, s4));
		
		try{
			route.consecutive(null, null);
			fail();
		}
		catch (IllegalArgumentException e){		}
	}
	
	@Test
	public void testPreviousStop()
	{
route = new Route();
		
		Stop s1 = new Stop();
		s1.setLat((float) 0.0);
		s1.setLon((float) 0.0);
		s1.setStopId(0);
		
		Stop s2 = new Stop();
		s2.setLat((float) 0.001);
		s2.setLon((float) 0.000);
		s2.setStopId(1);
		
		Stop s3 = new Stop();
		s3.setLat((float) 0.001);
		s3.setLon((float) 0.001);
		s3.setStopId(2);
		
		Stop s4 = new Stop();
		s4.setLat((float) 0.0);
		s4.setLon((float) 0.001);
		s4.setStopId(3);
		
		ArrayList<Stop> stops = new ArrayList<Stop>();
		
		stops.add(s1);
		stops.add(s2);
		stops.add(s3);
		stops.add(s4);
		route.setStops(stops);
		
		assertEquals(s4,route.getPreviousStop(s1));
		assertEquals(s1,route.getPreviousStop(s2));
		assertEquals(s2,route.getPreviousStop(s3));
		assertEquals(s3,route.getPreviousStop(s4));
		
	}

}
