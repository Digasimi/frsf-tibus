//
// Este archivo ha sido generado por la arquitectura JavaTM para la implantación de la referencia de enlace (JAXB) XML v2.2.5-2 
// Visite <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Todas las modificaciones realizadas en este archivo se perderán si se vuelve a compilar el esquema de origen. 
// Generado el: PM.08.07 a las 09:15:29 PM ART 
//


package frsf.tibus.nextbusProvider.xml;

import javax.xml.bind.annotation.XmlRegistry;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the frsf.tibus.nextbusProvider package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {


    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: frsf.tibus.nextbusProvider.xml
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link NextBusData }
     * 
     */
    public NextBusData createBody() {
        return new NextBusData();
    }

    /**
     * Create an instance of {@link VehiclePositionData }
     * 
     */
    public VehiclePositionData createVehiclePositionData() {
        return new VehiclePositionData();
    }

    /**
     * Create an instance of {@link NextBusData.LastTime }
     * 
     */
    public NextBusData.LastTime createBodyLastTime() {
        return new NextBusData.LastTime();
    }

}
