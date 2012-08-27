package frsf.tibus.prediction.model.averagespeed;

import javax.persistence.*;

@Entity
@Table(name="parada")
public class Stop {
	
	@Id
	@Column(name="idparada")
	private Integer stopId;
	
	@Column(name="orden")
	private Integer order;
	@Column(name="latitud")
	private Float lat;
	@Column(name="longitud")
	private Float lon;
	
	@ManyToOne
	@JoinColumn(name = "linea_id", nullable = false)
	private Route route;
	
	public String getAlgo()
	{
		return "asfadsf";
	}

	
	public Integer getStopId() {
		return stopId;
	}

	public void setStopId(Integer stopId) {
		this.stopId = stopId;
	}

	public Integer getOrder() {
		return order;
	}

	public void setOrder(Integer order) {
		this.order = order;
	}

	public Float getLat() {
		return lat;
	}

	public void setLat(Float lat) {
		this.lat = lat;
	}

	public Float getLon() {
		return lon;
	}

	public void setLon(Float lon) {
		this.lon = lon;
	}

	public Route getRoute() {
		return route;
	}

	public void setRoute(Route route) {
		this.route = route;
	}

}
