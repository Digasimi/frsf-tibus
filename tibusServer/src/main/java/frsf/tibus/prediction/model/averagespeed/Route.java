package frsf.tibus.prediction.model.averagespeed;

import java.util.ArrayList;

import java.util.List;

import javax.persistence.*;

import com.bbn.openmap.proj.Length;
import com.bbn.openmap.proj.coords.LatLonPoint;

import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.domain.PredictionResponse.Prediction;

@Entity
@Table(name="recorrido")
public class Route {
	@Id
	@Column(name="idrecorrido")
	private Integer routeId;
	
	@OneToMany(targetEntity=Stop.class, mappedBy = "route", 
			fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	@OrderBy("orden asc")
	private List<Stop> stops;
	
	@Transient
	private List<Bus> buses;
	

	public Route()
	{
		stops = new ArrayList<Stop>();
		buses = new ArrayList<Bus>();
	}
	
	public Integer getRouteId() {
		return routeId;
	}


	public void setRouteId(Integer routeId) {
		this.routeId = routeId;
	}


	public List<Stop> getStops() {
		return stops;
	}


	public void setStops(List<Stop> stops) {
		this.stops = stops;
	}


	public List<Bus> getBuses() {
		return buses;
	}


	public void setBuses(List<Bus> buses) {
		this.buses = buses;
	}


	public PredictionResponse getPredictions(String stopId) {
		
		PredictionResponse result = new PredictionResponse();
		Stop destination = this.getStopById(stopId);
		
		if (destination != null)
		{
			for(Bus bus: buses)
			{
				if (bus.getCurrentStop().getOrder() <= destination.getOrder())
				{
					Double time = new Double(0);
					Stop tempStop1, tempStop2;
					for(int i = bus.getCurrentStop().getOrder(); i < destination.getOrder();i++)
					{
						tempStop1 = getStopByOrder(i);
						tempStop2 = getNextStop(tempStop1);
						
						time += (getDistance(tempStop1, tempStop2)/
								tempStop1.getAverageSpeed().getAverageSpeed());						
					}
					result.addPrediction(new Prediction(bus.getId().toString(),new Integer(time.intValue()), bus.getLat(), bus.getLon()));
				}
			}
		}
		else
		{
			result.setError("No existe la parada especificada");
		}
		
		if(result.getPrediction().isEmpty())
			result.setError("No hay estimaciones disponibles");
		
		return result;
	}

	public Stop getStopById(String stopId){
		Integer d = new Integer(stopId);
		for(Stop stop:stops){
			if (stop.getStopId().equals(d)){
				return stop;
			}
		}
		return null;
	}
	
	public Stop getStopByOrder(Integer order){
		if(order < this.stops.size())
			return stops.get(order);
		else
			return null;
	}
	
	
	/**
	 * Calcula la distancia entre dos paradas.
	 * El cálculo se hace en el sentido del recorrido.
	 * @param start: Parada origen
	 * @param destination: Parada destino
	 * @return
	 */
	public Double getDistance(Stop start, Stop destination)
	{	
		if(start.equals(destination))
			return new Double(0);
		
		// Si las paradas son consecutivas
		if(consecutive(start,destination))
		{
			Double distance = Length.METER.fromRadians(new LatLonPoint.Float(start.getLat(),start.getLon())
			.distance(new LatLonPoint.Float(destination.getLat(),destination.getLon())));
			return distance;
		}
		else
		{
			Stop nextStop = getNextStop(start);
			return getDistance(start, nextStop) + 
					getDistance(nextStop, destination);
		}	
	}
	
	
	/**
	 * 
	 * @param start
	 * @return
	 */
	public Stop getNextStop(Stop start) {
		if(start.getOrder() < stops.size())
			return stops.get(start.getOrder()+1);
		else
			return stops.get(0);		
	}

	/**
	 * Determina si dos paradas son consecutivas. Se calcula en el sentido de circulación del 
	 * recorrido.
	 * Tener en cuenta que el recorrido es continuo, por lo que la ultima y primera parada 
	 * son consecutivas si se evaluan en ese orden.
	 * @param start: Parada de origen
	 * @param destination: Parada de destino
	 * @return devuelve true si son consecutivas, false de lo contrario
	 */

	public boolean consecutive(Stop start, Stop destination) {
		Integer startOrder = start.getOrder();
		Integer destinationOrder = destination.getOrder();
		
		if(startOrder <= destinationOrder)
			if(startOrder +1 == destinationOrder)
				return true;
			else
				return false;
		else
			if(startOrder == stops.size() && destinationOrder == 1)
				return true;
			else
				return false;
	}
}
