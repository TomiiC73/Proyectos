package ar.edu.utn.frc.backend.services;

import ar.edu.utn.frc.backend.distancias.Coordenada;
import ar.edu.utn.frc.backend.distancias.ObtenerDistancia;
import ar.edu.utn.frc.backend.dto.DTOReporteDetallePruebaVehiculo;
import ar.edu.utn.frc.backend.dto.DTOReporteIncidente;
import ar.edu.utn.frc.backend.dto.DTOReporteIncidenteEmpleado;
import ar.edu.utn.frc.backend.dto.DTOReporteKilometrosRecorridos;
import ar.edu.utn.frc.backend.entities.*;
import ar.edu.utn.frc.backend.repositorios.InteresadoRepositorio;
import ar.edu.utn.frc.backend.repositorios.PosicionRepositorio;
import ar.edu.utn.frc.backend.repositorios.PruebaRepositorio;
import ar.edu.utn.frc.backend.repositorios.VehiculoRepositorio;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
@Service
public class ReporteService {
    private final PruebaRepositorio pruebaRepositorio;
    private final VehiculoRepositorio vehiculoRepositorio;
    private final List<DTOReporteIncidente> incidentes = new ArrayList<>();
    private final PosicionRepositorio posicionRepositorio;
    private final ObtenerDistancia obtenerDistancia;
    private final DTOReporteKilometrosRecorridos dtoReporteKilometrosRecorridos;
    private final InteresadoRepositorio interesadoRepositorio;

    public ReporteService(PruebaRepositorio pruebaRepositorio, VehiculoRepositorio vehiculoRepositorio, PosicionRepositorio posicionRepositorio, PosicionRepositorio posicionRepositorio1, ObtenerDistancia obtenerDistancia, DTOReporteKilometrosRecorridos dtoReporteKilometrosRecorridos, InteresadoRepositorio interesadoRepositorio) {
        this.pruebaRepositorio = pruebaRepositorio;
        this.vehiculoRepositorio = vehiculoRepositorio;
        this.posicionRepositorio = posicionRepositorio1;
        this.obtenerDistancia = obtenerDistancia;
        this.dtoReporteKilometrosRecorridos = dtoReporteKilometrosRecorridos;
        this.interesadoRepositorio = interesadoRepositorio;
    }

    // agregar un incidente a la lista
    public void agregarIncidente(DTOReporteIncidente incidente) {
        incidentes.add(incidente);
    }

    // obtener todos los incidentes registrados
    public List<DTOReporteIncidente> obtenerTodosLosIncidentes() {
        return new ArrayList<>(incidentes);
    }

    public DTOReporteIncidente obtenerDatosParaReporteIncidente(Long idVehiculo) {
        // Obtener el ID del vehículo por la patente
        Vehiculo vehiculo = vehiculoRepositorio.findById(idVehiculo)
                .orElseThrow(() -> new IllegalArgumentException("No se encontró el vehículo con la patente especificada."));


        // Obtener todas las pruebas activas y filtrar por el ID del vehículo
        Prueba prueba = pruebaRepositorio.findAll().stream()
                .filter(p -> p.getFechaHoraFin() == null && p.getVehiculo() != null && p.getVehiculo().getId().equals(vehiculo.getId()))
                .findFirst()
                .orElseThrow(() -> new NoSuchElementException("No se encontró una prueba activa para el id::" + idVehiculo));

        if (prueba == null) {
            throw new NoSuchElementException("No se encontró una prueba activa para la patente proporcionada.");
        }

        DTOReporteIncidente reporteIncidente = new DTOReporteIncidente();
        reporteIncidente.setPatente(vehiculo.getPatente());
        reporteIncidente.setInteresadoNombre(prueba.getInteresado().getNombre());
        reporteIncidente.setInteresadoApellido(prueba.getInteresado().getApellido());
        reporteIncidente.setNombreEmpleado(prueba.getEmpleado().getNombre());
        reporteIncidente.setApellidoEmpleado(prueba.getEmpleado().getApellido());
        reporteIncidente.setFechaHoraIncidente(LocalDateTime.now()); // Fecha y hora actuales para el incidente
        reporteIncidente.setDescripcionIncidente("Incidente detectado en la verificación de zona.");

        return reporteIncidente;
    }

    public List<DTOReporteIncidenteEmpleado> obtenerIncidentesPorEmpleado(String nombreEmpleado, String apellidoEmpleado) {
        // Obtener todos los incidentes
        List<DTOReporteIncidente> incidentes = obtenerTodosLosIncidentes();

        // Filtrar y mapear a DTOReporteIncidenteEmpleado
        return incidentes.stream()
                .filter(incidente -> incidente.getNombreEmpleado().equalsIgnoreCase(nombreEmpleado)
                        && incidente.getApellidoEmpleado().equalsIgnoreCase(apellidoEmpleado))
                .map(incidente -> new DTOReporteIncidenteEmpleado(
                        incidente.getPatente(),
                        incidente.getNombreEmpleado(),
                        incidente.getApellidoEmpleado(),
                        incidente.getInteresadoNombre(),
                        incidente.getInteresadoApellido(),
                        incidente.getFechaHoraIncidente(),
                        incidente.getDescripcionIncidente()
                ))
                .collect(Collectors.toList());
    }

