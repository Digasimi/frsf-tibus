package frsf.tibus.prediction.model.averagespeed;

import java.sql.Timestamp;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import org.hibernate.annotations.GenericGenerator;

@Entity
@Table(name="averagespeed")
public class AverageSpeed {

	@Id
	@Column(name="averagespeed_id")
	@GeneratedValue(generator="increment")
	@GenericGenerator(name="increment", strategy = "increment")
	private Integer averageSpeedId;
	
	@OneToOne
	@JoinColumn(name = "stop_id", nullable = false)
	private Stop stopId;
	
	@Column(name="averagespeed")
	private Float averageSpeed;
	
	@Column
	private Timestamp timestamp;
	
	public AverageSpeed() {
		super();
	}

	public AverageSpeed(Stop stopId, Float averageSpeed, Timestamp timestamp) {
		super();
		this.stopId = stopId;
		this.averageSpeed = averageSpeed;
		this.timestamp = timestamp;
	}

	public Float getAverageSpeed() {
		return averageSpeed;
	}

	public void setAverageSpeed(Float averageSpeed) {
		this.averageSpeed = averageSpeed;
	}
}
