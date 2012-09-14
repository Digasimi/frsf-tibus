package frsf.tibus.prediction.model.averagespeed;

import javax.persistence.*;

import com.bbn.openmap.proj.Length;
import com.bbn.openmap.proj.coords.LatLonPoint;

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
	
	@OneToOne(targetEntity=AverageSpeed.class, mappedBy = "stopId", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	private AverageSpeed averageSpeed;

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
	
	public AverageSpeed getAverageSpeed() {
		return averageSpeed;
	}

	public void setAverageSpeed(AverageSpeed averageSpeed) {
		this.averageSpeed = averageSpeed;
	}	
	
	public boolean equals(Stop s)
	{
		if(s != null)
			if(this.getStopId().equals(s.getStopId()))
				return true;
			else
				return false;
		else
			return false;
	}

	public Double distance(LatLonPoint coordinates) {
		Double distance = Length.METER.fromRadians(new LatLonPoint.Float(lat,lon)
			.distance(coordinates));
		return distance;
	}

	
}
