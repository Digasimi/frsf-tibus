

package frsf.tibus.domain;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;



@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "linea",
    "parada"
})
@XmlRootElement(name = "prediction-request")
public class PredictionRequest implements Serializable{

    /**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	@XmlElement(required = true)
    protected String linea;
    @XmlElement(required = true)
    protected String parada;

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
     *     {@link String }
     *     
     */
    public String getParada() {
        return parada;
    }

    /**
     * Define el valor de la propiedad parada.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setParada(String value) {
        this.parada = value;
    }

}
