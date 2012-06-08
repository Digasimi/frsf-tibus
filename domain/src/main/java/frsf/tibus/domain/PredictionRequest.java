/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.domain;

import java.io.Serializable;

/**
 *
 * @author dani
 */
public class PredictionRequest implements Serializable {
    private final Integer parada;
    private final String linea;

    public PredictionRequest(Integer parada, String linea) {
        this.parada = parada;
        this.linea = linea;
    }

    public String getLinea() {
        return linea;
    }

    public Integer getParada() {
        return parada;
    }
}
