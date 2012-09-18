package frsf.tibus.prediction.model.averagespeed;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;

import org.joda.time.DateTime;
import org.junit.Before;
import org.junit.Test;

import com.bbn.openmap.proj.Length;

import frsf.tibus.domain.BusPositionData;

public class BusTest {
	private Route route;
	private Bus b;
	
	@Before
	public void setUp() throws Exception {		
		
		route = new Route();
		ArrayList<Stop> stops = new ArrayList<Stop>();
		
		Stop s1 = new Stop();
		s1.setStopId(new Integer(1));
		s1.setLat(new Float(0.0));
		s1.setLon(new Float(0.0));
		stops.add(s1);
		
		Stop s2 = new Stop();
		s2.setStopId(new Integer(2));
		s2.setLat(new Float(0.001));
		s2.setLon(new Float(0.000));
		stops.add(s2);
		
		Stop s3 = new Stop();
		s3.setStopId(new Integer(3));
		s3.setLat(new Float(0.002));
		s3.setLon(new Float(0.001));
		stops.add(s3);
		
		Stop s4 = new Stop();
		s4.setStopId(new Integer(4));
		s4.setLat(new Float(0.002));
		s4.setLon(new Float(0.002));
		stops.add(s4);
		
		Stop s5 = new Stop();
		s5.setStopId(new Integer(5));
		s5.setLat(new Float(0.002));
		s5.setLon(new Float(0.003));
		stops.add(s5);
		
		Stop s6 = new Stop();
		s6.setStopId(new Integer(6));
		s6.setLat(new Float(0.001));
		s6.setLon(new Float(0.003));
		stops.add(s6);
		
		Stop s7 = new Stop();
		s7.setStopId(new Integer(7));
		s7.setLat(new Float(0.001));
		s7.setLon(new Float(0.002));
		stops.add(s7);
		
		Stop s8 = new Stop();
		s8.setStopId(new Integer(8));
		s8.setLat(new Float(0.0));
		s8.setLon(new Float(0.001));
		stops.add(s8);
		
		route.setStops(stops);
		
		b = new Bus(111, route);
		HashMap<Integer, Bus> buses = new HashMap<Integer, Bus>();
		
		buses.put(b.getId(), b);
		route.setBuses(buses);
		
		route.setRouteName("R");

	}

	@Test
	public void ProcessPosition_NewBusPosition_SetFirstStop() {
		
		BusPositionData busPosition = 
				new BusPositionData(111, (float) 0, (float) 0, (float) 0, new DateTime(), "R");
		
		b.processPosition(busPosition);
		
		assertEquals(route.getFirstStop(), b.getCurrentStop());
	}
	
	@Test
	public void ProcessPosition_TwoBusPositions_FirstStopAndThirdStop() {
		
		BusPositionData busPosition1 = 
				new BusPositionData(111, (float) 0, (float) 0, (float) 0, new DateTime(), "R");

		BusPositionData busPosition2 = 
				new BusPositionData(111, (float) 0.002, (float) 0.002, (float) 90, new DateTime(), "R");
		
		b.processPosition(busPosition1);		
		assertEquals(route.getFirstStop(), b.getCurrentStop());
		
		b.processPosition(busPosition2);
		assertEquals(route.getStopById("4"), b.getCurrentStop());
	}
	
	@Test
	public void ProcessPosition_TwoBusPositions_FirstStopAndFourthStop() {
		
		BusPositionData busPosition1 = 
				new BusPositionData(111, (float) 0.002, (float) 0.002, (float) 90, new DateTime(), "R");

		BusPositionData busPosition2 = 
				new BusPositionData(111, (float) 0, (float) 0, (float) 0, new DateTime(), "R");
		
		b.processPosition(busPosition1);		
		assertEquals(route.getStopById("4"), b.getCurrentStop());
		
		b.processPosition(busPosition2);
		assertEquals(route.getFirstStop(), b.getCurrentStop());
	}
	
	@Test 
	public void calculateAverageSpeed_NoPositionDataAvailable_NullSpeed()
	{
		Double avgSpeed = b.calculateAverageSpeed();
		
		assertNull(avgSpeed);
	}
	
	@Test 
	public void calculateAverageSpeed_PositionDataAvailable()
	{
		Integer timeDiffSecs = 60;
		DateTime d1 = new DateTime();
		DateTime d2 = d1.plusSeconds(timeDiffSecs);
		
		BusPositionData busPosition1 = 
				new BusPositionData(111, (float) 0, (float) 0, (float) 0, d1, "R");

		BusPositionData busPosition2 = 
				new BusPositionData(111, (float) 0.002, (float) 0.002, (float) 90, d2, "R");
		
		Double distanceMts = Length.METER.fromRadians(busPosition1.getCoordinates().distance(busPosition2.getCoordinates()));
		Double avgSpeed = distanceMts / timeDiffSecs;
		
		b.processPosition(busPosition1);				
		b.processPosition(busPosition2);

		assertEquals(avgSpeed, b.calculateAverageSpeed());
	}

}
