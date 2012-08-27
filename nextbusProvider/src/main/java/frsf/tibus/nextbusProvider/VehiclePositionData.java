//
// Este archivo ha sido generado por la arquitectura JavaTM para la implantación de la referencia de enlace (JAXB) XML v2.2.5-2 
// Visite <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Todas las modificaciones realizadas en este archivo se perderán si se vuelve a compilar el esquema de origen. 
// Generado el: PM.08.07 a las 09:15:29 PM ART 
//


package frsf.tibus.nextbusProvider;

import java.math.BigDecimal;
import java.math.BigInteger;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Clase Java para vehiclePositionData complex type.
 * 
 * <p>El siguiente fragmento de esquema especifica el contenido que se espera que haya en esta clase.
 * 
 * <pre>
 * &lt;complexType name="vehiclePositionData">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="routeTag" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="dirTag" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="lat" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="lon" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="secsSinceReport" use="required" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="predictable" use="required" type="{http://www.w3.org/2001/XMLSchema}boolean" />
 *       &lt;attribute name="heading" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="speedKmHr" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "vehiclePositionData")
public class VehiclePositionData {

    @XmlAttribute(name = "id", required = true)
    protected String id;
    @XmlAttribute(name = "routeTag")
    protected String routeTag;
    @XmlAttribute(name = "dirTag")
    protected String dirTag;
    @XmlAttribute(name = "lat", required = true)
    protected BigDecimal lat;
    @XmlAttribute(name = "lon", required = true)
    protected BigDecimal lon;
    @XmlAttribute(name = "secsSinceReport", required = true)
    protected BigInteger secsSinceReport;
    @XmlAttribute(name = "predictable", required = true)
    protected boolean predictable;
    @XmlAttribute(name = "heading", required = true)
    protected BigDecimal heading;
    @XmlAttribute(name = "speedKmHr", required = true)
    protected BigDecimal speedKmHr;

    /**
     * Obtiene el valor de la propiedad id.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Define el valor de la propiedad id.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    /**
     * Obtiene el valor de la propiedad routeTag.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRouteTag() {
        return routeTag;
    }

    /**
     * Define el valor de la propiedad routeTag.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRouteTag(String value) {
        this.routeTag = value;
    }

    /**
     * Obtiene el valor de la propiedad dirTag.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDirTag() {
        return dirTag;
    }

    /**
     * Define el valor de la propiedad dirTag.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDirTag(String value) {
        this.dirTag = value;
    }

    /**
     * Obtiene el valor de la propiedad lat.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getLat() {
        return lat;
    }

    /**
     * Define el valor de la propiedad lat.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setLat(BigDecimal value) {
        this.lat = value;
    }

    /**
     * Obtiene el valor de la propiedad lon.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getLon() {
        return lon;
    }

    /**
     * Define el valor de la propiedad lon.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setLon(BigDecimal value) {
        this.lon = value;
    }

    /**
     * Obtiene el valor de la propiedad secsSinceReport.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getSecsSinceReport() {
        return secsSinceReport;
    }

    /**
     * Define el valor de la propiedad secsSinceReport.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setSecsSinceReport(BigInteger value) {
        this.secsSinceReport = value;
    }

    /**
     * Obtiene el valor de la propiedad predictable.
     * 
     */
    public boolean isPredictable() {
        return predictable;
    }

    /**
     * Define el valor de la propiedad predictable.
     * 
     */
    public void setPredictable(boolean value) {
        this.predictable = value;
    }

    /**
     * Obtiene el valor de la propiedad heading.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getHeading() {
        return heading;
    }

    /**
     * Define el valor de la propiedad heading.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setHeading(BigDecimal value) {
        this.heading = value;
    }

    /**
     * Obtiene el valor de la propiedad speedKmHr.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getSpeedKmHr() {
        return speedKmHr;
    }

    /**
     * Define el valor de la propiedad speedKmHr.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setSpeedKmHr(BigDecimal value) {
        this.speedKmHr = value;
    }

}
