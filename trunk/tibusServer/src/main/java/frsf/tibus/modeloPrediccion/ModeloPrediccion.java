/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package frsf.tibus.modeloPrediccion;

import frsf.tibus.domain.*;
import java.util.ArrayList;

/**
 *
 * @author dani
 */
public interface ModeloPrediccion {

    public void procesarNuevasPosiciones(ArrayList<Posicion> posiciones);
    public PredictionResponse obtenerPrediccion(PredictionRequest r);

}
