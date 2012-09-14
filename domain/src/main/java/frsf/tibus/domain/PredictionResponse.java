


package frsf.tibus.domain;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;



@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "prediction",
    "timestamp",
    "error"
})
@XmlRootElement(name = "prediction-response")
public class PredictionResponse implements Serializable{

	private static final long serialVersionUID = 1L;
	protected List<PredictionResponse.Prediction> prediction;
    @XmlElement(required = true)
    @XmlSchemaType(name = "dateTime")
    protected String timestamp;
    @XmlElement(required=false)
    protected String error;
    
    public PredictionResponse()
    {
    	prediction = new ArrayList<PredictionResponse.Prediction>();
    }

    public List<PredictionResponse.Prediction> getPrediction() {
        if (prediction == null) {
            prediction = new ArrayList<PredictionResponse.Prediction>();
        }
        return this.prediction;
    }

    
    public String getTimestamp() {
        return timestamp;
    }

        public void setTimestamp(String value) {
        this.timestamp = value;
    }


    public void addPrediction(Prediction p)
    {
    	this.prediction.add(p);
    }

    
    public String getError() {
		return error;
	}

	public void setError(String error) {
		this.error = error;
	}


	@XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "busId",
        "timeSec",
        "lat",
        "lon"
    })
    public static class Prediction {

        @XmlElement(required = true)
        protected String busId;
        @XmlElement(required = true)
        protected Integer timeSec;
        @XmlElement(required = true)
        protected Float lat;
        @XmlElement(required = true)
        protected Float lon;

        public Prediction()
        {
        	
        }
        
        public Prediction(String busId, Integer timeSec, Float lat,
				Float lon) {
			super();
			this.busId = busId;
			this.timeSec = timeSec;
			this.lat = lat;
			this.lon = lon;
		}

	    public String getBusId() {
            return busId;
        }

        public void setBusId(String value) {
            this.busId = value;
        }

        public Integer getTimeSec() {
            return timeSec;
        }

        public void setTimeSec(Integer value) {
            this.timeSec = value;
        }

        public Float getLat() {
            return lat;
        }

        public void setLat(Float value) {
            this.lat = value;
        }

        public Float getLon() {
            return lon;
        }

        public void setLon(Float value) {
            this.lon = value;
        }

    }


}
