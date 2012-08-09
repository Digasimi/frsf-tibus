/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.domain;

import java.io.Serializable;

import org.joda.time.DateTime;


/**
 *
 * @author dani
 */
public class BusPositionData implements Serializable{
    /**
	 * 
	 */
	private static final long serialVersionUID = 3150497970302555791L;
	private String idColectivo;
    private Float lat, lon;
    private DateTime date;

    public BusPositionData(String idColectivo, Float lat, Float lon, DateTime date) {
        this.idColectivo = idColectivo;
        this.lat = lat;
        this.lon = lon;
        this.date = date;
    }

    public DateTime getDate() {
        return date;
    }

    public void setDate(DateTime date) {
        this.date = date;
    }

    public void setIdColectivo(String idColectivo) {
        this.idColectivo = idColectivo;
    }

    public void setLat(Float lat) {
        this.lat = lat;
    }

    public void setLon(Float lon) {
        this.lon = lon;
    }

    public String getIdColectivo() {
        return idColectivo;
    }

    public Float getLat() {
        return lat;
    }

    public Float getLon() {
        return lon;
    }

}
