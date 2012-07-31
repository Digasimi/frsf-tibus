//
// Este archivo ha sido generado por la arquitectura JavaTM para la implantación de la referencia de enlace (JAXB) XML v2.2.5-2 
// Visite <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Todas las modificaciones realizadas en este archivo se perderán si se vuelve a compilar el esquema de origen. 
// Generado el: PM.07.31 a las 07:13:02 PM ART 
//


package frsf.tibus.domain;

import java.math.BigInteger;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Clase Java para anonymous complex type.
 * 
 * <p>El siguiente fragmento de esquema especifica el contenido que se espera que haya en esta clase.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="linea" type="{http://www.w3.org/2001/XMLSchema}string"/>
 *         &lt;element name="parada" type="{http://www.w3.org/2001/XMLSchema}integer"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "linea",
    "parada"
})
@XmlRootElement(name = "prediction-request")
public class PredictionRequest {

    @XmlElement(required = true)
    protected String linea;
    @XmlElement(required = true)
    protected BigInteger parada;

    /**
     * Obtiene el valor de la propiedad linea.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLinea() {
        return linea;
    }

    /**
     * Define el valor de la propiedad linea.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLinea(String value) {
        this.linea = value;
    }

    /**
     * Obtiene el valor de la propiedad parada.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getParada() {
        return parada;
    }

    /**
     * Define el valor de la propiedad parada.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setParada(BigInteger value) {
        this.parada = value;
    }

}
