package frsf.tibus.prediction.model.averagespeed;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

import com.bbn.openmap.proj.coords.LatLonPoint;

public class StopTest {

	public StopTest() {
	}

	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void testEqualsStop() {
		Stop stopTemp = new Stop();
		stopTemp.setStopId(new Integer(1));
		assertTrue(stopTemp.equals(stopTemp));
	}
	
	@Test
	public void testNotEqualsStop() {
		Stop stopTemp = new Stop();
		stopTemp.setStopId(new Integer(1));
		Stop stopTemp2 = new Stop();
		stopTemp2.setStopId(new Integer(2));
		assertFalse(stopTemp.equals(stopTemp2));
	}

	@Test
	public void testNullDistance() {
		Stop stopTemp = new Stop();
		stopTemp.setStopId(new Integer(1));
		stopTemp.setLat(new Float(0));
		stopTemp.setLon(new Float(0));
		stopTemp.setOrder(new Integer(1));
		assertEquals(stopTemp.distance(new LatLonPoint.Float(stopTemp.getLat(), stopTemp.getLon())),new Double(0));
	}
	
	public void testFixedDistance() {
		Stop stopTemp = new Stop();
		stopTemp.setStopId(new Integer(1));
		stopTemp.setLat(new Float(0));
		stopTemp.setLon(new Float(0));
		stopTemp.setOrder(new Integer(1));
		Stop stopTemp2 = new Stop();
		stopTemp2.setStopId(new Integer(1));
		stopTemp2.setLat(new Float(0));
		stopTemp2.setLon(new Float(1));
		stopTemp2.setOrder(new Integer(2));
		assertEquals(stopTemp.distance(new LatLonPoint.Float(stopTemp2.getLat(), stopTemp2.getLon())),new Double(1));
	}

}
