package frsf.tibus.prediction.model.averagespeed;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.*;

import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.domain.PredictionResponse.Prediction;

@Entity
@Table(name="recorrido")
public class Route {
	@Id
	@Column(name="idrecorrido")
	private Integer routeId;
	
	@OneToMany(targetEntity=Stop.class, mappedBy = "route", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
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
		Stop destination = this.getStop(stopId);
		if (destination != null)
		{
			for(Bus bus: buses)
			{
				if (bus.getCurrentStop().getOrder() <= destination.getOrder())
				{
					Float time = new Float(0);
					for(int i = bus.getCurrentStop().getOrder(); i < destination.getOrder();i++){
						time += this.getStopByOrder(i).getDistance(this.getStopByOrder(i+1))/
								this.getStopByOrder(i).getAverageSpeed().getAverageSpeed();
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
			result.setError("No hay predicciones");
		
		return result;
	}

	private Stop getStop(String parada){
		Integer d = new Integer(parada);
		for(Stop stop:stops){
			if (stop.getStopId().equals(d)){
				return stop;
			}
		}
		return null;
	}
	
	private Stop getStopByOrder(Integer orden){
		for(Stop stop:stops){
			if (stop.getOrder().equals(orden)){
				return stop;
			}
		}
		return null;
	}


}
