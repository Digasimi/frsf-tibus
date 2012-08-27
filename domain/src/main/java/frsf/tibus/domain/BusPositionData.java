/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.domain;

import java.io.Serializable;

import org.joda.time.DateTime;


/**
 *
 * @author Daniel González
 */

public class BusPositionData implements Serializable{
    /**
	 * 
	 */
	private static final long serialVersionUID = 3150497970302555791L;
	private String busId;
    private Float lat, lon;
    private Float heading;
    private DateTime date;
    private String routeId;

    

    public BusPositionData(String busId, Float lat, Float lon, Float heading,
			DateTime date, String routeId) {
		super();
		this.busId = busId;
		this.lat = lat;
		this.lon = lon;
		this.heading = heading;
		this.date = date;
		this.routeId = routeId;
	}

	public DateTime getDate() {
        return date;
    }

    public void setDate(DateTime date) {
        this.date = date;
    }

    public void setIdColectivo(String idColectivo) {
        this.busId = idColectivo;
    }

    public void setLat(Float lat) {
        this.lat = lat;
    }

    public void setLon(Float lon) {
        this.lon = lon;
    }

    public String getIdColectivo() {
        return busId;
    }

    public Float getLat() {
        return lat;
    }

    public Float getLon() {
        return lon;
    }

	public String getRouteId() {
		return routeId;
	}

	public void setRouteId(String routeId) {
		this.routeId = routeId;
	}

	public Float getHeading() {
		return heading;
	}

	public void setHeading(Float heading) {
		this.heading = heading;
	}

}
