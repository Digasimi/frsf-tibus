/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.prediction.model;

import frsf.tibus.domain.BusPositionData;
import frsf.tibus.domain.PredictionRequest;
import frsf.tibus.domain.PredictionResponse;

import org.joda.time.DateTime;

/**
 *
 * @author Daniel González
 */
public class DummyPredictionModel implements PredictionModel {

   

    @Override
    public PredictionResponse obtenerPrediccion(PredictionRequest r) {
        PredictionResponse pr = new PredictionResponse();
        pr.setTimestamp(new DateTime(2012,8,16, 19,33).toString());
        pr.addPrediction(new PredictionResponse.Prediction("001",new Integer("30"), new Float(37.76677954095475), new Float(-122.40331649780273)));
        pr.addPrediction(new PredictionResponse.Prediction("001",new Integer("30"), new Float(37.75334401310656), new Float(-122.41344451904297)));
        pr.addPrediction(new PredictionResponse.Prediction("001",new Integer("30"), new Float(37.74126352639086), new Float(-122.39988327026367)));
        return pr;
    }

    @Override
    public void procesarNuevaPosicion(BusPositionData busPosition) {
        
    }

}
