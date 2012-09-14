//
// Este archivo ha sido generado por la arquitectura JavaTM para la implantación de la referencia de enlace (JAXB) XML v2.2.5-2 
// Visite <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Todas las modificaciones realizadas en este archivo se perderán si se vuelve a compilar el esquema de origen. 
// Generado el: PM.08.07 a las 09:15:29 PM ART 
//


package frsf.tibus.nextbusProvider;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "vehicle",
    "lastTime"
})
@XmlRootElement(name = "body")
public class Body {

    protected List<NextBusPositionData> vehicle;
    @XmlElement(required = true)
    protected Body.LastTime lastTime;
    @XmlAttribute(name = "copyright")
    protected String copyright;

    public List<NextBusPositionData> getVehicle() {
        if (vehicle == null) {
            vehicle = new ArrayList<NextBusPositionData>();
        }
        return this.vehicle;
    }

    
    public Body.LastTime getLastTime() {
        return lastTime;
    }

    public void setLastTime(Body.LastTime value) {
        this.lastTime = value;
    }

    public String getCopyright() {
        return copyright;
    }

    public void setCopyright(String value) {
        this.copyright = value;
    }

    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "")
    public static class LastTime {

        @XmlAttribute(name = "time", required = true)
        @XmlSchemaType(name = "unsignedLong")
        protected Integer time;

        public Integer getTime() {
            return time;
        }

        public void setTime(Integer value) {
            this.time = value;
        }

    }

}