    public Double obtenerKmRecorridoDeVehiculo(DTOReporteKilometrosRecorridos dtoReporteKilometrosRecorridos) {
        // Obtener el vehículo por su patente
        Vehiculo vehiculo = vehiculoRepositorio.findByPatente(dtoReporteKilometrosRecorridos.getPatente());

        if (vehiculo == null) {
            log.error("Vehículo no encontrado con patente: " + dtoReporteKilometrosRecorridos.getPatente());
            throw new IllegalArgumentException("Vehículo no encontrado con la patente: " + dtoReporteKilometrosRecorridos.getPatente());
        }

        // Obtener las posiciones del vehículo dentro del rango de fechas
        List<Posicion> posicionesVehiculo = posicionRepositorio.findPosicionsByVehiculoAndFecha(
                vehiculo,
                dtoReporteKilometrosRecorridos.getFechaHoraInicio(),
                dtoReporteKilometrosRecorridos.getFechaHoraFin()
        );

        if (posicionesVehiculo.isEmpty()) {
            log.error("No se encontraron posiciones para el vehículo con patente: " + dtoReporteKilometrosRecorridos.getPatente() + " en el rango de fechas.");
            throw new IllegalArgumentException("No se encontraron posiciones para el vehículo con patente: " + dtoReporteKilometrosRecorridos.getPatente());
        }

        // Coordenadas de la agencia (punto de inicio)
        Coordenada coordenadaAgencia = new Coordenada(42.50886738457441, 1.5347139324337429); // Lat y Lon de la agencia

        Double distanciaTotalKm = 0.0;

        Coordenada coordenadaAnterior = coordenadaAgencia; // La agencia es el primer punto de referencia

        for (Posicion posicionActual : posicionesVehiculo) {
            // Crear la coordenada actual del vehículo
            Coordenada coordenadaActual = new Coordenada(posicionActual.getLatitud(), posicionActual.getLongitud());

            // Calcular la distancia entre la coordenada anterior (agencia o punto anterior) y la actual
            Double distanciaKm = obtenerDistancia.calcularDistancia(coordenadaAnterior, coordenadaActual);

            distanciaTotalKm += distanciaKm;

            coordenadaAnterior = coordenadaActual; // la "coordenadaAnterior" se convierte en la "coordenadaActual"
        }

        return distanciaTotalKm;
    }

    public List<DTOReporteDetallePruebaVehiculo> obtenerDetalleDePruebasPorVehiculo(Long idVehiculo) {
        // Obtengo las pruebas asociadas al vehículo
        List<Prueba> pruebas = pruebaRepositorio.findByVehiculoId(idVehiculo);
        String patente = vehiculoRepositorio.findVehiculoPatenteById(idVehiculo);

        // Si no hay pruebas, retorno una lista vacía
        if (pruebas.isEmpty()) {
            return Collections.emptyList();
        }

        // Mapear las pruebas a DTOs
        List<DTOReporteDetallePruebaVehiculo> reportePruebas = pruebas.stream()
                .map(prueba -> {
                    // Obtengo los datos relacionados con la prueba: Interesado y Empleado
                    Optional<Interesado> interesado = interesadoRepositorio.findInteresadoByPruebaId(prueba.getId());
                    Optional<Empleado> empleado = pruebaRepositorio.findEmpleadoByPruebaId(prueba.getId());

                    // Creo el DTO para la prueba
                    DTOReporteDetallePruebaVehiculo dto = new DTOReporteDetallePruebaVehiculo();
                    dto.setPruebaId(prueba.getId());
                    dto.setPatente(patente);

                    // Verifico si el interesado existe, sino asigno un valor por defecto
                    if (interesado.isPresent()) {
                        dto.setNombreInteresado(interesado.get().getNombre());
                        dto.setApellidoInteresado(interesado.get().getApellido());
                    } else {
                        dto.setNombreInteresado("Desconocido");
                        dto.setApellidoInteresado("Desconocido");
                    }

                    // Verifico si el empleado existe, sino asigno un valor por defecto
                    if (empleado.isPresent()) {
                        dto.setNombreEmpleado(empleado.get().getNombre());
                        dto.setApellidoEmpleado(empleado.get().getApellido());
                    } else {
                        dto.setNombreEmpleado("Desconocido");
                        dto.setApellidoEmpleado("Desconocido");
                    }

                    // Seteo las fechas y comentarios
                    dto.setFechaHoraInicio(prueba.getFechaHoraInicio());
                    dto.setFechaHoraFin(prueba.getFechaHoraFin());
                    dto.setComentarios(Optional.ofNullable(prueba.getComentarios()).orElse("Sin comentarios"));

                    return dto;
                })
                .collect(Collectors.toList());

        // Retorno el reporte con los detalles de las pruebas
        return reportePruebas;
    }
}