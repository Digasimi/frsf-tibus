/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.modeloPrediccion.DummyModel;

import frsf.tibus.domain.BusPositionData;
import frsf.tibus.domain.PredictionRequest;
import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.modeloPrediccion.ModeloPrediccion;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;

/**
 *
 * @author Daniel González
 */
public class DummyPredictionModel implements ModeloPrediccion {

   

    @Override
    public PredictionResponse obtenerPrediccion(PredictionRequest r) {
        PredictionResponse pr = new PredictionResponse();
        pr.addPrediction(new PredictionResponse.Prediction("001",new BigInteger("30"), new BigDecimal(0.00), new BigDecimal(0.00)));
        return pr;
    }

    @Override
    public void procesarNuevaPosicion(BusPositionData busPosition) {
        
    }

}
