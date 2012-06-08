/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.domain;

import java.io.Serializable;
import java.util.GregorianCalendar;

/**
 *
 * @author dani
 */
public class Posicion implements Serializable{
    /**
	 * 
	 */
	private static final long serialVersionUID = 3150497970302555791L;
	private String idColectivo;
    private Float lat, lon;
    private GregorianCalendar date;

    public Posicion(String idColectivo, Float lat, Float lon, GregorianCalendar date) {
        this.idColectivo = idColectivo;
        this.lat = lat;
        this.lon = lon;
        this.date = date;
    }

    public GregorianCalendar getDate() {
        return date;
    }

    public void setDate(GregorianCalendar date) {
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
