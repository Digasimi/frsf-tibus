/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.prediction.model;

import frsf.tibus.domain.*;
import java.util.ArrayList;

/**
 *
 * @author dani
 */
public interface PredictionModel {

    public void procesarNuevaPosicion(BusPositionData busPosition);
    public PredictionResponse obtenerPrediccion(PredictionRequest r);

}
