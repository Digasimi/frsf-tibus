


package frsf.tibus.domain;

import java.io.Serializable;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;

import org.joda.time.DateTime;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "prediction",
    "timestamp"
})
@XmlRootElement(name = "prediction-response")
public class PredictionResponse implements Serializable{

	private static final long serialVersionUID = 1L;
	protected List<PredictionResponse.Prediction> prediction;
    @XmlElement(required = true)
    @XmlSchemaType(name = "dateTime")
    protected DateTime timestamp;
    
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

    
    public DateTime getTimestamp() {
        return timestamp;
    }

        public void setTimestamp(DateTime value) {
        this.timestamp = value;
    }


    public void addPrediction(Prediction p)
    {
    	this.prediction.add(p);
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
        protected BigInteger timeSec;
        @XmlElement(required = true)
        protected BigDecimal lat;
        @XmlElement(required = true)
        protected BigDecimal lon;

        public Prediction()
        {
        	
        }
        
        public Prediction(String busId, BigInteger timeSec, BigDecimal lat,
				BigDecimal lon) {
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

        public BigInteger getTimeSec() {
            return timeSec;
        }

        public void setTimeSec(BigInteger value) {
            this.timeSec = value;
        }

        public BigDecimal getLat() {
            return lat;
        }

        public void setLat(BigDecimal value) {
            this.lat = value;
        }

        public BigDecimal getLon() {
            return lon;
        }

        public void setLon(BigDecimal value) {
            this.lon = value;
        }

    }

}
