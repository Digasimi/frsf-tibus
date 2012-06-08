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
public class PredictionResponse  implements Serializable {

    private final String tiempoPrediccion;

    public PredictionResponse(String tiempoPrediccion) {
        this.tiempoPrediccion = tiempoPrediccion;
    }

    public String getTiempoPrediccion() {
        return tiempoPrediccion;
    }
}
