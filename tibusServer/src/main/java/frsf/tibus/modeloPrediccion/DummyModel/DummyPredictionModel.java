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

import org.joda.time.DateTime;

/**
 *
 * @author Daniel González
 */
public class DummyPredictionModel implements ModeloPrediccion {

   

    @Override
    public PredictionResponse obtenerPrediccion(PredictionRequest r) {
        PredictionResponse pr = new PredictionResponse();
        pr.setTimestamp(new DateTime(2012,8,16, 19,33));
        pr.addPrediction(new PredictionResponse.Prediction("001",new BigInteger("30"), new BigDecimal(37.76677954095475), new BigDecimal(-122.40331649780273)));
        pr.addPrediction(new PredictionResponse.Prediction("001",new BigInteger("30"), new BigDecimal(37.75334401310656), new BigDecimal(-122.41344451904297)));
        pr.addPrediction(new PredictionResponse.Prediction("001",new BigInteger("30"), new BigDecimal(37.74126352639086), new BigDecimal(-122.39988327026367)));
        return pr;
    }

    @Override
    public void procesarNuevaPosicion(BusPositionData busPosition) {
        
    }

}
