package frsf.tibus.prediction.model.averagespeed;

import static org.junit.Assert.*;

import org.joda.time.DateTime;
import org.junit.Before;
import org.junit.Test;

import frsf.tibus.domain.BusPositionData;

public class AverageSpeedModelTest {
	
	private AverageSpeedModel testModel;
	
	public AverageSpeedModelTest() {
	}

	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void testAverageSpeedModel() {
		testModel = new AverageSpeedModel();
		assertTrue(testModel != null);
	}
	
	@Test
	public void testProcesarNuevaPosicion() {
		BusPositionData busPosition = new BusPositionData(1234, new Float(37.7), new Float(-122.45), new Float(5.3), new DateTime(), "N");
		testModel.procesarNuevaPosicion(busPosition);
		assertTrue(busPosition != null);
	}
	
	@Test
	public void testProcesarNuevaPosicionVacia() {
		BusPositionData busPosition = null;
		testModel.procesarNuevaPosicion(busPosition);
		assertTrue(busPosition == null);
	}

	@Test
	public void testObtenerPrediccion() {
		fail("Not yet implemented");
	}
	
	@Test
	public void testObtenerPrediccionSinBuses() {
		fail("Not yet implemented");
	}
	
	@Test
	public void testObtenerPrediccionSinEstimacion() {
		fail("Not yet implemented");
	}
	
	@Test
	public void testObtenerPrediccionConLineaNoValida() {
		fail("Not yet implemented");
	}
	
	@Test
	public void testObtenerPrediccionConParadaNoValida() {
		fail("Not yet implemented");
	}
}

