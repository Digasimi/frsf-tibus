package frsf.tibus.prediction.model.averagespeed;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

import java.util.List;

import javax.persistence.*;

import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormatter;
import org.joda.time.format.DateTimeFormatterBuilder;

import com.bbn.openmap.proj.Length;
import com.bbn.openmap.proj.coords.LatLonPoint;

import frsf.tibus.domain.BusPositionData;
import frsf.tibus.domain.PredictionResponse;
import frsf.tibus.domain.PredictionResponse.Prediction;
import frsf.tibus.prediction.model.averagespeed.Bus;
import frsf.tibus.prediction.model.Frecuency;

@Entity
@Table(name="recorrido")
public class Route {
	@Id
	@Column(name="idrecorrido")
	private Integer routeId;
	
	@Column(name="linea")
	private String routeName;
	
	@OneToMany(targetEntity=Stop.class, mappedBy = "route", 
			fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	@OrderBy("orden asc")
	private List<Stop> stops;

	@OneToMany(targetEntity=Frecuency.class, mappedBy = "route", 
			fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	private Set<Frecuency> frecuencies;
	
	@Transient
	private HashMap<Integer,Bus> buses;
	
	@Transient
	final private Float distanceTolerance = (float) 50;
	
	@Transient
	final private Integer headingDifferenceTolerance = 90;
	

	public Route()
	{
		stops = new ArrayList<Stop>();
		buses = new HashMap<Integer,Bus>();
		frecuencies = new HashSet<Frecuency>();
	}
	
	public Integer getRouteId() {
		return routeId;
	}

	public void setRouteId(Integer routeId) {
		this.routeId = routeId;
	}

	public List<Stop> getStops() {
		return stops;
	}

	public void setStops(List<Stop> stops) {
		this.stops = stops;
	}

	public Set<Frecuency> getFrecuencies() {
		return frecuencies;
	}

	public void setFrecuencies(Set<Frecuency> frecuencies) {
		this.frecuencies = frecuencies;
	}

	public HashMap<Integer,Bus> getBuses() {
		return buses;
	}

	public void setBuses(HashMap<Integer,Bus> buses) {
		this.buses = buses;
	}

	
	public PredictionResponse getPredictions(String stopId) {
		
		PredictionResponse result = new PredictionResponse();
		Stop destination = this.getStopById(stopId);
		
		if (destination != null)
		{
			for(Bus bus: buses.values())
			{
				if(bus.getCurrentStop() != null)
				{
					if (getStopOrder(bus.getCurrentStop()) <= getStopOrder(destination))
					{
						Double time = new Double(0);
						Stop tempStop1, tempStop2;
						for(int i = getStopOrder(bus.getCurrentStop()); i < getStopOrder(destination);i++)
						{
							tempStop1 = getStopByOrder(i);
							tempStop2 = getNextStop(tempStop1);
							
							time += getDistance(tempStop1, tempStop2)/
									tempStop1.getAverageSpeed();						
						}
						result.addPrediction(new Prediction(bus.getId().toString(),new Integer(time.intValue()), 
								bus.getLat(), bus.getLon()));
					}
				}
			}
			 DateTimeFormatter dateFormat = new DateTimeFormatterBuilder()
			 		.appendHourOfDay(2)
			 		.appendLiteral(":")
					.appendMinuteOfHour(2)
					.appendLiteral(" de ")
					.appendDayOfWeekText()
					.appendLiteral(' ')
					.appendDayOfMonth(2)
					.appendLiteral(" de ")
					.appendMonthOfYearText()
					.appendLiteral(" de ")
					.appendYear(4, 4)
					.toFormatter();
	 		dateFormat.withLocale(new Locale("es_ES"));
			result.setTimestamp(dateFormat.print(new DateTime()));
		}
		else
		{
			result.setError("No existe la parada especificada");
		}
		
		if(result.getPrediction().isEmpty()){
			result.setError("No hay estimaciones disponibles");
			//Agregar predicciones con las frecuencias (colocar verdadero solo si hay proxima frecuencia)
			if (!this.frecuencies.isEmpty()){
				if (destination != null){
					Double time = new Double(0);
					Stop tempStop1, tempStop2;
					for(int i = 1; i < getStopOrder(destination);i++)
					{
						tempStop1 = getStopByOrder(i);
						tempStop2 = getNextStop(tempStop1);
						
						time += getDistance(tempStop1, tempStop2)/
								tempStop1.getAverageSpeed();						
					}
					tempStop1 = getStopByOrder(1);
					time = time + findNextFrecuency(new DateTime());
					result.addPrediction(new Prediction("Siguiente",new Integer(time.intValue()), 
							tempStop1.getLat(), tempStop1.getLon()));
				}
				 DateTimeFormatter dateFormat = new DateTimeFormatterBuilder()
			 		.appendHourOfDay(2)
			 		.appendLiteral(":")
					.appendMinuteOfHour(2)
					.appendLiteral(" de ")
					.appendDayOfWeekText()
					.appendLiteral(' ')
					.appendDayOfMonth(2)
					.appendLiteral(" de ")
					.appendMonthOfYearText()
					.appendLiteral(" de ")
					.appendYear(4, 4)
					.toFormatter();
				 dateFormat.withLocale(new Locale("es_ES"));
				 result.setTimestamp(dateFormat.print(new DateTime()));
			}
		}
		return result;
	}

	public Integer findNextFrecuency(DateTime time) {
		Integer diferenciaMinima = 86400, diferencia; // 24 hours * 60 minutes * 60 seconds
		new DateTime();
		DateTime hoy = DateTime.now();
		for(Frecuency frecuency:frecuencies){
			if (coincideDia(frecuency.getWeekDay(), hoy.getDayOfWeek())){
				diferencia = diferenciaTiempo(hoy, frecuency.getTime().toDateTime());
				if (diferencia >= 0 && diferencia < diferenciaMinima){
					diferenciaMinima = diferencia;
				}
			}
		}
		return diferenciaMinima;
	}

	public boolean coincideDia(String weekDay, int dayOfWeek) {
		if (weekDay.equalsIgnoreCase("LUNES") && (dayOfWeek == 1 || dayOfWeek == 2))
			return true;
		if (weekDay.equalsIgnoreCase("MARTES") && (dayOfWeek == 2 || dayOfWeek == 3))
			return true;
		if (weekDay.equalsIgnoreCase("MIERCOLES") && (dayOfWeek == 3 || dayOfWeek == 4))
			return true;
		if (weekDay.equalsIgnoreCase("JUEVES") && (dayOfWeek == 4 || dayOfWeek == 5))
			return true;
		if (weekDay.equalsIgnoreCase("VIERNES") && (dayOfWeek == 5 || dayOfWeek == 6))
			return true;
		if (weekDay.equalsIgnoreCase("SABADO") && (dayOfWeek == 6 || dayOfWeek == 7))
			return true;
		if (weekDay.equalsIgnoreCase("DOMINGO") && (dayOfWeek == 7 || dayOfWeek == 1))
			return true;
		return false;
	}

	public Integer diferenciaTiempo(DateTime inicio, DateTime fin) {
		Integer segundosInicio, segundosFin, difSegundos = null;
		if (inicio != null && fin != null){
			segundosInicio = inicio.getSecondOfDay();
			segundosFin = fin.getSecondOfDay();
			if (segundosFin >= segundosInicio) 
				difSegundos = segundosFin - segundosInicio;
			else
				difSegundos = 86400 + segundosFin - segundosInicio;
		}
		return difSegundos;
	}

	public Integer getStopOrder(Stop s) {
		for(int i = 0; i < stops.size(); i++)
			if(stops.get(i).equals(s))
				return i;
	
		return null;
	}

	public Stop getStopById(String stopId){
		Integer d = new Integer(stopId);
		for(Stop stop:stops){
			if (stop.getStopId().equals(d)){
				return stop;
			}
		}
		return null;
	}
	
	public Stop getStopByOrder(Integer order){
		if(order < this.stops.size())
			return stops.get(order);
		else
			return null;
	}
	
	
	/**
	 * Calcula la distancia entre dos paradas pertenecientes al recorrido.
	 * El cálculo se hace en el sentido del recorrido.
	 * @param start: Parada origen
	 * @param destination: Parada destino
	 * @return
	 */
	public Double getDistance(Stop start, Stop destination)
	{	
		if(start.equals(destination))
			return new Double(0);
		
		// Si las paradas son consecutivas
		if(consecutive(start,destination))
		{
			Double distance = Length.METER.fromRadians(new LatLonPoint.Float(start.getLat(),start.getLon())
			.distance(new LatLonPoint.Float(destination.getLat(),destination.getLon())));
			return distance;
		}
		else
		{
			Stop nextStop = getNextStop(start);
			return getDistance(start, nextStop) + 
					getDistance(nextStop, destination);
		}	
	}
	
	
	/**
	 * 
	 * @param stop
	 * @return
	 */
	public Stop getNextStop(Stop stop) {
		if(this.contains(stop))
			//Si stop no es la ultima parada
			if(getStopOrder(stop) < stops.size()-1)
				return this.getStopByOrder(getStopOrder(stop)+1);
			else
				return this.getFirstStop();
		else
			throw new IllegalArgumentException("The route doesn't contain the stop");
	}
	
	/**
	 * 
	 * @param stop
	 * @return
	 */
	public Stop getPreviousStop(Stop stop) {
		if(this.contains(stop))
			//Si stop es la primera parada
			if(getFirstStop().equals(stop))
				return this.getLastStop();
			else
				return this.getStopByOrder(getStopOrder(stop)-1);
		else
			throw new IllegalArgumentException("The route doesn't contain the stop");
	}
	
	/**
	 * 
	 * @param stop
	 * @return
	 */
	public boolean contains(Stop stop) {
		if(this.stops.contains(stop))
			return true;
		else
			return false;
	}

	/**
	 * 
	 * @return
	 */
	public Stop getFirstStop()
	{
		return stops.get(0);
	}
	
	/**
	 * 
	 * @return
	 */
	public Stop getLastStop()
	{
		return stops.get(stops.size()-1);
	}
	

	/**
	 * Determina si dos paradas son consecutivas. Se calcula en el sentido de circulación del 
	 * recorrido.
	 * Tener en cuenta que el recorrido es continuo, por lo que la ultima y primera parada 
	 * son consecutivas si se evaluan en ese orden.
	 * @param start: Parada de origen
	 * @param destination: Parada de destino
	 * @return devuelve true si son consecutivas, false de lo contrario
	 */

	public boolean consecutive(Stop start, Stop destination) {
		
		if(!this.contains(start) && !this.contains(destination))
			throw new IllegalArgumentException("The route doesn't contain the stop");
			
		Integer startOrder = getStopOrder(start);
		Integer destinationOrder = getStopOrder(destination);
		
		if(startOrder < destinationOrder)
			if(startOrder +1 == destinationOrder)
				return true;
			else
				return false;
		else
			//Si el origen es la ultima parada y el destino es la primera
			if(start.equals(this.getLastStop()) && destination.equals(this.getFirstStop()))
				return true;
			else
				return false;
	}

	public void processBusPosition(BusPositionData busPosition) 
	{
		Bus bus = buses.get(busPosition.getIdColectivo());
		
		if(bus == null)
		{
			bus = new Bus(busPosition.getIdColectivo(), this);
			buses.put(busPosition.getIdColectivo(), bus);			
		}	
		
		bus.processPosition(busPosition);
	}

	/**
	 * Encuentra la parada mas cercana a busPosition empezando desde currentStop
	 * @param busPosition
	 * @param currentStop
	 * @return
	 */
	protected Stop findNearestStop(BusPositionData busPosition, Stop currentStop) {
		
		Stop previousStop = this.getPreviousStop(currentStop);
		
		for(Stop stop = currentStop; !stop.equals(previousStop); stop = this.getNextStop(stop))
		{
			Double distance = stop.distance(busPosition.getCoordinates());
			Double stopHeading = calculateHeading(stop);
			Float busHeading = busPosition.getHeading();
			
			if(stopHeading != null && busHeading != null)
			{
				Double headingDifference = Math.abs(stopHeading - busHeading);
				
				if(distance < this.distanceTolerance && headingDifference < this.headingDifferenceTolerance)
					return stop;
			}
		}
		return null;
	}
	
	/**
	 * Encuentra la parada mas cercana empezando desde el principio del recorrido
	 * @param busPosition
	 * @return
	 */
	
	public Stop findNearestStop(BusPositionData busPosition) {
		return this.findNearestStop(busPosition, this.getFirstStop());
	}

	/**
	 * Calcula la direccion de la parada en el sentido del recorrido
	 * @param stop
	 * @return
	 */
	public Double calculateHeading(Stop stop) 
	{
		Stop nextStop = this.getNextStop(stop);
		
		LatLonPoint stopCoordinates = new LatLonPoint.Float(stop.getLat(), stop.getLon());
		Double heading = Length.DECIMAL_DEGREE.fromRadians(stopCoordinates.azimuth(new LatLonPoint.Float(nextStop.getLat(), nextStop.getLon())));
		
		if(heading < 0)
			heading = 360 + heading;
		
		return heading;		
	}


	public String getRouteName() {
		return routeName;
	}

	public void setRouteName(String routeName) {
		this.routeName = routeName;
	}

}
