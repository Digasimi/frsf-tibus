/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.domain;

import java.io.Serializable;

import org.joda.time.DateTime;

import com.bbn.openmap.proj.coords.LatLonPoint;


/**
 *
 * @author Daniel González
 */

public class BusPositionData implements Serializable{

	private static final long serialVersionUID = 3150497970302555791L;
	private Integer busId;
    private Float lat, lon;
    private Float heading;
    private DateTime date;
    private String routeName;

    public BusPositionData(Integer busId, Float lat, Float lon, Float heading,
			DateTime date, String routeName) {
		super();
		this.busId = busId;
		this.lat = lat;
		this.lon = lon;
		this.heading = heading;
		this.date = date;
		this.routeName = routeName;
	}

	public DateTime getDate() {
        return date;
    }

    public void setDate(DateTime date) {
        this.date = date;
    }

    public void setIdColectivo(Integer idColectivo) {
        this.busId = idColectivo;
    }

    public void setLat(Float lat) {
        this.lat = lat;
    }

    public void setLon(Float lon) {
        this.lon = lon;
    }

    public Integer getIdColectivo() {
        return busId;
    }

    public Float getLat() {
        return lat;
    }

    public Float getLon() {
        return lon;
    }

	public String getRouteName() {
		return routeName;
	}

	public void setRouteName(String routeName) {
		this.routeName = routeName;
	}

	public Float getHeading() {
		return heading;
	}

	public void setHeading(Float heading) {
		this.heading = heading;
	}

	public LatLonPoint getCoordinates() {
		return new LatLonPoint.Float(lat, lon);
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((busId == null) ? 0 : busId.hashCode());
		result = prime * result + ((date == null) ? 0 : date.hashCode());
		result = prime * result + ((heading == null) ? 0 : heading.hashCode());
		result = prime * result + ((lat == null) ? 0 : lat.hashCode());
		result = prime * result + ((lon == null) ? 0 : lon.hashCode());
		result = prime * result
				+ ((routeName == null) ? 0 : routeName.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		
		BusPositionData other = (BusPositionData) obj;
		if (busId == null) {
			if (other.busId != null)
				return false;
		} else if (!busId.equals(other.busId))
			return false;
		if (date == null) {
			if (other.date != null)
				return false;
		} else if (!date.equals(other.date))
			return false;
		if (heading == null) {
			if (other.heading != null)
				return false;
		} else if (!heading.equals(other.heading))
			return false;
		if (lat == null) {
			if (other.lat != null)
				return false;
		} else if (!lat.equals(other.lat))
			return false;
		if (lon == null) {
			if (other.lon != null)
				return false;
		} else if (!lon.equals(other.lon))
			return false;
		if (routeName == null) {
			if (other.routeName != null)
				return false;
		} else if (!routeName.equals(other.routeName))
			return false;
		return true;
	}
	
	@Override
	public String toString() {
		return "BusPositionData [busId=" + busId + ", lat=" + lat + ", lon="
				+ lon + ", heading=" + heading + ", date=" + date
				+ ", routeName=" + routeName + "]";
	}
}
