package frsf.tibus.prediction.model.averagespeed;

import org.joda.time.Period;

import com.bbn.openmap.proj.Length;

import frsf.tibus.domain.BusPositionData;
import frsf.tibus.prediction.model.averagespeed.Route;
import frsf.tibus.prediction.model.averagespeed.Stop;

public class Bus extends frsf.tibus.prediction.model.Bus{

	// Parada asignada según posición recibida
	private Stop currentStop;
	private Stop previousStop;
	
	// Ubicación real
	private BusPositionData previousLocation;
	private BusPositionData currentLocation;
	
	public Bus(Integer id, Route route) {
		super(id, route);
		this.currentStop = null;
	}
	
	public Stop getCurrentStop() {
		return currentStop;
	}
	public void setCurrentStop(Stop currentStop) {
		this.currentStop = currentStop;
	}

	protected void processPosition(BusPositionData busPosition) 
	{
		Stop nearestStop;
		if(currentStop == null)
			nearestStop = route.findNearestStop(busPosition);
		else
			nearestStop = route.findNearestStop(busPosition, currentStop);
		
//			if(nearestStop != null)
		
		previousStop = currentStop;
		currentStop = nearestStop;
		
		previousLocation = currentLocation;
		currentLocation = busPosition;
		
		this.lat = busPosition.getLat();
		this.lon = busPosition.getLon();
	}

	public Double calculateAverageSpeed() {
		
		if(previousLocation != null && currentLocation != null)
		{
			Double distance = Length.METER.fromRadians(previousLocation.getCoordinates().distance(currentLocation.getCoordinates()));
			Integer timeDifference = new Period(previousLocation.getDate(), currentLocation.getDate())
											.toStandardSeconds()
											.getSeconds();
			
			return distance / timeDifference;
		}
		else
			return null;
	}

	public String getRouteName() {
		return this.route.getRouteName();
	}

	public Stop getPreviousStop() {
		return this.previousStop;
	}

	public BusPositionData getCurrentLocation() {
		return this.currentLocation;
	}
}
