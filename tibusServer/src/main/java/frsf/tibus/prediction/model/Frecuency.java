package frsf.tibus.prediction.model;

import javax.persistence.*;

import org.hibernate.annotations.Type;
import org.joda.time.DateTime;
import org.joda.time.LocalDateTime;

import frsf.tibus.prediction.model.averagespeed.Route;

@Entity
@Table(name="frecuencia")
public class Frecuency {
	
	@Id
	@Column(name="idfrecuencia")
	private Integer frecuencyId;
	
	@Column(name="dia_semana")
	private String weekDay;
	@Column(name="hora")
	@Type(type="org.jadira.usertype.dateandtime.joda.PersistentLocalDateTime")
	private LocalDateTime time;
	
	@ManyToOne
	@JoinColumn(name = "linea_id", nullable = false)
	private Route route;

	public String getWeekDay() {
		return weekDay;
	}

	public void setWeekDay(String weekDay) {
		this.weekDay = weekDay;
	}

	public LocalDateTime getTime() {
		return time;
	}

	public void setTime(LocalDateTime time) {
		this.time = time;
	}

	public Route getRoute() {
		return route;
	}

	public void setRoute(Route route) {
		this.route = route;
	}
};
