/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.modeloPrediccion.test;

import frsf.tibus.domain.Posicion;
import frsf.tibus.domain.PredictionRequest;
import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.modeloPrediccion.ModeloPrediccion;
import java.util.ArrayList;

/**
 *
 * @author dani
 */
public class ModeloTest implements ModeloPrediccion {

   

    @Override
    public PredictionResponse obtenerPrediccion(PredictionRequest r) {
        return new PredictionResponse("Espera 10 Minutos");
    }

    @Override
    public void procesarNuevasPosiciones(ArrayList<Posicion> posiciones) {
        throw new UnsupportedOperationException("Not supported yet.");
    }

}
