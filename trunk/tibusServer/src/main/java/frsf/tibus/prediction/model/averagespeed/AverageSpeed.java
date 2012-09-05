package frsf.tibus.prediction.model.averagespeed;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

@Entity
@Table(name="averagespeed")
public class AverageSpeed {

	@Id
	@Column(name="averagespeedid")
	private Integer averageSpeedId;
	
	@OneToOne
	@JoinColumn(name = "stop_id", nullable = false)
	private Stop stopId;
	
	@Column(name="speedaverage")
	private Float averageSpeed;
	
	public AverageSpeed() {
		super();
	}

	public AverageSpeed(Stop stopId, Float averageSpeed) {
		super();
		this.stopId = stopId;
		this.averageSpeed = averageSpeed;
	}

	public Float getAverageSpeed() {
		return averageSpeed;
	}

	public void setAverageSpeed(Float averageSpeed) {
		this.averageSpeed = averageSpeed;
	}
}
