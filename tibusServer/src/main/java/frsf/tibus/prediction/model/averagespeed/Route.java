package frsf.tibus.prediction.model.averagespeed;

import java.util.List;

import javax.persistence.*;

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




}
