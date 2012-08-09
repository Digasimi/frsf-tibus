

package frsf.tibus.domain;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "prediccion"
})
@XmlRootElement(name = "prediction-response")
public class PredictionResponse implements Serializable {

	private static final long serialVersionUID = 1L;
	@XmlElement(required = true)
    protected List<BigDecimal> prediccion;
	
	public PredictionResponse()
	{
		prediccion = new ArrayList<BigDecimal>();
	}

    public List<BigDecimal> getPrediccion() {
        if (prediccion == null) {
            prediccion = new ArrayList<BigDecimal>();
        }
        return this.prediccion;
    }

	public void addPrediction(BigDecimal p) {
		prediccion.add(p);
		
	}

}
